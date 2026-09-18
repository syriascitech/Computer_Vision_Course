#!/usr/bin/env python3
"""
يبني قاعدة بيانات الأسبوع 7 (كشف مركبات الطوارئ) من Open Images V6/V7.

لماذا Open Images؟
  - صناديق إحاطة حقيقية موسومة يدوياً على صور شوارع حقيقية.
  - الفئة Ambulance موجودة فيها، وهي الفئة التي تعجز COCO عن التعبير عنها.
  - الصور برخصة CC BY 2.0 والتوسيم برخصة CC BY 4.0، فيمكن إعادة نشرها في
    مستودع تعليمي مفتوح.
  - التنزيل بلا مفاتيح ولا تسجيل.

المخرَج: مجلد بصيغة YOLO جاهز للاستخدام بلا إنترنت داخل Week7/dataset/.

الاستخدام:
    python tools/prepare_week7_dataset.py --work-dir /path/to/scratch --out Week7/dataset
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import random
import shutil
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from PIL import Image

# ترتيب الفئات هو ترتيب class_id في ملفات التوسيم، ولا يجوز تغييره بعد التصدير.
CLASSES = ["ambulance", "car", "truck", "bus"]
MID_TO_CLASS = {
    "/m/012n7d": "ambulance",
    "/m/0k4j": "car",
    "/m/07r04": "truck",
    "/m/01bjv": "bus",
}
CLASS_TO_ID = {name: i for i, name in enumerate(CLASSES)}

S3_URL = "https://open-images-dataset.s3.amazonaws.com/{split}/{image_id}.jpg"

# أعمدة ملفات Open Images: أول 13 عموداً متطابقة بين train و validation و test.
COL_IMAGE_ID, COL_LABEL = 0, 2
COL_XMIN, COL_XMAX, COL_YMIN, COL_YMAX = 4, 5, 6, 7
COL_IS_GROUP_OF, COL_IS_DEPICTION = 10, 11

MIN_BOX_REL_SIDE = 0.02  # نتجاهل الصناديق الأصغر من 2% من ضلع الصورة

# تسميات Open Images هرمية، فقد يحمل الجسم الواحد تسميتين معاً: سيارة الإسعاف
# توسَم أحياناً ambulance و truck في الوقت نفسه. لو تركنا الاثنين لأعطينا
# النموذج إشارتين متناقضتين على البكسلات نفسها، وهو بالضبط الالتباس الذي
# نريد أن نعلّمه تجنّبه. لذلك نُبقي التسمية الأكثر تخصيصاً فقط.
SPECIFICITY = {"ambulance": 0, "bus": 1, "truck": 2, "car": 3}
DUPLICATE_IOU = 0.6


def parse_annotations(path: Path, has_header: bool) -> dict[str, list[tuple]]:
    """يقرأ ملف توسيم Open Images ويعيد {image_id: [(class_name, xmin, xmax, ymin, ymax), ...]}."""
    boxes: dict[str, list[tuple]] = defaultdict(list)
    skipped_group = skipped_depiction = 0

    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        if has_header:
            next(reader, None)

        for row in reader:
            if len(row) < 13:
                continue

            class_name = MID_TO_CLASS.get(row[COL_LABEL])
            if class_name is None:
                continue

            # IsGroupOf يعني صندوقاً يغطي مجموعة أجسام دفعة واحدة، وهو يسمّم التدريب.
            if row[COL_IS_GROUP_OF] == "1":
                skipped_group += 1
                continue

            # IsDepiction يعني رسماً أو صورة داخل صورة، لا جسماً حقيقياً.
            if row[COL_IS_DEPICTION] == "1":
                skipped_depiction += 1
                continue

            boxes[row[COL_IMAGE_ID]].append(
                (
                    class_name,
                    float(row[COL_XMIN]),
                    float(row[COL_XMAX]),
                    float(row[COL_YMIN]),
                    float(row[COL_YMAX]),
                )
            )

    print(
        f"  {path.name}: {len(boxes)} صورة، "
        f"تجاهلنا {skipped_group} صندوق IsGroupOf و {skipped_depiction} صندوق IsDepiction"
    )
    return boxes


def box_iou(a: tuple, b: tuple) -> float:
    """IoU بين صندوقين بصيغة (xmin, xmax, ymin, ymax)."""
    axmin, axmax, aymin, aymax = a
    bxmin, bxmax, bymin, bymax = b

    inter_w = max(0.0, min(axmax, bxmax) - max(axmin, bxmin))
    inter_h = max(0.0, min(aymax, bymax) - max(aymin, bymin))
    intersection = inter_w * inter_h

    union = (
        (axmax - axmin) * (aymax - aymin)
        + (bxmax - bxmin) * (bymax - bymin)
        - intersection
    )
    return intersection / union if union > 0 else 0.0


def drop_duplicate_labels(boxes: list[tuple]) -> tuple[list[tuple], int]:
    """يحذف الصندوق الأقل تخصيصاً حين يغطي صندوقان من فئتين الجسم نفسه."""
    dropped = set()

    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if i in dropped or j in dropped:
                continue

            name_i, *coords_i = boxes[i]
            name_j, *coords_j = boxes[j]
            if name_i == name_j:
                continue

            if box_iou(tuple(coords_i), tuple(coords_j)) > DUPLICATE_IOU:
                loser = i if SPECIFICITY[name_i] > SPECIFICITY[name_j] else j
                dropped.add(loser)

    return [b for k, b in enumerate(boxes) if k not in dropped], len(dropped)


def to_yolo_lines(boxes: list[tuple]) -> list[str]:
    """يحوّل صناديق Open Images (xmin,xmax,ymin,ymax مطبَّعة) إلى أسطر YOLO."""
    lines = []
    for class_name, xmin, xmax, ymin, ymax in boxes:
        width = xmax - xmin
        height = ymax - ymin
        if width < MIN_BOX_REL_SIDE or height < MIN_BOX_REL_SIDE:
            continue

        x_center = xmin + width / 2
        y_center = ymin + height / 2
        lines.append(
            f"{CLASS_TO_ID[class_name]} "
            f"{x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
        )
    return lines


def download_and_resize(
    image_id: str, split: str, dest: Path, max_side: int, quality: int
) -> bool:
    """ينزّل صورة واحدة ويصغّرها ويحفظها. يعيد True عند النجاح."""
    if dest.exists():
        return True

    try:
        response = requests.get(
            S3_URL.format(split=split, image_id=image_id), timeout=30
        )
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content)).convert("RGB")
    except Exception:
        return False

    scale = max_side / max(image.size)
    if scale < 1:
        new_size = (round(image.width * scale), round(image.height * scale))
        image = image.resize(new_size, Image.LANCZOS)

    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest, "JPEG", quality=quality, optimize=True)
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-side", type=int, default=416)
    parser.add_argument("--quality", type=int, default=78)
    parser.add_argument("--negatives", type=int, default=280)
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    random.seed(args.seed)

    sources = [
        (args.work_dir / "train-bbox-filtered.csv", "train", False),
        (args.work_dir / "validation-bbox.csv", "validation", True),
        (args.work_dir / "test-bbox.csv", "test", True),
    ]

    print("قراءة ملفات التوسيم:")
    boxes_by_image: dict[str, list[tuple]] = {}
    split_of_image: dict[str, str] = {}

    for path, split, has_header in sources:
        if not path.exists():
            print(f"  ملف مفقود: {path}", file=sys.stderr)
            return 1
        for image_id, boxes in parse_annotations(path, has_header).items():
            boxes_by_image[image_id] = boxes
            split_of_image[image_id] = split

    # الصور الإيجابية: كل صورة فيها إسعاف واحد على الأقل.
    positives = [
        image_id
        for image_id, boxes in boxes_by_image.items()
        if any(name == "ambulance" for name, *_ in boxes)
    ]

    # الصور السلبية: مركبات عادية بلا إسعاف. نفضّل ما فيه شاحنة أو باص لأن
    # صور السيارات وحدها وفيرة ومملة، والتنوّع أهم من الكم.
    negatives_pool = [
        image_id
        for image_id, boxes in boxes_by_image.items()
        if image_id not in set(positives)
        and any(name in {"truck", "bus"} for name, *_ in boxes)
    ]
    random.shuffle(negatives_pool)
    negatives = negatives_pool[: args.negatives]

    selected = positives + negatives
    print(
        f"\nاخترنا {len(selected)} صورة: "
        f"{len(positives)} فيها إسعاف، و {len(negatives)} مركبات عادية فقط."
    )

    # التنزيل والتصغير.
    raw_dir = args.work_dir / "images_resized"
    raw_dir.mkdir(parents=True, exist_ok=True)

    print("\nتنزيل الصور وتصغيرها...")
    ok: list[str] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                download_and_resize,
                image_id,
                split_of_image[image_id],
                raw_dir / f"{image_id}.jpg",
                args.max_side,
                args.quality,
            ): image_id
            for image_id in selected
        }
        for done, future in enumerate(as_completed(futures), 1):
            if future.result():
                ok.append(futures[future])
            if done % 200 == 0:
                print(f"  {done}/{len(selected)} … نجح {len(ok)}")

    print(f"نزّلنا {len(ok)} صورة بنجاح من أصل {len(selected)}.")

    # التقسيم. صور Open Images مستقلة تماماً (لقطات من مصوّرين مختلفين)، فلا
    # يوجد خطر تسرّب بين المجموعات كما يحدث مع إطارات فيديو واحد.
    random.shuffle(ok)
    n_train = int(0.70 * len(ok))
    n_valid = int(0.20 * len(ok))
    partitions = {
        "train": ok[:n_train],
        "valid": ok[n_train : n_train + n_valid],
        "test": ok[n_train + n_valid :],
    }

    if args.out.exists():
        shutil.rmtree(args.out)

    stats: dict[str, Counter] = {}
    image_counts: dict[str, int] = {}
    duplicates_removed: Counter = Counter()

    for split_name, image_ids in partitions.items():
        images_dir = args.out / split_name / "images"
        labels_dir = args.out / split_name / "labels"
        images_dir.mkdir(parents=True, exist_ok=True)
        labels_dir.mkdir(parents=True, exist_ok=True)

        counter: Counter = Counter()
        kept = 0

        for image_id in image_ids:
            cleaned, n_dropped = drop_duplicate_labels(boxes_by_image[image_id])
            duplicates_removed[split_name] += n_dropped

            lines = to_yolo_lines(cleaned)
            if not lines:
                continue

            shutil.copy2(raw_dir / f"{image_id}.jpg", images_dir / f"{image_id}.jpg")
            (labels_dir / f"{image_id}.txt").write_text("\n".join(lines) + "\n")

            for line in lines:
                counter[CLASSES[int(line.split()[0])]] += 1
            kept += 1

        stats[split_name] = counter
        image_counts[split_name] = kept

    # نتعمّد عدم كتابة المفتاح path. حين يغيب تعتمد Ultralytics مجلد ملف
    # الـ yaml نفسه جذراً، فيعمل المجلد أينما نُسخ ومن أي مجلد عمل شُغّل.
    # لو كتبنا "path: ." لحُلّت النقطة إلى مجلد العمل الحالي لا إلى مجلد
    # قاعدة البيانات، ولفشل التدريب برسالة "images not found".
    (args.out / "data.yaml").write_text(
        "# قاعدة بيانات الأسبوع 7 - كشف مركبات الطوارئ\n"
        "# المصدر: Open Images V6/V7 (Google)\n"
        "#\n"
        "# لا نكتب المفتاح path عمداً: حين يغيب، تعتمد Ultralytics مجلد هذا الملف\n"
        "# نفسه جذراً للمسارات، فيعمل المجلد أينما نُسخ ومن أي مكان شُغّل الدفتر.\n"
        "train: train/images\n"
        "val: valid/images\n"
        "test: test/images\n\n"
        f"nc: {len(CLASSES)}\n"
        f"names: {json.dumps(CLASSES)}\n"
    )

    (args.out / "LICENSE.md").write_text(
        "# مصدر قاعدة البيانات ورخصتها\n\n"
        "استُخرجت هذه المجموعة من **Open Images Dataset V6/V7** من Google.\n\n"
        "- صفحة المجموعة: https://storage.googleapis.com/openimages/web/index.html\n"
        "- **الصور**: منشورة على Flickr برخصة "
        "[CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)، "
        "وحقوقها لأصحابها الأصليين.\n"
        "- **التوسيم (صناديق الإحاطة)**: من Google برخصة "
        "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).\n\n"
        "## ما فعلناه بها\n\n"
        f"1. اخترنا أربع فئات فقط: {'، '.join(CLASSES)}.\n"
        "2. أخذنا كل صورة تحتوي على `ambulance`، وأضفنا عيّنة من صور المركبات "
        "العادية كأمثلة سلبية.\n"
        "3. تجاهلنا الصناديق المعلّمة `IsGroupOf` (صندوق يغطي مجموعة أجسام) "
        "و `IsDepiction` (رسم أو صورة داخل صورة).\n"
        f"4. صغّرنا كل صورة إلى {args.max_side}px للضلع الأطول بجودة JPEG "
        f"{args.quality} لتقليل الحجم.\n"
        "5. حوّلنا التوسيم من صيغة Open Images (`XMin, XMax, YMin, YMax`) إلى "
        "صيغة YOLO (`class x_center y_center width height`).\n\n"
        "سكربت التحويل كاملاً في `tools/prepare_week7_dataset.py`.\n"
    )

    # التقرير النهائي.
    print("\n" + "=" * 62)
    print("قاعدة البيانات جاهزة:", args.out)
    print("=" * 62)
    header = f"{'المجموعة':<10}{'صور':>8}" + "".join(f"{c:>12}" for c in CLASSES)
    print(header)
    total = Counter()
    for split_name in ("train", "valid", "test"):
        counter = stats[split_name]
        total.update(counter)
        row = f"{split_name:<10}{image_counts[split_name]:>8}"
        row += "".join(f"{counter[c]:>12}" for c in CLASSES)
        print(row)
    print("-" * len(header))
    row = f"{'المجموع':<10}{sum(image_counts.values()):>8}"
    row += "".join(f"{total[c]:>12}" for c in CLASSES)
    print(row)

    print(
        f"\nحذفنا {sum(duplicates_removed.values())} صندوقاً مكرراً "
        "(الجسم نفسه موسوم بفئتين، أبقينا الأكثر تخصيصاً)."
    )

    size_mb = sum(p.stat().st_size for p in args.out.rglob("*") if p.is_file()) / 1e6
    print(f"الحجم على القرص: {size_mb:.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
