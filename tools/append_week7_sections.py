#!/usr/bin/env python3
"""
يضيف الأقسام 4 حتى 15 إلى دفتر الأسبوع 7 دون المساس بالخلايا السابقة.

نضيف ولا نعيد التوليد، لأن الدفتر يُحرَّر يدوياً بين الجولات. السكربت
قابل لإعادة التشغيل: إن وجد القسم الرابع موجوداً مسبقاً حذف كل ما بعده
وأعاد بناءه.

أشكال الدرس موصوفة في Week7/media/FIGURE_BRIEFS.md ويشير إليها الدفتر
بمسار نسبي فقط.

الاستخدام:
    python tools/append_week7_sections.py
"""

from __future__ import annotations

import json
from pathlib import Path

NOTEBOOK = Path("Week7/week_7_training_and_finetuning.ipynb")
SECTION_4_MARKER = "<h1>4. التعزيز"
FIGURE_6_MARKER = "دور كل قسم من الأقسام الثلاثة"
DATA_YAML_NOTES_MARKER = "لاحظ نقطتين مهمتين"

# ملاحظة ثالثة على ملف data.yaml. أضفناها بعد أن أوقع غيابُ هذا التوضيح
# التدريبَ المرجعي في خطأ "images not found".
DATA_YAML_NOTES = """<p>لاحظ ثلاث نقاط مهمة:</p>

<ul>
<li>كل صورة <code>img_001.jpg</code> يقابلها ملف <code>img_001.txt</code>
بالاسم نفسه تماماً، في مجلد <code>labels</code> الموازي لمجلد
<code>images</code>. هذه ليست عادة تنظيمية بل هي الطريقة التي تعثر بها
Ultralytics على التوسيم.</li>
<li>ترتيب الأسماء في <code>names</code> هو الذي يحدّد
<code>class_id</code>. لو غيّرت الترتيب بعد التوسيم فسدت كل الملفات
دفعة واحدة.</li>
<li>لا يوجد مفتاح <code>path</code> في ملفنا، وهذا مقصود. حين يغيب
<code>path</code> تعتبر Ultralytics <strong>مجلد ملف data.yaml نفسه</strong>
جذراً للمسارات.</li>
</ul>

<div class="note">
<p><strong>فخّ يقع فيه كثيرون:</strong> لو كتبت <code>path: .</code> ظاناً
أنها تعني «المجلد الحالي لهذا الملف»، فستفاجأ بأن النقطة تُحلّ إلى
<strong>مجلد العمل الذي شُغّل منه الدفتر</strong> لا إلى مجلد قاعدة
البيانات. عندها يبحث التدريب عن <code>valid/images</code> في المكان
الخطأ ويفشل برسالة <code>images not found</code>.</p>
<p>الحل: إما أن تحذف <code>path</code> تماماً كما فعلنا، أو أن تكتب مساراً
مطلقاً كاملاً.</p>
</div>"""

RTL_OPEN = '<div dir="rtl" class="rtl-cell" style="direction:rtl; text-align:right;">'
RTL_CLOSE = "</div>"

new_cells: list[dict] = []


def _cell(kind: str, text: str) -> dict:
    cell = {
        "cell_type": kind,
        "metadata": {},
        "source": [l + "\n" for l in text.split("\n")],
    }
    if kind == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell


def rtl(body: str) -> None:
    new_cells.append(_cell("markdown", f"{RTL_OPEN}\n\n{body.strip()}\n\n{RTL_CLOSE}"))


def figure(number: int, filename: str) -> None:
    """إشارة إلى شكل بصيغة markdown، والوصف الكامل في FIGURE_BRIEFS.md."""
    new_cells.append(_cell("markdown", f"![Figure {number}](media/{filename})"))


def code(src: str) -> None:
    new_cells.append(_cell("code", src.strip()))


# ===========================================================================
# 4. التعزيز
# ===========================================================================

rtl(
    """<hr />
<h1>4. التعزيز Data Augmentation</h1>

<h2>4.1 لماذا نحتاجه؟</h2>

<p>قاعدة بياناتنا فيها 477 صورة تدريب فقط. لو عرضناها على النموذج كما هي
ستين مرة، فسيحفظها حفظاً بدل أن يتعلّم منها، وسيفشل على أول صورة جديدة.</p>

<p>التعزيز يحلّ هذا بأن يعرض النموذج نسخة معدَّلة قليلاً من الصورة في كل
مرة: مقلوبة، أو أفتح، أو مقصوصة، أو مصغَّرة. فيرى النموذج عملياً آلاف
الصور المختلفة من مئاتٍ قليلة، ويتعلّم أن سيارة الإسعاف تبقى سيارة إسعاف
مهما تغيّر لون الإضاءة أو زاوية اللقطة.</p>

<div class="note">
<p><strong>قاعدة أساسية:</strong> التعزيز يُطبَّق على الصورة
<strong>وعلى صناديقها معاً</strong>. لو قلبنا الصورة أفقياً ونسينا قلب
الصناديق، لأصبح كل توسيمنا خاطئاً. مكتبة Ultralytics تتولى هذا تلقائياً،
لكن إن كتبت تعزيزاً بنفسك فهذه مسؤوليتك.</p>
</div>

<h2>4.2 ما تفعله Ultralytics تلقائياً</h2>

<p>عند استدعاء <code>model.train()</code> تُطبَّق مجموعة تعزيزات افتراضية
دون أن تطلبها:</p>

<table>
<thead>
<tr><th>المعامل</th><th>القيمة الافتراضية</th><th>ماذا يفعل</th></tr>
</thead>
<tbody>
<tr><td><code>mosaic</code></td><td>1.0</td>
    <td>يدمج أربع صور في صورة واحدة، وهو الأقوى أثراً</td></tr>
<tr><td><code>fliplr</code></td><td>0.5</td>
    <td>يقلب الصورة أفقياً في نصف الحالات</td></tr>
<tr><td><code>scale</code></td><td>0.5</td>
    <td>يكبّر ويصغّر ليتعلّم النموذج أحجاماً مختلفة</td></tr>
<tr><td><code>translate</code></td><td>0.1</td>
    <td>يزيح الصورة قليلاً</td></tr>
<tr><td><code>hsv_h / hsv_s / hsv_v</code></td><td>0.015 / 0.7 / 0.4</td>
    <td>يغيّر التدرّج والتشبّع والإضاءة</td></tr>
<tr><td><code>erasing</code></td><td>0.4</td>
    <td>يمسح جزءاً عشوائياً ليتعلّم التعامل مع الحجب</td></tr>
</tbody>
</table>

<p>أقواها أثراً هو <strong>Mosaic</strong>. الشكل التالي يوضح كيف يعمل:</p>"""
)

figure(7, "mosaic_augmentation.jpg")

rtl(
    """<h2>4.3 لنرَ التعزيز على بياناتنا</h2>

<p>بدل أن نصدّق الكلام، لنطبّق بعض هذه التحويلات على صورة حقيقية من
قاعدة بياناتنا وننظر إلى النتيجة.</p>"""
)

code(
    '''augmentation_source = sorted(Path("dataset/train/images").glob("*.jpg"))[3]
original = cv2.cvtColor(cv2.imread(str(augmentation_source)), cv2.COLOR_BGR2RGB)
height, width = original.shape[:2]

# قلب أفقي
flipped = original[:, ::-1]

# تغيير الإضاءة والتشبّع عبر فضاء HSV
hsv = cv2.cvtColor(original, cv2.COLOR_RGB2HSV).astype(np.int16)
hsv[..., 1] = np.clip(hsv[..., 1] * 1.6, 0, 255)   # تشبّع أعلى
hsv[..., 2] = np.clip(hsv[..., 2] * 0.55, 0, 255)  # إضاءة أخفض
darker = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

# تكبير مع قصّ من المركز
zoom = 1.4
zoomed = cv2.resize(original, None, fx=zoom, fy=zoom)
oy = (zoomed.shape[0] - height) // 2
ox = (zoomed.shape[1] - width) // 2
zoomed = zoomed[oy:oy + height, ox:ox + width]

# إزاحة
shift = np.float32([[1, 0, 0.12 * width], [0, 1, -0.08 * height]])
translated = cv2.warpAffine(original, shift, (width, height))

# مسح جزء عشوائي
erased = original.copy()
erased[int(0.35 * height):int(0.65 * height), int(0.30 * width):int(0.55 * width)] = 114

panels = [
    ("Original", original),
    ("Horizontal flip", flipped),
    ("HSV shift", darker),
    ("Scale + crop", zoomed),
    ("Translate", translated),
    ("Random erasing", erased),
]

fig, axes = plt.subplots(2, 3, figsize=(16, 9))

for ax, (title, image) in zip(axes.flat, panels):
    ax.imshow(image)
    ax.set_title(title, fontsize=13)
    ax.axis("off")

plt.suptitle("The same image, six ways the model will see it", fontsize=16)
plt.tight_layout()
plt.show()'''
)

