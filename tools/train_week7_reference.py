#!/usr/bin/env python3
"""
يجري التدريب المرجعي الكامل للأسبوع 7 مرة واحدة، ثم يجمع مخرجاته في
Week7/runs_reference/emergency_full/ لتُرفَق مع الدرس.

الطلاب لا يشغّلون هذا السكربت. الدفتر يقرأ نتائجه فقط، لأن التدريب الكامل
لا يمكن إنجازه داخل الحصة على معالج.

نستخدم imgsz=416 لأنه حجم الصور المغلَّفة نفسه، فلا معنى لتكبيرها.

الاستخدام:
    python tools/train_week7_reference.py
"""

from __future__ import annotations

import os
import shutil
import time
from pathlib import Path

os.environ["YOLO_VERBOSE"] = "True"

WEEK7 = Path(__file__).resolve().parent.parent / "Week7"
REFERENCE_DIR = WEEK7 / "runs_reference" / "emergency_full"

# الملفات التي يحتاجها الدفتر من مخرجات التدريب. نأخذها فقط لنبقى ضمن
# ميزانية حجم المجلد.
# ملاحظة: تسمّي Ultralytics 8.4 منحنيات المقاييس بسابقة Box، أي
# BoxPR_curve.png لا PR_curve.png كما في الإصدارات الأقدم.
WANTED = [
    "results.csv",
    "results.png",
    "confusion_matrix_normalized.png",
    "confusion_matrix.png",
    "BoxPR_curve.png",
    "BoxF1_curve.png",
    "labels.jpg",
    "val_batch0_pred.jpg",
    "val_batch0_labels.jpg",
    "args.yaml",
]


def main() -> None:
    os.chdir(WEEK7)

    from ultralytics import YOLO, settings

    settings.update({"sync": False})

    model = YOLO("models/yolo11n.pt")

    started = time.time()
    model.train(
        data="dataset/data.yaml",
        epochs=60,
        imgsz=416,
        batch=16,
        device="cpu",
        workers=8,
        amp=False,
        patience=15,
        plots=True,
        name="emergency_full",
        exist_ok=True,
        seed=7,
    )
    minutes = (time.time() - started) / 60

    save_dir = Path(model.trainer.save_dir)
    print(f"\nانتهى التدريب في {minutes:.1f} دقيقة. المخرجات في {save_dir}")

    # تقييم نهائي نزيه على مجموعة الاختبار التي لم تُستخدم في التدريب.
    best = YOLO(str(save_dir / "weights" / "best.pt"))
    metrics = best.val(data="dataset/data.yaml", split="test", imgsz=416,
                       device="cpu", verbose=False)

    print("\nالنتائج على مجموعة الاختبار:")
    print(f"  mAP@50    : {metrics.box.map50:.3f}")
    print(f"  mAP@50-95 : {metrics.box.map:.3f}")

    names = best.names
    for index, class_id in enumerate(metrics.ap_class_index):
        print(
            f"  {names[class_id]:10s} "
            f"P={metrics.box.p[index]:.3f} "
            f"R={metrics.box.r[index]:.3f} "
            f"mAP50={metrics.box.ap50[index]:.3f}"
        )

    # تجميع ما يحتاجه الدفتر.
    if REFERENCE_DIR.exists():
        shutil.rmtree(REFERENCE_DIR)
    REFERENCE_DIR.mkdir(parents=True)

    for filename in WANTED:
        source = save_dir / filename
        if source.exists():
            shutil.copy2(source, REFERENCE_DIR / filename)
        else:
            print("  ملف غير موجود، تخطّيناه:", filename)

    shutil.copy2(save_dir / "weights" / "best.pt", WEEK7 / "models" / "emergency_best.pt")

    total_kb = sum(p.stat().st_size for p in REFERENCE_DIR.rglob("*") if p.is_file()) / 1024
    print(f"\nجُمعت المخرجات في {REFERENCE_DIR} ({total_kb:.0f} KB)")
    print("ونُسخ النموذج إلى Week7/models/emergency_best.pt")


if __name__ == "__main__":
    main()