rtl(
    """<h2>4.4 التعزيز الذي يضرّ</h2>

<p>التعزيز ليس دائماً مفيداً. القاعدة: <strong>لا تولّد صوراً لا يمكن أن
تظهر في الواقع، ولا تغيّر ما يحمل المعنى.</strong></p>

<ul>
<li><strong>القلب الرأسي</strong> (<code>flipud</code>): سيارة مقلوبة رأساً
على عقب لا تحدث في الشارع. اتركه صفراً في مسائل المرور.</li>
<li><strong>القلب الأفقي مع النصوص</strong>: لو كنا نقرأ لوحات الأرقام أو
لافتات، فالقلب الأفقي يجعل الكتابة معكوسة ويعلّم النموذج شيئاً خاطئاً.
في حالتنا نحن نكشف المركبة كاملة لا نقرأ نصاً، فالقلب مفيد.</li>
<li><strong>تغيير الألوان بإفراط</strong>: سيارة الإسعاف تُعرف جزئياً
بلونها الأبيض وعلاماتها الحمراء. لو غيّرنا التدرّج
(<code>hsv_h</code>) كثيراً لمحونا إشارة مهمة يعتمد عليها النموذج.</li>
<li><strong>التدوير الكبير</strong>: مفيد في صور الأقمار الصناعية، ضار في
كاميرا مثبّتة على عمود.</li>
</ul>

<blockquote>
<p>اسأل نفسك دائماً: هل يمكن أن تصل هذه الصورة من الكاميرا الحقيقية؟ إن
كان الجواب لا، فالتعزيز يضرّ لا ينفع.</p>
</blockquote>"""
)


# ===========================================================================
# 5. تشريح عملية التدريب
# ===========================================================================

rtl(
    """<hr />
<h1>5. تشريح عملية التدريب</h1>

<p>قبل أن نضغط زر التدريب، لنفهم ماذا يحدث بالضبط ومعنى كل رقم سنراه.</p>

<h2>5.1 Epoch و Batch و Iteration</h2>

<p>ثلاثة مصطلحات يخلط بينها كثيرون:</p>

<ul>
<li><strong>Batch</strong>: عدد الصور التي يعالجها النموذج دفعة واحدة قبل
أن يعدّل أوزانه مرة. مقيَّد بحجم الذاكرة.</li>
<li><strong>Iteration</strong>: تعديل واحد للأوزان، أي معالجة batch واحد.</li>
<li><strong>Epoch</strong>: مرور كامل على كل صور التدريب مرة واحدة.</li>
</ul>

<p>بالأرقام في تدريبنا المصغّر:</p>"""
)

code(
    '''MINI_TRAIN_IMAGES = 100
MINI_BATCH = 8
MINI_EPOCHS = 5

iterations_per_epoch = -(-MINI_TRAIN_IMAGES // MINI_BATCH)   # قسمة لأعلى

print(f"صور التدريب      : {MINI_TRAIN_IMAGES}")
print(f"حجم الـ batch     : {MINI_BATCH}")
print(f"iterations في كل epoch : {iterations_per_epoch}")
print(f"عدد الـ epochs    : {MINI_EPOCHS}")
print(f"إجمالي تعديلات الأوزان : {iterations_per_epoch * MINI_EPOCHS}")'''
)

rtl(
    """<h2>5.2 خسائر YOLO الثلاث</h2>

<p>أثناء التدريب ستظهر ثلاثة أرقام للخسارة، لأن الكشف ثلاث مسائل في آن
واحد:</p>

<table>
<thead>
<tr><th>الخسارة</th><th>تقيس</th><th>حين ترتفع فهذا يعني</th></tr>
</thead>
<tbody>
<tr><td><code>box_loss</code></td>
    <td>دقة موضع الصندوق وحجمه</td>
    <td>النموذج يجد الأجسام لكن صناديقه غير دقيقة</td></tr>
<tr><td><code>cls_loss</code></td>
    <td>صحة الفئة المختارة</td>
    <td>النموذج يجد الأجسام لكنه يخطئ في تسميتها</td></tr>
<tr><td><code>dfl_loss</code></td>
    <td>دقة توزيع حدود الصندوق (Distribution Focal Loss)</td>
    <td>حواف الصناديق غير محسومة</td></tr>
</tbody>
</table>

<p>الفصل بينها مفيد عملياً: لو كانت <code>cls_loss</code> عالية و
<code>box_loss</code> منخفضة، فمشكلتك في التمييز بين الفئات لا في
تحديد المواقع، والحل يكون بمزيد من الأمثلة المتنوعة لكل فئة لا بتحسين
التوسيم.</p>

<h2>5.3 معدّل التعلّم Learning Rate والإحماء Warmup</h2>

<p>معدّل التعلّم يحدّد حجم الخطوة عند تعديل الأوزان:</p>

<ul>
<li><strong>كبير جداً</strong>: يقفز فوق الحل الأمثل، والخسارة تتذبذب أو
تنفجر.</li>
<li><strong>صغير جداً</strong>: يتعلّم ببطء شديد، وقد يعلق في حل رديء.</li>
</ul>

<p>في Fine-Tuning نستخدم معدّلاً <strong>أصغر</strong> من التدريب من
الصفر، لأننا نبدأ من أوزان جيدة ولا نريد تخريبها. القيمة الافتراضية في
Ultralytics <code>lr0=0.01</code> وهي مناسبة عادة.</p>

<p>و<strong>الإحماء</strong> (<code>warmup_epochs=3</code>) يبدأ بمعدّل
صغير جداً ويرفعه تدريجياً في أول عدة epochs. السبب أن الرأس Head مهيّأ
عشوائياً في البداية، فلو ضربناه بخطوة كبيرة فوراً لأفسد الأوزان الجيدة
القادمة من الـ Backbone.</p>

<h2>5.4 imgsz و batch وحدود الذاكرة</h2>

<p><code>imgsz</code> هو الحجم الذي تُصغَّر إليه كل صورة قبل دخولها
النموذج. أثره كبير على السرعة وعلى كشف الأجسام الصغيرة:</p>

<table>
<thead>
<tr><th>الوضع</th><th>imgsz</th><th>batch</th><th>ملاحظة</th></tr>
</thead>
<tbody>
<tr><td>معالج فقط، داخل الحصة</td><td>320</td><td>8</td>
    <td>ما سنستخدمه الآن. سريع، ودقته متواضعة</td></tr>
<tr><td>كرت شاشة 6 GB</td><td>640</td><td>16</td>
    <td>الوضع المتوازن المعتاد</td></tr>
<tr><td>كرت شاشة 12 GB أو أكثر</td><td>640</td><td>32</td>
    <td>أسرع، ونتائج أثبت</td></tr>
<tr><td>أجسام صغيرة وبعيدة</td><td>960</td><td>8</td>
    <td>ذاكرة أكبر بكثير وزمن أطول</td></tr>
</tbody>
</table>

<div class="note">
<p>إن ظهرت رسالة <code>CUDA out of memory</code> فالحل هو تصغير
<code>batch</code> أولاً، ثم تصغير <code>imgsz</code>. لاحظ أن
<code>imgsz</code> يجب أن يكون من مضاعفات 32.</p>
</div>

<p>وسيط بياناتنا يقول إن الأجسام تشغل نحو 12% من مساحة الصورة، وهي أجسام
كبيرة نسبياً، لذلك <code>imgsz=320</code> يكفي في الحصة ولن نخسر كثيراً.</p>

<h2>5.5 تجميد الطبقات Freezing</h2>

<p>يمكننا أن نمنع الطبقات الأولى من التعديل ونكتفي بتدريب الرأس:</p>

<pre><code>model.train(data=..., freeze=10)   # تجميد أول عشر طبقات</code></pre>

<ul>
<li><strong>متى يفيد؟</strong> حين تكون البيانات قليلة جداً (أقل من مئة
صورة)، أو حين نريد تدريباً أسرع بكثير على معالج ضعيف.</li>
<li><strong>متى يضرّ؟</strong> حين تختلف صورنا كثيراً عن ImageNet و COCO،
لأن الـ Backbone عندها يحتاج فعلاً أن يتكيّف.</li>
</ul>

<p>في حالتنا صور شوارع عادية، والـ Backbone مناسب أصلاً، فالتجميد خيار
معقول لتوفير الوقت. سنتركه مفتوحاً في التدريب الكامل، وستجرّبه أنت في
التمارين.</p>"""
)


# ===========================================================================
# 6. لنُدرّب
# ===========================================================================

rtl(
    """<hr />
<h1>6. لنُدرّب</h1>

<p>سنقوم بتدريبين مختلفين تماماً في الهدف:</p>

<ol>
<li><strong>تدريب مصغّر حي</strong> تشغّله الآن على معالج جهازك خلال بضع
دقائق. هدفه أن ترى الخسارة تنخفض بعينك وتفهم مجرى العملية.
<strong>نتيجته ستكون ضعيفة، وهذا مقصود.</strong></li>
<li><strong>تدريب كامل</strong> أُجري مسبقاً على كرت شاشة، ونتائجه مرفقة
في مجلد <code>runs_reference/</code>. عليه سنبني كل التحليل في القسم
السابع.</li>
</ol>

<h2>6.1 نبني قاعدة بيانات مصغّرة للحصة</h2>

<p>477 صورة على معالج ستأخذ وقتاً طويلاً. سنأخذ عيّنة صغيرة منها فقط.</p>"""
)

code(
    '''import random
import shutil

random.seed(7)

MINI_ROOT = Path("dataset_mini")
if MINI_ROOT.exists():
    shutil.rmtree(MINI_ROOT)

for split, n_images in [("train", MINI_TRAIN_IMAGES), ("valid", 30)]:
    source_images = sorted((Path("dataset") / split / "images").glob("*.jpg"))
    chosen = random.sample(source_images, min(n_images, len(source_images)))

    (MINI_ROOT / split / "images").mkdir(parents=True, exist_ok=True)
    (MINI_ROOT / split / "labels").mkdir(parents=True, exist_ok=True)

    for image_path in chosen:
        label_path = Path("dataset") / split / "labels" / (image_path.stem + ".txt")
        shutil.copy2(image_path, MINI_ROOT / split / "images" / image_path.name)
        shutil.copy2(label_path, MINI_ROOT / split / "labels" / label_path.name)

    print(f"{split}: نسخنا {len(chosen)} صورة")

# ملف إعداد خاص بالنسخة المصغّرة، بالقاعدة نفسها: بلا مفتاح path، فيصير
# مجلد هذا الملف هو الجذر.
(MINI_ROOT / "data.yaml").write_text(
    "train: train/images\\n"
    "val: valid/images\\n\\n"
    f"nc: {len(CLASS_NAMES)}\\n"
    f"names: {CLASS_NAMES}\\n"
)

print("\\nجاهز:", MINI_ROOT / "data.yaml")'''
)

rtl(
    """<h2>6.2 التدريب المصغّر</h2>

<p>الخلية التالية تدرّب فعلياً. على معالج بأربعة أنوية تستغرق نحو خمس
دقائق. راقب عمود <code>cls_loss</code>: هو الأوضح انخفاضاً، لأن مسألتنا
الأساسية هي تعليم النموذج <strong>اسماً جديداً</strong> لا تحسين دقة
صناديقه.</p>

<div class="note">
<p><code>amp=False</code> ضرورية هنا لسببين: الحساب نصف الدقة لا يعمل على
المعالج أصلاً، والأهم أن فحص AMP في Ultralytics يحاول تحميل نموذج من
الإنترنت، ونحن نعمل بلا اتصال.</p>
</div>"""
)

code(
    '''mini_model = YOLO(PRETRAINED_PATH)

mini_results = mini_model.train(
    data=str(MINI_ROOT / "data.yaml"),
    epochs=MINI_EPOCHS,
    imgsz=320,
    batch=MINI_BATCH,
    device=DEVICE,
    workers=0,
    amp=False,
    cache=False,
    plots=True,
    name="mini",
    exist_ok=True,
    seed=7,
)

# لا نخمّن مسار المخرجات، بل نسأل المدرِّب عنه. المسار يختلف بين إصدارات
# Ultralytics وبحسب إعداداتها المحلية.
MINI_RUN_DIR = Path(mini_model.trainer.save_dir)

print("\\nانتهى التدريب المصغّر.")
print("مخرجاته في:", MINI_RUN_DIR)'''
)

rtl(
    """<h2>6.3 ماذا تعني أرقام شريط التقدم؟</h2>

<p>أثناء التدريب رأيت سطراً يشبه هذا:</p>

<pre><code>  Epoch  GPU_mem  box_loss  cls_loss  dfl_loss  Instances  Size
    3/5       0G     1.842     2.104     1.203         21   320</code></pre>

<ul>
<li><code>3/5</code>: نحن في الدورة الثالثة من خمس.</li>
<li><code>box_loss</code> و <code>cls_loss</code> و <code>dfl_loss</code>:
الخسائر الثلاث التي شرحناها. <strong>يجب أن تنخفض مع الوقت.</strong></li>
<li><code>Instances</code>: عدد الأجسام في الـ batch الحالي، لا عدد
الصور.</li>
<li><code>Size</code>: حجم الصورة الداخل إلى النموذج، أي
<code>imgsz</code>.</li>
</ul>

<p>وبعد كل epoch يظهر سطر تقييم على مجموعة <code>valid</code> فيه
<code>Box(P R mAP50 mAP50-95)</code>، وهي المقاييس التي سنشرحها في القسم
التالي.</p>

<h2>6.4 نتيجة تدريبنا المصغّر</h2>"""
)

code(
    '''mini_history = pd.read_csv(MINI_RUN_DIR / "results.csv")
mini_history.columns = [c.strip() for c in mini_history.columns]

loss_columns = [c for c in mini_history.columns if "train/" in c and "loss" in c]

fig, axes = plt.subplots(1, 2, figsize=(14, 4.5))

for column in loss_columns:
    axes[0].plot(mini_history["epoch"], mini_history[column],
                 marker="o", label=column.replace("train/", ""))
axes[0].set_xlabel("epoch")
axes[0].set_ylabel("loss")
axes[0].set_title("Training losses (mini run)")
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].plot(mini_history["epoch"], mini_history["metrics/mAP50(B)"],
             marker="o", color="#2E7D32")
axes[1].set_xlabel("epoch")
axes[1].set_ylabel("mAP@50")
axes[1].set_title("Validation mAP@50 (mini run)")
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("mAP@50 بعد التدريب المصغّر:",
      round(float(mini_history["metrics/mAP50(B)"].iloc[-1]), 3))'''
)

rtl(
    """<div class="note">
<p><strong>هل انخفضت كل الخسائر؟ غالباً لا، وهذا طبيعي.</strong> سترى
<code>cls_loss</code> ينخفض بوضوح، بينما قد يرتفع <code>box_loss</code>
قليلاً في الدورات الأولى. السبب أن تعزيز <strong>Mosaic</strong> الذي
شرحناه في القسم الرابع يبني صوراً مركّبة أصعب بكثير من الصور الأصلية،
فيصبح ضبط الصناديق أصعب مؤقتاً قبل أن يتحسّن. في تدريب طويل يستقر
الاثنان معاً وينخفضان.</p>
<p><strong>المؤشر الأهم في تدريب قصير كهذا هو
<code>mAP@50</code></strong>: انظر هل ارتفع من الصفر. هذا وحده يكفي
دليلاً على أن النموذج بدأ يتعلّم الفئة الجديدة.</p>
</div>

<div class="note">
<p><strong>ولماذا النتيجة ضعيفة عموماً؟</strong> لأننا استخدمنا مئة صورة فقط، وخمس
دورات فقط، وحجم صورة 320 بدل 640. هذا ليس فشلاً بل هو حدود ما يمكن فعله
في دقائق على معالج. الغرض كان أن ترى الآلية تعمل: الخسارة تنخفض، والـ
mAP يرتفع من الصفر.</p>
<p>لتحصل على نموذج مفيد فعلاً نحتاج بيانات أكثر ودورات أكثر وحجم صورة
أكبر، وهذا ما فعلناه في التدريب المرجعي.</p>
</div>

<h2>6.5 التدريب الكامل</h2>

<p>الخلية التالية معطّلة بثابت. شغّلها في البيت إن كان لديك كرت شاشة
NVIDIA. تستغرق نحو نصف ساعة.</p>"""
)

code(
    '''RUN_FULL_TRAINING = False   # اجعلها True إن كان لديك كرت شاشة NVIDIA

if RUN_FULL_TRAINING:
    full_model = YOLO(PRETRAINED_PATH)

    full_model.train(
        data=DATA_YAML,
        epochs=60,
        imgsz=640,
        batch=16,
        device=DEVICE,
        workers=4,
        amp=True,
        patience=15,
        plots=True,
        name="emergency_full",
        exist_ok=True,
        seed=7,
    )

    print("مخرجات التدريب الكامل في:", full_model.trainer.save_dir)
else:
    print("التدريب الكامل معطّل.")
    print("سنستخدم النتائج المرفقة في", REFERENCE_RUN)'''
)

rtl(
    """<h2>6.6 النتائج المرجعية المرفقة</h2>

<p>مجلد <code>runs_reference/emergency_full/</code> يحوي مخرجات تدريب كامل
أجريناه مسبقاً على كامل قاعدة البيانات. سنعتمد عليه في كل التحليل التالي.</p>"""
)

code(
    '''for item in sorted(REFERENCE_RUN.rglob("*")):
    if item.is_file():
        size_kb = item.stat().st_size / 1024
        print(f"{str(item.relative_to(REFERENCE_RUN)):38s} {size_kb:8.1f} KB")'''
)


# ===========================================================================
# 7. التقييم
# ===========================================================================

rtl(
    """<hr />
<h1>7. قراءة النتائج والتقييم</h1>

<div class="note">
<p><strong>تنبيه مهم:</strong> كل الأرقام في هذا القسم تأتي من
<strong>التدريب الكامل المرجعي</strong> الذي أُجري مسبقاً على كرت شاشة،
لا من تدريبك المصغّر قبل قليل. تدريبك المصغّر سيعطي أرقاماً أقل بكثير،
وهذا متوقع.</p>
</div>

<h2>7.1 مراجعة سريعة: IoU</h2>

<p>قبل أي مقياس، نحتاج أن نقرّر متى نعتبر صندوقاً متوقَّعاً
<strong>صحيحاً</strong>. المعيار هو <strong>IoU</strong>، أي نسبة التقاطع
إلى الاتحاد بين الصندوق المتوقَّع والصندوق الحقيقي.</p>

<p>القيمة تتراوح بين صفر وواحد، والعتبة الشائعة <code>0.5</code>: إن كان
التقاطع نصف الاتحاد أو أكثر فالكشف صحيح.</p>"""
)

code(
    '''def intersection_over_union(box_a, box_b):
    """كل صندوق بصيغة (x1, y1, x2, y2)."""
    inter_x1 = max(box_a[0], box_b[0])
    inter_y1 = max(box_a[1], box_b[1])
    inter_x2 = min(box_a[2], box_b[2])
    inter_y2 = min(box_a[3], box_b[3])

    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)

    area_a = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
    area_b = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
    union_area = area_a + area_b - inter_area

    return inter_area / union_area if union_area > 0 else 0.0


ground_truth = (100, 100, 300, 250)

for name, prediction in [
    ("مطابق تماماً", (100, 100, 300, 250)),
    ("إزاحة بسيطة", (110, 108, 305, 258)),
    ("إزاحة كبيرة", (180, 150, 380, 300)),
    ("بعيد تماماً", (320, 260, 480, 380)),
]:
    score = intersection_over_union(ground_truth, prediction)
    verdict = "مقبول" if score >= 0.5 else "مرفوض"
    print(f"{name:14s} IoU = {score:.2f}  ->  {verdict}")'''
)

rtl(
    """<h2>7.2 TP و FP و FN ثم Precision و Recall</h2>

<p>بعد تطبيق عتبة IoU يصبح كل كشف واحداً من ثلاثة:</p>

<ul>
<li><strong>TP</strong> (True Positive): كشف صحيح طابق جسماً حقيقياً.</li>
<li><strong>FP</strong> (False Positive): كشف على لا شيء، أو بفئة خاطئة.
إنذار كاذب.</li>
<li><strong>FN</strong> (False Negative): جسم حقيقي لم يكشفه النموذج.
فوّتناه.</li>
</ul>

<p>ومنها مقياسان:</p>

<ul>
<li><strong>Precision</strong> = TP / (TP + FP)
  — «مما أعلنتُ عنه، كم كان صحيحاً؟»</li>
<li><strong>Recall</strong> = TP / (TP + FN)
  — «مما كان موجوداً فعلاً، كم وجدتُ؟»</li>
</ul>

<p>بينهما مقايضة دائمة: خفض <code>conf</code> يرفع الـ Recall ويخفض الـ
Precision، ورفعه يفعل العكس. وهذا بالضبط ما جرّبناه في الأسبوع الماضي.</p>

<div class="note">
<p><strong>في نظامنا أيهما أهم؟</strong> إن فاتنا إسعاف
(<strong>FN</strong>) فلن تُفتح له الإشارة وقد يتأخر عن حالة طارئة. وإن
أطلقنا إنذاراً كاذباً (<strong>FP</strong>) فسنعطّل حركة المرور بلا سبب.
الخطأ الأول أخطر، لذلك سنميل إلى <strong>Recall</strong> أعلى ونتحمّل
بعض الإنذارات الكاذبة.</p>
</div>"""
)

figure(8, "tp_fp_fn.jpg")

rtl(
    """<h2>7.3 منحنى PR و mAP</h2>

<p>مشكلة Precision و Recall أن كلاً منهما يعتمد على عتبة
<code>conf</code> التي اخترناها. فأي قيمة نُبلغ عنها؟</p>

<p>الحل أن نجرّب <strong>كل</strong> العتبات ونرسم Precision مقابل Recall،
فنحصل على <strong>منحنى PR</strong>. والمساحة تحت هذا المنحنى هي
<strong>Average Precision (AP)</strong> لتلك الفئة. ومتوسط AP على كل
الفئات هو <strong>mAP</strong>.</p>

<ul>
<li><strong>mAP@50</strong>: بعتبة IoU واحدة هي 0.5. متساهل نسبياً، يقيس
أساساً «هل وجدت الجسم وسمّيته صحيحاً؟»</li>
<li><strong>mAP@50-95</strong>: متوسط عشر عتبات من 0.50 إلى 0.95. أقسى
بكثير، ويكافئ دقة الصندوق لا مجرد إيجاد الجسم. هذا هو الرقم الذي يُنشر
في الأبحاث.</li>
</ul>

<p>ستكون <code>mAP@50-95</code> دائماً أقل من <code>mAP@50</code>. لا
تقارن رقماً من نوع برقم من نوع آخر.</p>"""
)

figure(9, "pr_curve_map.jpg")

rtl(
    """<h2>7.4 كيف نقرأ results.png</h2>

<p>تنتج Ultralytics بعد كل تدريب صورة تلخّص المسيرة كاملة. لنعرضها من
التدريب المرجعي:</p>"""
)

code(
    '''from IPython.display import Image as IPImage

IPImage(str(REFERENCE_RUN / "results.png"), width=1100)'''
)

rtl(
    """<p>الصورة عشر لوحات. اقرأها هكذا:</p>

<ul>
<li><strong>الصف العلوي</strong>: خسائر التدريب الثلاث
(<code>train/box_loss</code>, <code>cls_loss</code>, <code>dfl_loss</code>)
ثم مقياسا <code>precision</code> و <code>recall</code>.</li>
<li><strong>الصف السفلي</strong>: الخسائر الثلاث نفسها لكن على مجموعة
<code>valid</code>، ثم <code>mAP50</code> و <code>mAP50-95</code>.</li>
</ul>

<p>ما تبحث عنه:</p>

<ol>
<li>خسائر التدريب تنخفض بسلاسة ← معدّل التعلّم مناسب.</li>
<li>خسائر <code>valid</code> تنخفض معها ← النموذج يعمّم لا يحفظ.</li>
<li>منحنيات mAP ترتفع ثم تستوي ← اقتربنا من حدود البيانات الحالية.</li>
<li>لو ارتفعت خسارة <code>valid</code> بينما تواصل خسارة التدريب الانخفاض
← هذا هو <strong>Overfitting</strong> بعينه.</li>
</ol>

<p>ولنقرأ الأرقام النهائية مباشرة من الملف:</p>"""
)

code(
    '''reference_history = pd.read_csv(REFERENCE_RUN / "results.csv")
reference_history.columns = [c.strip() for c in reference_history.columns]

final = reference_history.iloc[-1]

print(f"عدد الدورات المنفَّذة : {int(final['epoch'])}")
print(f"Precision          : {final['metrics/precision(B)']:.3f}")
print(f"Recall             : {final['metrics/recall(B)']:.3f}")
print(f"mAP@50             : {final['metrics/mAP50(B)']:.3f}")
print(f"mAP@50-95          : {final['metrics/mAP50-95(B)']:.3f}")

best_epoch = int(reference_history["metrics/mAP50-95(B)"].idxmax()) + 1
print(f"\\nأفضل دورة حسب mAP@50-95 : {best_epoch}")
print("وهي الدورة المحفوظة في best.pt")'''
)

rtl(
    """<h2>7.5 مصفوفة الالتباس Confusion Matrix</h2>

<p>الـ mAP رقم واحد يلخّص كل شيء، وهذا عيبه: لا يخبرنا <strong>أين</strong>
يخطئ النموذج. مصفوفة الالتباس تجيب عن ذلك.</p>"""
)

code(
    '''IPImage(str(REFERENCE_RUN / "confusion_matrix_normalized.png"), width=850)'''
)

figure(10, "confusion_matrix_guide.jpg")

rtl(
    """<p>الأسئلة التي تجيب عنها المصفوفة:</p>

<ul>
<li><strong>القطر</strong>: نسبة الإصابة لكل فئة. كلما اقترب من 1 كان
أفضل.</li>
<li><strong>خلية خارج القطر</strong>: التبس على النموذج بين فئتين. راقب
خانة <code>ambulance</code> مقابل <code>truck</code> بالذات، فهي الخطأ
الذي بدأنا منه الدرس.</li>
<li><strong>عمود background</strong>: أجسام حقيقية لم يكشفها النموذج
إطلاقاً، أي FN.</li>
<li><strong>صف background</strong>: صناديق رسمها النموذج على خلفية فارغة،
أي FP.</li>
</ul>

<h2>7.6 هل عندنا Overfitting؟</h2>

<p><strong>Overfitting</strong> أن يحفظ النموذج صور التدريب بدل أن يتعلّم
منها قاعدة عامة. علاماته:</p>

<ul>
<li>خسارة التدريب تواصل الانخفاض، وخسارة <code>valid</code> تتوقف ثم
ترتفع.</li>
<li>فجوة كبيرة ومتّسعة بين أداء <code>train</code> و <code>valid</code>.</li>
<li>أداء ممتاز على بياناتك وفشل ذريع على أي صورة جديدة.</li>
</ul>

<p>وعلاجه بالترتيب العملي:</p>

<ol>
<li><strong>بيانات أكثر وأكثر تنوّعاً</strong> — الحل الأقوى دائماً.</li>
<li><strong>تعزيز أقوى</strong> — أرخص وأسرع من جمع بيانات.</li>
<li><strong>إيقاف مبكر</strong> (<code>patience</code>) — Ultralytics
تفعله تلقائياً وتحفظ أفضل نسخة في <code>best.pt</code>.</li>
<li><strong>تجميد طبقات</strong> (<code>freeze</code>) — يقلّل عدد
الأوزان القابلة للتعديل.</li>
<li><strong>نموذج أصغر</strong> — <code>yolo11n</code> بدل
<code>yolo11s</code>.</li>
</ol>"""
)

figure(11, "overfitting_curves.jpg")

rtl(
    """<p>ولنفحص منحنياتنا نحن: هل الفجوة بين التدريب والتحقق تتّسع؟</p>"""
)

code(
    '''fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(reference_history["epoch"], reference_history["train/box_loss"],
        label="train/box_loss", color="#1565C0", linewidth=2)
ax.plot(reference_history["epoch"], reference_history["val/box_loss"],
        label="val/box_loss", color="#F9A825", linewidth=2)

ax.set_xlabel("epoch")
ax.set_ylabel("box loss")
ax.set_title("Train vs validation loss - are they drifting apart?")
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()
plt.show()

gap_start = float(reference_history["val/box_loss"].iloc[0]
                  - reference_history["train/box_loss"].iloc[0])
gap_end = float(reference_history["val/box_loss"].iloc[-1]
                - reference_history["train/box_loss"].iloc[-1])

print(f"الفجوة في البداية : {gap_start:.3f}")
print(f"الفجوة في النهاية : {gap_end:.3f}")
print("الفجوة تتّسع، وهي علامة تجهيز زائد."
      if gap_end > gap_start else "الفجوة مستقرة، والوضع سليم.")'''
)


# ===========================================================================
# 8. قبل وبعد
# ===========================================================================

rtl(
    """<hr />
<h1>8. اللحظة الحاسمة: قبل وبعد</h1>

<p>نعود الآن إلى صور القسم الأول نفسها، تلك التي سمّى فيها النموذج الجاهز
سيارة الإسعاف <code>truck</code> بثقة تجاوزت 0.90. لنشغّل عليها النموذجين
جنباً إلى جنب.</p>"""
)

code(
    '''finetuned_model = YOLO("models/emergency_best.pt")

n_failures = len(failures_df)
fig, axes = plt.subplots(2, n_failures, figsize=(4.2 * n_failures, 9))

for column, (_, item) in enumerate(failures_df.iterrows()):
    image_path = f"failures/{item['file']}"

    before = pretrained_model.predict(
        source=image_path, conf=0.35, device=DEVICE, verbose=False
    )[0]
    after = finetuned_model.predict(
        source=image_path, conf=0.35, device=DEVICE, verbose=False
    )[0]

    axes[0, column].imshow(cv2.cvtColor(before.plot(), cv2.COLOR_BGR2RGB))
    axes[0, column].axis("off")

    axes[1, column].imshow(cv2.cvtColor(after.plot(), cv2.COLOR_BGR2RGB))
    axes[1, column].axis("off")

axes[0, 0].set_ylabel("BEFORE")
axes[1, 0].set_ylabel("AFTER")

fig.text(0.5, 0.97, "Before: pretrained yolo11n (COCO, 80 classes)",
         ha="center", fontsize=15)
fig.text(0.5, 0.49, "After: fine-tuned on our 4 classes",
         ha="center", fontsize=15)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()'''
)

rtl(
    """<p>والآن الأرقام. نقيّم النموذج المدرَّب على مجموعة
<code>test</code> التي لم يرَها إطلاقاً أثناء التدريب:</p>"""
)

code(
    '''metrics = finetuned_model.val(
    data=DATA_YAML,
    split="test",
    imgsz=640,
    device=DEVICE,
    verbose=False,
)

per_class = []
for index, class_id in enumerate(metrics.ap_class_index):
    per_class.append({
        "الفئة": CLASS_NAMES[class_id],
        "Precision": round(float(metrics.box.p[index]), 3),
        "Recall": round(float(metrics.box.r[index]), 3),
        "mAP@50": round(float(metrics.box.ap50[index]), 3),
        "mAP@50-95": round(float(metrics.box.ap[index]), 3),
    })

results_table = pd.DataFrame(per_class)
print(results_table.to_string(index=False))
print()
print(f"المتوسط العام mAP@50    : {metrics.box.map50:.3f}")
print(f"المتوسط العام mAP@50-95 : {metrics.box.map:.3f}")'''
)

rtl(
    """<div class="note">
<p><strong>لماذا لا نضع جدولاً مقابلاً للنموذج الجاهز؟</strong> لأن
المقارنة العددية المباشرة مستحيلة أصلاً، وهذا هو بيت القصيد: النموذج
الجاهز لا يملك فئة <code>ambulance</code>، فقيمة
<code>mAP</code> له على هذه الفئة تساوي <strong>صفراً بالتعريف</strong>،
لا لأنه سيّئ بل لأن السؤال خارج قاموسه تماماً.</p>
<p>هذا هو الفرق بين «نموذج ضعيف» و«نموذج لا يستطيع التعبير عن المسألة».
والتدريب هو الطريق الوحيد من الثاني إلى الأول.</p>
</div>

<p>لاحظ أيضاً أن النموذج ما زال يكشف <code>car</code> و <code>truck</code>
و <code>bus</code>. لم نخسر شيئاً، بل أضفنا فئة رابعة يحتاجها نظامنا.</p>

<h2>لماذا فئة ambulance هي الأفضل والبقية أضعف؟</h2>

<p>النتيجة قد تبدو غريبة للوهلة الأولى: الفئة <strong>الجديدة</strong> التي
كنا نظن أنها الأصعب هي الأعلى نتيجةً، بينما <code>car</code> وهي فئة
عادية جداً جاءت الأضعف. والسبب ليس في النموذج بل في
<strong>بياناتنا</strong>:</p>

<ol>
<li><strong>عدد الأمثلة.</strong> جمعنا الصور انطلاقاً من سيارات الإسعاف،
فصارت <code>ambulance</code> أكثر الفئات صناديقَ بفارق كبير. أما
<code>car</code> فظهرت عرضاً في الخلفيات.</li>
<li><strong>التمايز البصري.</strong> سيارة الإسعاف بيضاء غالباً، عالية،
عليها علامات وأضواء مميزة. أما «سيارة» فصنف واسع جداً يضم أشكالاً
وألواناً لا تُحصى.</li>
<li><strong>التوسيم غير الشامل.</strong> وهذا أهم سبب وأخطره. مجموعة
Open Images <strong>لا توسّم كل جسم في كل صورة</strong>. في مجموعة
الاختبار لدينا 23 سيارة موسومة فقط، بينما يجد النموذج الجاهز 37 سيارة
حقيقية. أي أن نحو ثلث السيارات موجود في الصور وغير موسوم.</li>
</ol>

<div class="note">
<p><strong>وماذا يعني ذلك؟</strong> حين يكشف نموذجنا سيارةً حقيقية لم
يوسّمها أحد، يحسبها التقييم <strong>إنذاراً كاذباً</strong>
(<code>FP</code>) ويعاقب النموذج على إجابة صحيحة. فالرقم المنخفض لفئة
<code>car</code> يقيس نقص التوسيم أكثر مما يقيس ضعف النموذج.</p>
<p>هذا درس عملي مهم: <strong>المقياس لا يكون أصدق من البيانات التي
يُحسب عليها.</strong> قبل أن تلوم نموذجك على رقم منخفض، افتح الصور وانظر
هل التوسيم نفسه سليم وشامل.</p>
</div>

<p>ولهذا نقول إن الرقم الذي يهمّنا فعلاً في هذا الدرس هو
<code>mAP@50</code> لفئة <code>ambulance</code>: هي الفئة التي جمعنا
البيانات من أجلها، وهي الوحيدة الموسّمة توسيماً شاملاً، وهي التي يقوم
عليها نظام الأولوية في الأسبوع التاسع.</p>"""
)


# ===========================================================================
# 9-11
# ===========================================================================

rtl(
    """<hr />
<h1>9. دليل التحسين حين تكون النتائج ضعيفة</h1>

<p>لن يكون تدريبك الأول جيداً غالباً. هذا الجدول يربط العَرَض بالسبب
المحتمل بالإجراء:</p>

<table>
<thead>
<tr><th>العَرَض</th><th>السبب المحتمل</th><th>الإجراء</th></tr>
</thead>
<tbody>
<tr><td>الخسارة لا تنخفض إطلاقاً</td>
    <td>خطأ في مسارات البيانات أو التوسيم</td>
    <td>افحص <code>labels.jpg</code>: هل الصناديق في مواضعها؟</td></tr>
<tr><td>الخسارة تنفجر أو تصبح NaN</td>
    <td>معدّل التعلّم كبير</td>
    <td>خفّض <code>lr0</code> إلى 0.001</td></tr>
<tr><td>mAP مرتفع للتدريب ومنخفض للتحقق</td>
    <td>تجهيز زائد Overfitting</td>
    <td>بيانات أكثر، تعزيز أقوى، <code>freeze</code></td></tr>
<tr><td>فئة واحدة أداؤها سيّئ وحدها</td>
    <td>أمثلتها قليلة أو توسيمها غير متسق</td>
    <td>أضف صوراً لها، وراجع توسيمها</td></tr>
<tr><td>Recall منخفض والـ Precision مرتفع</td>
    <td>النموذج متحفّظ جداً</td>
    <td>خفّض <code>conf</code>، وأضف أمثلة صعبة</td></tr>
<tr><td>Precision منخفض والـ Recall مرتفع</td>
    <td>إنذارات كاذبة كثيرة</td>
    <td>ارفع <code>conf</code>، وأضف صوراً سلبية</td></tr>
<tr><td>يفشل على الأجسام الصغيرة فقط</td>
    <td><code>imgsz</code> صغير</td>
    <td>ارفعه إلى 960 مع تصغير <code>batch</code></td></tr>
<tr><td>ممتاز على بياناتك وسيّئ في الواقع</td>
    <td>اختلاف المجال Domain Shift</td>
    <td>اجمع صوراً من الكاميرا الحقيقية نفسها</td></tr>
<tr><td>الفئتان تلتبسان دائماً</td>
    <td>الفئتان متشابهتان بصرياً فعلاً</td>
    <td>أعد التفكير: هل يجب فصلهما أصلاً؟</td></tr>
<tr><td>النتائج تتغيّر كل مرة</td>
    <td>لم تثبّت البذرة العشوائية</td>
    <td>مرّر <code>seed</code> ثابتاً</td></tr>
</tbody>
</table>

<hr />
<h1>10. حفظ النموذج واستخدامه لاحقاً</h1>

<p>ينتج التدريب ملفين في <code>runs/&lt;name&gt;/weights/</code>:</p>

<ul>
<li><code>best.pt</code>: أفضل نسخة حسب أداء <code>valid</code>.
<strong>هذا ما تستخدمه دائماً.</strong></li>
<li><code>last.pt</code>: آخر دورة. يفيد فقط لمتابعة تدريب انقطع.</li>
</ul>"""
)

code(
    '''saved_model_path = Path("models/emergency_best.pt")

print("حجم ملف النموذج:", round(saved_model_path.stat().st_size / 1e6, 1), "MB")
print()

# الملف يحمل معه أسماء الفئات، فلا تحتاج data.yaml عند الاستخدام
loaded = YOLO(str(saved_model_path))
print("الفئات المحفوظة داخل النموذج:", loaded.names)'''
)

rtl(
    """<p>لتشغيله في مشروع آخر لا تحتاج إلا هذا الملف:</p>

<pre><code>from ultralytics import YOLO

model = YOLO("emergency_best.pt")
results = model.predict("street.jpg", conf=0.35)</code></pre>

<p>ولنشره على أجهزة صغيرة أو خوادم، يمكن تصديره إلى صيغ أخرى مثل
<strong>ONNX</strong> عبر <code>model.export(format="onnx")</code>، وهي
صيغة تعمل بلا PyTorch وأسرع على المعالج. لن نحتاجها في هذا المسار، لكن
اعرف أنها موجودة.</p>

<div class="note">
<p>احفظ <code>emergency_best.pt</code> في مكان آمن. سنستخدمه في الأسبوع
القادم لتتبّع سيارات الإسعاف عبر إطارات الفيديو.</p>
</div>

<hr />
<h1>11. حدود ما فعلناه</h1>

<p>من الأمانة العلمية أن نعرف حدود نموذجنا قبل أن نثق به:</p>

<ul>
<li><strong>قاعدة البيانات صغيرة.</strong> 682 صورة فقط، منها نحو 400
فيها إسعاف. النماذج الإنتاجية تُدرَّب على عشرات الآلاف.</li>
<li><strong>تحيّز جغرافي.</strong> معظم الصور من أوروبا وأمريكا الشمالية.
سيارات الإسعاف عندنا قد تختلف شكلاً ولوناً وعلامات، وأداء النموذج عليها
سيكون أضعف مما تُظهره أرقامنا.</li>
<li><strong>اختلاف المجال.</strong> صورنا لقطات فوتوغرافية من مستوى
الأرض، بينما كاميرا المرور مثبّتة على عمود عالٍ وبزاوية مختلفة وجودة
أقل.</li>
<li><strong>ظروف ناقصة.</strong> الصور نهارية في معظمها. الليل والمطر
والضباب ممثَّلة تمثيلاً ضعيفاً.</li>
<li><strong>مجموعة اختبار صغيرة.</strong> 69 صورة تعني أن أرقامنا تحمل
هامش خطأ واسعاً. لا تعامل الفرق بين 0.82 و 0.85 كفرق حقيقي.</li>
</ul>

<div class="note">
<p><strong>بُعد يتجاوز التقنية:</strong> نظام يقرّر فتح إشارة مرور بناءً
على كشف بصري يمسّ سلامة الناس. الخطأ فيه ليس رقماً في جدول: تفويت إسعاف
قد يعني تأخيراً في حالة حرجة، وإنذار كاذب متكرر قد يدفع الناس إلى تجاهل
النظام كله. أي نظام حقيقي من هذا النوع يحتاج مراقبة بشرية، وآلية تجاوز
يدوي، واختباراً ميدانياً طويلاً قبل أن يُعتمد عليه.</p>
</div>"""
)


# ===========================================================================
# 12-15
# ===========================================================================

rtl(
    """<hr />
<h1>12. تمرين صفي</h1>

<h3>المهمة 1: أثر عدد الدورات</h3>
<p>أعد التدريب المصغّر بـ <code>epochs=10</code> بدل 5. سجّل
<code>mAP@50</code> في الحالتين. هل تضاعفت النتيجة بمضاعفة الدورات؟ ولماذا
في رأيك؟</p>

<h3>المهمة 2: تجميد الطبقات</h3>
<p>أضف <code>freeze=10</code> إلى خلية التدريب المصغّر. قارن زمن التدريب
والنتيجة النهائية. متى يكون هذا التنازل مقبولاً؟</p>

<h3>المهمة 3: افحص توسيمك بعينك</h3>
<p>اختر عشر صور من <code>dataset/train/images</code> واعرض صناديقها. هل
تجد صندوقاً خاطئاً أو ناقصاً أو أوسع من جسمه؟ سجّل ما تجد.</p>

<h3>المهمة 4: صورك أنت</h3>
<p>ضع صورة فيها مركبة في مجلد <code>student_images/</code>، وشغّل عليها
النموذجين. اشرح الفرق بينهما بجملتين.</p>"""
)

code(
    '''# TODO:
# 1. غيّر القيم التالية
# 2. أعد بناء قاعدة البيانات المصغّرة إن لزم
# 3. شغّل التدريب وسجّل النتيجة
# 4. قارنها بنتيجتك الأولى

STUDENT_EPOCHS = 10
STUDENT_FREEZE = None      # جرّب 10
STUDENT_IMGSZ = 320

# اكتب الحل هنا'''
)

code(
    '''# المهمة 4: شغّل النموذجين على صورك أنت
student_images = sorted(Path("student_images").glob("*.jpg"))

if not student_images:
    print("ضع صورة أو أكثر في مجلد student_images/ ثم أعد تشغيل هذه الخلية.")
else:
    for image_path in student_images[:3]:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        for ax, (title, model) in zip(
            axes, [("Pretrained", pretrained_model),
                   ("Fine-tuned", finetuned_model)]
        ):
            result = model.predict(
                source=str(image_path), conf=0.35, device=DEVICE, verbose=False
            )[0]
            ax.imshow(cv2.cvtColor(result.plot(), cv2.COLOR_BGR2RGB))
            ax.set_title(title, fontsize=14)
            ax.axis("off")

        plt.suptitle(image_path.name, fontsize=15)
        plt.tight_layout()
        plt.show()'''
)

rtl(
    """<hr />
<h1>13. أسئلة مراجعة سريعة</h1>

<h3>سؤال 1</h3>
<p>لماذا لا يمكن لضبط <code>conf</code> أن يجعل النموذج الجاهز يكشف
سيارة إسعاف؟</p>

<h3>سؤال 2</h3>
<p>ما الفرق بين تسمية على مستوى الصورة وتسمية على مستوى الجسم؟ وأيهما
يلزم لتدريب كاشف؟</p>

<h3>سؤال 3</h3>
<p>في السطر <code>0 0.48 0.61 0.18 0.27</code>، ماذا يمثّل كل رقم؟ ولماذا
كل القيم أصغر من واحد؟</p>

<h3>سؤال 4</h3>
<p>لماذا يُعد وضع إطارات متتالية من فيديو واحد في <code>train</code> و
<code>valid</code> معاً خطأً فادحاً؟</p>

<h3>سؤال 5</h3>
<p>نموذج Precision له 0.95 و Recall 0.40. صف سلوكه بكلماتك. وهل يصلح
لنظام أولوية الإسعاف؟</p>

<h3>سؤال 6</h3>
<p>ما الفرق بين <code>mAP@50</code> و <code>mAP@50-95</code>؟ ولماذا
الثاني أقل دائماً؟</p>

<h3>سؤال 7</h3>
<p>خسارة التدريب تنخفض وخسارة التحقق ترتفع. ما التشخيص؟ واذكر علاجين.</p>"""
)

rtl(
    """<hr />
<h1>14. بنك أسئلة Kahoot</h1>

<div class="note">
<p>هذه الأسئلة جاهزة للنسخ إلى Kahoot. الحدود المسموحة في المنصة: نص
السؤال حتى 120 حرفاً، وكل خيار حتى 75 حرفاً، وأربعة خيارات، وإجابة صحيحة
واحدة.</p>
</div>

<h3>سؤال 1</h3>
<p><strong>السؤال:</strong> ما الذي لا يمكن حلّه بضبط قيمة Confidence
وحدها؟</p>
<ul>
<li>أ) كثرة الإنذارات الخاطئة</li>
<li>ب) عدم وجود فئة ambulance في النموذج</li>
<li>ج) فقدان الأجسام البعيدة</li>
<li>د) بطء المعالجة</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 2</h3>
<p><strong>السؤال:</strong> كم رقماً في كل سطر من ملف توسيم YOLO؟</p>
<ul>
<li>أ) ثلاثة</li>
<li>ب) أربعة</li>
<li>ج) خمسة</li>
<li>د) ستة</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ج</p>

<h3>سؤال 3</h3>
<p><strong>السؤال:</strong> إحداثيات صيغة YOLO مكتوبة بأي وحدة؟</p>
<ul>
<li>أ) بالبكسل</li>
<li>ب) بالسنتيمتر</li>
<li>ج) نسبة مطبَّعة بين 0 و 1</li>
<li>د) بالنسبة المئوية من 0 إلى 100</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ج</p>

<h3>سؤال 4</h3>
<p><strong>السؤال:</strong> ما دور مجموعة valid أثناء التدريب؟</p>
<ul>
<li>أ) يتعلّم منها النموذج ويعدّل أوزانه</li>
<li>ب) تختار أفضل دورة وتكشف التجهيز الزائد</li>
<li>ج) تزيد عدد صور التدريب</li>
<li>د) لا دور لها، للزينة فقط</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 5</h3>
<p><strong>السؤال:</strong> ماذا يعني أن خسارة التدريب تنخفض وخسارة
التحقق ترتفع؟</p>
<ul>
<li>أ) تجهيز زائد Overfitting</li>
<li>ب) تجهيز ناقص Underfitting</li>
<li>ج) التدريب مثالي</li>
<li>د) معدّل التعلّم صغير جداً</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> أ</p>

<h3>سؤال 6</h3>
<p><strong>السؤال:</strong> Precision تجيب عن أي سؤال؟</p>
<ul>
<li>أ) مما كان موجوداً، كم وجدت؟</li>
<li>ب) مما أعلنت عنه، كم كان صحيحاً؟</li>
<li>ج) كم صورة عالجت في الثانية؟</li>
<li>د) كم فئة يعرف النموذج؟</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 7</h3>
<p><strong>السؤال:</strong> في نظام أولوية الإسعاف، أي خطأ أخطر؟</p>
<ul>
<li>أ) إنذار كاذب FP</li>
<li>ب) تفويت إسعاف حقيقي FN</li>
<li>ج) صندوق غير دقيق</li>
<li>د) بطء بسيط في المعالجة</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 8</h3>
<p><strong>السؤال:</strong> لماذا mAP@50-95 أقل دائماً من mAP@50؟</p>
<ul>
<li>أ) يستخدم صوراً أقل</li>
<li>ب) يشترط عتبات IoU أقسى</li>
<li>ج) يتجاهل بعض الفئات</li>
<li>د) خطأ في الحساب</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 9</h3>
<p><strong>السؤال:</strong> ما أقوى تعزيز تطبّقه Ultralytics تلقائياً؟</p>
<ul>
<li>أ) Mosaic</li>
<li>ب) القلب الرأسي</li>
<li>ج) التدوير 90 درجة</li>
<li>د) تحويل الصورة لرمادية</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> أ</p>

<h3>سؤال 10</h3>
<p><strong>السؤال:</strong> ماذا يحدث لو غيّرت ترتيب names في data.yaml
بعد التوسيم؟</p>
<ul>
<li>أ) لا شيء، الأسماء للعرض فقط</li>
<li>ب) كل ملفات التوسيم تصبح خاطئة</li>
<li>ج) يصبح التدريب أسرع</li>
<li>د) تظهر رسالة خطأ واضحة</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 11</h3>
<p><strong>السؤال:</strong> أي ملف تستخدمه بعد انتهاء التدريب؟</p>
<ul>
<li>أ) last.pt</li>
<li>ب) best.pt</li>
<li>ج) data.yaml</li>
<li>د) results.csv</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 12</h3>
<p><strong>السؤال:</strong> لماذا نجح التدريب على مئات الصور فقط؟</p>
<ul>
<li>أ) لأن المسألة سهلة جداً</li>
<li>ب) لأننا بدأنا من أوزان مدرَّبة مسبقاً</li>
<li>ج) لأن الصور عالية الدقة</li>
<li>د) لأننا استخدمنا معالجاً سريعاً</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>"""
)

rtl(
    """<hr />
<h1>15. الخلاصة</h1>

<p>ما فعلناه في هذا الدرس:</p>

<ul>
<li>أثبتنا أن النموذج الجاهز <strong>يفشل فشلاً واثقاً</strong>: كشف
سيارة الإسعاف بثقة تجاوزت 0.90 وسمّاها <code>truck</code>، لأن الفئة
غير موجودة في قاموسه أصلاً.</li>
<li>ميّزنا بين <strong>فجوة الفئات</strong> التي لا يصلحها إلا التدريب،
و<strong>اختلاف المجال</strong> الذي قد تخفّفه العتبات.</li>
<li>فهمنا أن <strong>Fine-Tuning</strong> يعيد استخدام نحو 99% من الأوزان
ولا يستبدل إلا الرأس، ولهذا تكفيه مئات الصور لا ملايينها.</li>
<li>تعلّمنا صيغة توسيم YOLO وكتبناها بأيدينا، وبنينا بنية المجلدات وملف
<code>data.yaml</code>، وقسّمنا البيانات تقسيماً نزيهاً.</li>
<li>درّبنا فعلياً، وقرأنا الخسائر الثلاث ومنحنيات النتائج ومصفوفة
الالتباس، وشخّصنا التجهيز الزائد.</li>
<li>حصلنا على نموذج يعرف <code>ambulance</code> إلى جانب
<code>car</code> و <code>truck</code> و <code>bus</code>.</li>
</ul>

<h2>في الأسبوع القادم</h2>

<p>نموذجنا الآن يجيب عن سؤالَي «ما هذا؟» و«أين هو؟» في كل إطار على حدة.
لكنه <strong>ينسى كل شيء بين إطار وإطار</strong>: لا يعرف أن الإسعاف الذي
رآه في الإطار العاشر هو نفسه الذي رآه في الإطار التاسع.</p>

<p>ولهذا لا نستطيع بعد أن نجيب عن أسئلة بسيطة مثل: كم مركبة عبرت
التقاطع؟ وبأي سرعة يقترب هذا الإسعاف؟</p>

<p>حلّ ذلك هو <strong>التتبّع Object Tracking</strong>: أن نعطي كل جسم
رقماً ثابتاً يلازمه عبر الإطارات. وهذا موضوع الأسبوع الثامن.</p>

<hr />
<h2>مصادر للاستزادة</h2>

<ul>
<li><a href="https://docs.ultralytics.com/modes/train/">Ultralytics — Train</a></li>
<li><a href="https://docs.ultralytics.com/modes/val/">Ultralytics — Validate</a></li>
<li><a href="https://docs.ultralytics.com/datasets/detect/">Ultralytics — تنسيق قواعد بيانات الكشف</a></li>
<li><a href="https://docs.ultralytics.com/guides/yolo-performance-metrics/">Ultralytics — شرح مقاييس الأداء</a></li>
<li><a href="https://docs.ultralytics.com/guides/model-training-tips/">Ultralytics — نصائح للتدريب</a></li>
<li><a href="https://storage.googleapis.com/openimages/web/index.html">Open Images Dataset</a></li>
</ul>"""
)


# ===========================================================================
# الدمج مع الدفتر الموجود
# ===========================================================================


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    cells = notebook["cells"]

    def source_of(cell: dict) -> str:
        return "".join(cell["source"])

    # ننهي التنظيف الذي بدأه المؤلف: خلية الشكل السادس ما زالت تحمل الوصف
    # القديم، وبعدها خلية كود معطَّلة لم تعد لازمة.
    for index, cell in enumerate(cells):
        if DATA_YAML_NOTES_MARKER in source_of(cell):
            cells[index] = _cell(
                "markdown", f"{RTL_OPEN}\n\n{DATA_YAML_NOTES}\n\n{RTL_CLOSE}"
            )
            break

    for index, cell in enumerate(cells):
        if FIGURE_6_MARKER in source_of(cell):
            cells[index] = _cell(
                "markdown",
                f"""{RTL_OPEN}

<h4>دور كل قسم من الأقسام الثلاثة</h4>

<p>الشكل التالي يلخّص الأدوار الثلاثة والخطأ الشائع في التقسيم.</p>

{RTL_CLOSE}""",
            )
            following = cells[index + 1] if index + 1 < len(cells) else None
            if following is not None and "TODO-FIG-06" in source_of(following):
                cells[index + 1] = _cell(
                    "markdown", "![Figure 6](media/train_val_test_split.jpg)"
                )
            break

    # قابل لإعادة التشغيل: نحذف كل ما بعد بداية القسم الرابع إن وُجد.
    for index, cell in enumerate(cells):
        if SECTION_4_MARKER in source_of(cell):
            del cells[index:]
            break

    cells.extend(new_cells)
    NOTEBOOK.write_text(json.dumps(notebook, ensure_ascii=False, indent=1))

    n_md = sum(1 for c in cells if c["cell_type"] == "markdown")
    n_code = sum(1 for c in cells if c["cell_type"] == "code")
    print(f"{NOTEBOOK}: {len(cells)} خلية ({n_md} markdown، {n_code} code)")
    print(f"أُضيفت {len(new_cells)} خلية للأقسام 4-15.")


if __name__ == "__main__":
    main()
