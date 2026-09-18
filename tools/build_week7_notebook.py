#!/usr/bin/env python3
"""
يبني دفتر الأسبوع 7. نولّد الدفتر من سكربت بدل تحريره يدوياً حتى نضمن
تناسق تغليف RTL في كل خلية، ونتمكن من إعادة التوليد بعد التدريب المرجعي.

الاستخدام:
    python tools/build_week7_notebook.py
"""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path("Week7/week_7_training_and_finetuning.ipynb")

# نفس كتلة النمط المستخدمة في الأسبوع 6، لكن مكتوبة مرة واحدة في أول خلية
# بدل تكرارها في كل خلية عربية.
STYLE = """<style>
.rtl-cell {
    direction: rtl !important;
    text-align: right !important;
    line-height: 1.9 !important;
    font-size: 17px !important;
    font-family: Arial, Tahoma, sans-serif !important;
}
.rtl-cell p,
.rtl-cell h1, .rtl-cell h2, .rtl-cell h3, .rtl-cell h4,
.rtl-cell li, .rtl-cell blockquote, .rtl-cell th, .rtl-cell td {
    direction: rtl !important;
    text-align: right !important;
}
.rtl-cell ul, .rtl-cell ol {
    direction: rtl !important;
    text-align: right !important;
    padding-right: 2em !important;
    padding-left: 0 !important;
}
.rtl-cell blockquote {
    border-right: 4px solid #d0d7de !important;
    border-left: none !important;
    margin-right: 0 !important;
    padding-right: 1em !important;
}
.rtl-cell table {
    direction: rtl !important;
    text-align: right !important;
    margin-right: 0 !important;
    margin-left: auto !important;
    border-collapse: collapse !important;
}
.rtl-cell th, .rtl-cell td { padding: 7px 10px !important; }
.rtl-cell code { direction: ltr !important; unicode-bidi: isolate !important; }
.rtl-cell pre, .rtl-cell pre code {
    direction: ltr !important;
    text-align: left !important;
    unicode-bidi: embed !important;
}
.rtl-cell .todo {
    background-color: rgba(249, 168, 37, 0.14);
    border-right: 5px solid #F9A825;
    padding: 12px 18px;
    margin: 16px 0;
    border-radius: 6px;
}
.rtl-cell .note {
    background-color: rgba(127, 127, 127, 0.12);
    border-right: 5px solid #777;
    padding: 12px 18px;
    margin: 16px 0;
    border-radius: 6px;
}
</style>
"""

RTL_OPEN = '<div dir="rtl" class="rtl-cell" style="direction:rtl; text-align:right;">'
RTL_CLOSE = "</div>"

cells: list[dict] = []


def rtl(body: str) -> None:
    """خلية markdown عربية مغلَّفة بـ div dir=rtl."""
    text = f"{RTL_OPEN}\n\n{body.strip()}\n\n{RTL_CLOSE}"
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [l + "\n" for l in text.split("\n")],
        }
    )


def code(src: str) -> None:
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [l + "\n" for l in src.strip().split("\n")],
        }
    )


def figure_todo(
    fig_id: str,
    filename: str,
    arabic_title: str,
    arabic_why: str,
    brief: str,
    width: int = 900,
) -> None:
    """
    خليتان لكل شكل لم يُنتَج بعد: خلية شرح عربية تحمل الـ brief كاملاً،
    وخلية كود معطَّلة تعرض الصورة حين تصبح جاهزة.
    """
    rtl(
        f"""<h4>{arabic_title}</h4>

<p>{arabic_why}</p>

<div class="todo">
<p><strong>TODO — {fig_id}</strong> — الشكل غير منتَج بعد. الملف المطلوب:
<code>media/{filename}</code></p>
<p>النص التالي هو الوصف الكامل الجاهز لتسليمه لمن سينتج الشكل. النمط العام
لكل أشكال الدرس موصوف في الخلية الأولى من نوعها (TODO-FIG-01).</p>
<pre>{brief.strip()}</pre>
</div>"""
    )
    code(
        f"""# {fig_id} — يُفعَّل بعد إنتاج الصورة في media/{filename}
# from IPython.display import Image as IPImage
# IPImage("media/{filename}", width={width})"""
    )


STYLE_GUIDE = """SHARED STYLE GUIDE (applies to every figure in Week 7)
------------------------------------------------------
Format   : PNG, dpi=200, logical width 1600px (1600x900 for wide figures).
Canvas   : explicit solid WHITE (#FFFFFF) background, never transparent,
           so it stays readable in both light and dark Jupyter themes.
Font     : DejaVu Sans. ALL text inside figures is ENGLISH; the Arabic
           explanation lives in the notebook markdown, not in the image.
Palette  : #1565C0 blue   = ground truth / "before" / pretrained model
           #2E7D32 green  = correct detection / true positive / "after"
           #C62828 red    = error / false positive / failure
           #F9A825 amber  = warning / low confidence / highlight
           #616161 grey   = neutral, arrows, axes, secondary text
           #ECEFF1 light  = panel fills
Drawing  : completely flat. No gradients, no shadows, no 3D, NO EMOJI.
           Boxes: rounded rectangles, pad 0.4, linewidth 2.
           Arrows: plain "-|>" heads in grey.
           Check / cross marks: text glyphs are OK, coloured by role.
Type size: title 18pt bold, panel titles 14pt bold, labels 13pt,
           annotations 11pt. Formulas via matplotlib mathtext.
Output   : save to Week7/media/<exact filename>, referenced from the
           notebook by a RELATIVE path only."""


# ===========================================================================
# 0-6 : العنوان والتهيئة
# ===========================================================================

cells.append(
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            l + "\n"
            for l in (
                STYLE
                + "\n"
                + RTL_OPEN
                + """

<h1>الأسبوع 7: التدريب والضبط الدقيق</h1>
<h2>Training and Fine-Tuning</h2>
<hr />
<p><strong>مسار أنظمة المرور الذكية – الرؤية الحاسوبية</strong></p>
<p><strong>المُعد/المؤلف:</strong> </p>
<hr />

<p>في الأسبوع الماضي شغّلنا نموذج YOLO جاهزاً وكشفنا به السيارات والمشاة،
ولم ندرّب شيئاً. النموذج الجاهز يعرف ثمانين فئة تعلّمها من مجموعة
<strong>COCO</strong>، وكان ذلك كافياً لأن السيارة والشخص من ضمن هذه الفئات.</p>

<p>لكن نظام المرور الذي نبنيه يحتاج شيئاً لا تعرفه COCO إطلاقاً:</p>

<blockquote>
<p><strong>هل هذه المركبة سيارة إسعاف؟</strong></p>
</blockquote>

<p>لا توجد فئة اسمها <code>ambulance</code> بين فئات COCO الثمانين. لذلك مهما
ضبطنا قيمة <code>conf</code> ومهما غيّرنا حجم النموذج، لن يخبرنا النموذج
الجاهز بوجود إسعاف، لأنه ببساطة لا يملك الكلمة في قاموسه.</p>

<p>هنا يبدأ عمل هذا الأسبوع: سنأخذ النموذج الجاهز، ونُعلّمه فئة جديدة من
بياناتنا نحن. هذه العملية اسمها <strong>Fine-Tuning</strong>، وهي الجسر بين
"نموذج يعمل" و"نموذج يعمل على مشكلتنا".</p>

<p>وفي نهاية الدرس سيكون بين أيدينا نموذج يميّز الإسعاف عن بقية المركبات،
وهو النموذج الذي سنتتبّعه في الأسبوع القادم ونبني عليه منطق أولوية الإشارة
في الأسبوع التاسع.</p>

<div class="note">
<p><strong>هذا الدرس يعمل بلا إنترنت.</strong> كل ما تحتاجه موجود داخل مجلد
<code>Week7</code> نفسه: الصور، والتوسيم، والنموذج الجاهز، ونتائج التدريب
المرجعية. لا تحتاج إلى حساب ولا إلى تحميل أي شيء أثناء الحصة.</p>
</div>

"""
                + RTL_CLOSE
            ).split("\n")
        ],
    }
)

rtl(
    """<h2>أهداف الدرس</h2>

<p>في نهاية هذا الدرس ستكون قادراً على أن:</p>

<ol>
<li>تشرح لماذا يفشل نموذج جاهز على مسألة معيّنة، وتميّز بين نوعَي الفشل:
<strong>فجوة في الفئات</strong> و<strong>اختلاف في المجال</strong>.</li>
<li>تفرّق بين التدريب من الصفر و<strong>Transfer Learning</strong>، وتعرف
متى يستحق كلٌّ منهما.</li>
<li>تقرأ وتكتب توسيماً بصيغة YOLO، وتحوّل إحداثيات البكسل إلى إحداثيات
مطبَّعة بيدك.</li>
<li>تبني بنية مجلدات صحيحة وملف <code>data.yaml</code>، وتقسّم البيانات إلى
<code>train</code> و <code>valid</code> و <code>test</code> تقسيماً نزيهاً.</li>
<li>تشغّل عملية تدريب فعلية وتفهم معنى كل رقم يظهر أثناءها.</li>
<li>تقيّم النموذج بـ <strong>Precision</strong> و<strong>Recall</strong>
و<strong>mAP</strong>، وتقرأ مصفوفة الالتباس ومنحنيات التدريب.</li>
<li>تشخّص التجهيز الزائد <strong>Overfitting</strong> وتعرف ماذا تفعل حياله.</li>
</ol>"""
)

rtl(
    """<h2>محتويات الدرس</h2>

<ol>
<li>أين يفشل النموذج الجاهز؟</li>
<li>ما هو Fine-Tuning ولماذا لا ندرّب من الصفر؟</li>
<li>تجهيز قاعدة البيانات</li>
<li>التعزيز Data Augmentation</li>
<li>تشريح عملية التدريب</li>
<li>لنُدرّب</li>
<li>قراءة النتائج والتقييم</li>
<li>اللحظة الحاسمة: قبل وبعد</li>
<li>دليل التحسين حين تكون النتائج ضعيفة</li>
<li>حفظ النموذج واستخدامه لاحقاً</li>
<li>حدود ما فعلناه</li>
<li>تمرين صفي</li>
<li>أسئلة مراجعة سريعة</li>
<li>بنك أسئلة Kahoot</li>
<li>الخلاصة</li>
</ol>"""
)

rtl(
    """<hr />
<h1>التهيئة</h1>

<p>الخلية التالية <strong>لا تثبّت شيئاً</strong>، بل تتحقق فقط من وجود
المكتبات. التثبيت يتم مرة واحدة قبل الحصة حسب ما هو مشروح في ملف
<code>SETUP.md</code> بجانب هذا الدفتر.</p>"""
)

code(
    '''import importlib.util

REQUIRED = ["ultralytics", "cv2", "torch", "pandas", "matplotlib", "yaml"]

missing = [name for name in REQUIRED if importlib.util.find_spec(name) is None]

if missing:
    print("المكتبات الناقصة:", "، ".join(missing))
    print("نفّذ ما في ملف SETUP.md مرة واحدة، ثم أعد تشغيل النواة (Restart Kernel).")
else:
    print("كل المكتبات المطلوبة متوفرة.")'''
)

rtl(
    """<h2>الاستيرادات وإعدادات العمل بلا إنترنت</h2>

<p>مكتبة Ultralytics تحاول الاتصال بالإنترنت في أكثر من موضع: لتحميل الأوزان
إن لم تجدها، ولإرسال إحصاءات استخدام. الخلية التالية تعطّل ذلك وتشير إلى
نسخة النموذج المحفوظة محلياً داخل <code>models/</code>.</p>"""
)

code(
    '''import os
from collections import Counter
from pathlib import Path

os.environ["YOLO_VERBOSE"] = "False"

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import yaml

from ultralytics import YOLO, settings

# إيقاف إرسال إحصاءات الاستخدام، فهو يحتاج اتصالاً بالشبكة.
settings.update({"sync": False})

# مسارات محلية: لا شيء يُحمَّل من الإنترنت في هذا الدفتر.
PRETRAINED_PATH = "models/yolo11n.pt"
DATA_YAML = "dataset/data.yaml"
REFERENCE_RUN = Path("runs_reference/emergency_full")

print("PyTorch:", torch.__version__)
print("النموذج الجاهز:", PRETRAINED_PATH)'''
)

rtl(
    """<h2>الجهاز المستخدم</h2>

<p>سنعمل في الحصة على المعالج <code>cpu</code>، وهذا يحدّد حجم التدريب الذي
يمكننا تنفيذه مباشرة. إن كان لديك كرت شاشة NVIDIA في البيت فسيظهر
<code>cuda</code>، وعندها يمكنك تشغيل التدريب الكامل في القسم السادس.</p>"""
)

code(
    '''DEVICE = 0 if torch.cuda.is_available() else "cpu"

print("الجهاز المستخدم:", DEVICE)
print("عدد أنوية المعالج المتاحة:", os.cpu_count())'''
)


# ===========================================================================
# القسم 1: أين يفشل النموذج الجاهز؟
# ===========================================================================

rtl(
    """<hr />
<h1>1. أين يفشل النموذج الجاهز؟</h1>

<p>قبل أن ندرّب أي شيء، علينا أن نثبت أن التدريب ضروري أصلاً. أسوأ ما يمكن
أن يفعله مهندس رؤية حاسوبية هو أن يدرّب نموذجاً جديداً بينما كان النموذج
الجاهز كافياً.</p>

<p>لذلك سنبدأ بتجربة: نأخذ النموذج نفسه الذي استخدمناه في الأسبوع الماضي،
ونشغّله على صور فيها سيارات إسعاف، ثم ننظر ماذا يقول.</p>

<h2>1.1 تجربة حية على صور من الشارع</h2>

<p>مجلد <code>failures/</code> يحوي خمس صور اخترناها بعناية، وملف
<code>failures.csv</code> يذكر لكل صورة ما <em>ينبغي</em> أن يكون الجواب
الصحيح.</p>"""
)

code(
    '''pretrained_model = YOLO(PRETRAINED_PATH)

print("عدد الفئات التي يعرفها النموذج الجاهز:", len(pretrained_model.names))

# هل توجد فئة للإسعاف بين فئات COCO الثمانين؟
has_ambulance = any(
    "ambulance" in name.lower() for name in pretrained_model.names.values()
)
print("هل يعرف النموذج فئة ambulance؟", "نعم" if has_ambulance else "لا")

# الفئات المتعلقة بالمركبات التي يعرفها فعلاً:
vehicle_names = ["car", "bus", "truck", "motorcycle", "bicycle", "train"]
for class_id, name in pretrained_model.names.items():
    if name in vehicle_names:
        print(f"  {class_id:2d} -> {name}")'''
)

rtl(
    """<p>الآن نشغّل النموذج على صور الفشل ونقارن ما يقوله بما ينبغي أن يقوله.</p>"""
)

code(
    '''failures_df = pd.read_csv("failures/failures.csv")

rows = []

for _, item in failures_df.iterrows():
    image_path = f"failures/{item['file']}"

    result = pretrained_model.predict(
        source=image_path,
        conf=0.25,
        device=DEVICE,
        verbose=False,
    )[0]

    if len(result.boxes) == 0:
        predicted = "لا شيء"
        confidence = 0.0
    else:
        # نأخذ أعلى كشف ثقةً كإجابة النموذج عن "ما هذه المركبة؟"
        best = int(result.boxes.conf.argmax())
        predicted = result.names[int(result.boxes.cls[best])]
        confidence = float(result.boxes.conf[best])

    rows.append({
        "الصورة": item["file"],
        "قال النموذج": predicted,
        "الثقة": round(confidence, 2),
        "الصحيح": item["correct_class"],
        "نوع الفشل": item["failure_type"],
    })

pd.DataFrame(rows)'''
)

rtl("""<p>ولنرَ ذلك بأعيننا لا بالأرقام فقط:</p>""")

code(
    '''fig, axes = plt.subplots(2, 3, figsize=(18, 11))

for ax, (_, item) in zip(axes.flat, failures_df.iterrows()):
    result = pretrained_model.predict(
        source=f"failures/{item['file']}",
        conf=0.25,
        device=DEVICE,
        verbose=False,
    )[0]

    ax.imshow(cv2.cvtColor(result.plot(), cv2.COLOR_BGR2RGB))
    ax.set_title(f"should be: {item['correct_class']}", fontsize=13)
    ax.axis("off")

# الخلية السادسة نتركها فارغة لأن عدد الصور خمس.
axes.flat[-1].axis("off")

plt.suptitle("Pretrained YOLO on emergency vehicles", fontsize=17)
plt.tight_layout()
plt.show()'''
)

rtl(
    """<h2>1.2 أنواع الفشل الأربعة</h2>

<p>ما رأيناه ليس فشلاً واحداً بل أربعة أنواع مختلفة، ولكل نوع علاج مختلف:</p>

<table>
<thead>
<tr><th>النوع</th><th>ما يحدث</th><th>مثال</th><th>هل يصلحه ضبط conf؟</th></tr>
</thead>
<tbody>
<tr>
  <td><strong>فجوة في الفئات</strong></td>
  <td>الفئة غير موجودة في قاموس النموذج أصلاً</td>
  <td>إسعاف يُكشف <code>truck</code></td>
  <td>لا، أبداً</td>
</tr>
<tr>
  <td><strong>فئة خاطئة</strong></td>
  <td>يكشف الجسم لكن يسمّيه خطأ</td>
  <td>ميكروباص يتذبذب بين <code>bus</code> و <code>truck</code></td>
  <td>لا</td>
</tr>
<tr>
  <td><strong>كشف مفقود</strong></td>
  <td>لا يرى الجسم إطلاقاً</td>
  <td>إسعاف ليلاً أو بعيداً</td>
  <td>جزئياً، بخفض العتبة</td>
</tr>
<tr>
  <td><strong>صندوق سيّئ</strong></td>
  <td>يرى الجسم لكن الصندوق غير دقيق</td>
  <td>مركبتان متلاصقتان في صندوق واحد</td>
  <td>لا</td>
</tr>
</tbody>
</table>

<p>النوعان الأول والثاني سببهما <strong>فجوة في الفئات</strong>: القاموس
نفسه ناقص. والنوعان الثالث والرابع سببهما <strong>اختلاف المجال
Domain Shift</strong>: الفئة موجودة لكن الصور التي تدرّب عليها النموذج تختلف
عن صورنا في الإضاءة والزاوية والازدحام.</p>

<blockquote>
<p>هذا التمييز هو مفتاح الدرس كله. <strong>فجوة الفئات لا يصلحها إلا
التدريب.</strong> أما اختلاف المجال فقد يخفّ بضبط العتبات، لكن التدريب على
بياناتنا يعالجه أفضل بكثير.</p>
</blockquote>"""
)

figure_todo(
    "TODO-FIG-01",
    "coco_class_gap.png",
    "1.3 لماذا يحدث هذا؟ ما هي COCO",
    "النموذج الجاهز تدرّب على مجموعة COCO، وهي ثمانون فئة عامة اختيرت قبل "
    "سنوات لأغراض بحثية عامة، لا لنظام مرور. الشكل التالي يوضح الفجوة بين "
    "ما تعرفه COCO وما نحتاجه نحن.",
    f"""{STYLE_GUIDE}

FIGURE TODO-FIG-01  ->  Week7/media/coco_class_gap.png
Title: "What COCO cannot say"
Size : 1600 x 900

LEFT PANEL  (panel title: "COCO: 80 classes")
  An 8 x 10 grid of small rounded "chips", one per COCO class,
  filled #ECEFF1 with 8pt #616161 text (person, bicycle, car, ...).
  This panel should read as a dense but unremarkable wall of words.

RIGHT PANEL (panel title: "What our traffic system needs")
  Four large chips stacked vertically, 20pt text:
    car        -> green #2E7D32, marked with a check glyph
    truck      -> green #2E7D32, marked with a check glyph
    bus        -> green #2E7D32, marked with a check glyph
    ambulance  -> red   #C62828, marked with a cross glyph

CONNECTIONS
  From each of the three GREEN chips draw a thin solid grey (#616161)
  arrow leading back to the matching chip inside the left grid; also
  highlight that matching left-grid chip with a green outline.
  From the RED "ambulance" chip draw a DASHED red (#C62828) arrow that
  points at the left grid and stops short in empty space, with the
  label "no matching class" in red near the arrow head.

BOTTOM STRIP (full width, 13pt, #616161)
  "car, truck and bus exist in COCO. ambulance does not.
   No confidence threshold can create a class that was never trained."

The single idea the reader must leave with: three of our four classes
are already in COCO, and exactly one is missing -- which is precisely
why fine-tuning is required and why the before/after comparison later
in the lesson isolates one variable.""",
)

rtl(
    """<h2>فكر قبل المتابعة</h2>

<p>قبل أن تنتقل إلى القسم التالي، فكّر في هذه الأسئلة:</p>

<ol>
<li>لو خفّضنا <code>conf</code> إلى <code>0.05</code>، هل سيظهر
<code>ambulance</code> في النتائج؟ ولماذا؟</li>
<li>النموذج سمّى الإسعاف <code>truck</code>. هل هذا خطأ من النموذج، أم أنه
أفضل إجابة ممكنة ضمن قاموسه؟</li>
<li>لو أردت نظاماً يعطي الأولوية للإسعاف، ما الحد الأدنى من الفئات التي
تحتاجها فعلاً؟</li>
<li>متى يكون استخدام النموذج الجاهز هو القرار الصحيح رغم أخطائه؟</li>
</ol>"""
)


# ===========================================================================
# القسم 2: ما هو Fine-Tuning
# ===========================================================================

rtl(
    """<hr />
<h1>2. ما هو Fine-Tuning ولماذا لا ندرّب من الصفر؟</h1>

<h2>2.1 التدريب من الصفر مقابل Transfer Learning</h2>

<p>أمامنا طريقان لبناء نموذج يعرف الإسعاف:</p>

<table>
<thead>
<tr>
  <th></th>
  <th>التدريب من الصفر</th>
  <th>Fine-Tuning</th>
</tr>
</thead>
<tbody>
<tr>
  <td>نقطة البداية</td>
  <td>أوزان عشوائية</td>
  <td>أوزان نموذج تدرّب على ملايين الصور</td>
</tr>
<tr>
  <td>حجم البيانات المطلوب</td>
  <td>عشرات أو مئات الآلاف من الصور</td>
  <td>مئات إلى بضعة آلاف</td>
</tr>
<tr>
  <td>الزمن</td>
  <td>أيام إلى أسابيع</td>
  <td>دقائق إلى ساعات</td>
</tr>
<tr>
  <td>العتاد</td>
  <td>عدة كروت شاشة</td>
  <td>كرت واحد، وأحياناً معالج فقط</td>
</tr>
<tr>
  <td>متى نختاره</td>
  <td>بيانات مختلفة جذرياً عن الصور الطبيعية</td>
  <td>في كل الحالات العملية تقريباً</td>
</tr>
</tbody>
</table>

<p>في الممارسة العملية، التدريب من الصفر قرار نادر جداً. نحن سنستخدم
Fine-Tuning، وهذا ليس حلاً وسطاً بل هو الخيار الصحيح.</p>"""
)

figure_todo(
    "TODO-FIG-02",
    "transfer_learning.png",
    "2.2 ماذا تعلّمه الـ Backbone فعلاً؟",
    "لفهم لماذا ينجح Fine-Tuning، علينا أن نعرف أن النموذج ليس كتلة واحدة. "
    "الطبقات الأولى تعلّمت أشياء عامة جداً: الحواف، ثم الملامس، ثم أجزاء "
    "الأجسام كالعجلات والنوافذ. هذه المعرفة صالحة لأي مركبة، ولا داعي "
    "لإعادة تعلّمها. الجزء الوحيد المرتبط بقائمة الفئات هو الرأس Head.",
    """FIGURE TODO-FIG-02  ->  Week7/media/transfer_learning.png
Title: "Fine-tuning: reuse the eyes, replace the vocabulary"
Size : 1600 x 850
Style: see the shared style guide in TODO-FIG-01.

MAIN ROW (left to right, connected by grey "-|>" arrows)
  1. Small grey box: "Input 640 x 640"
  2. LARGE BLUE (#1565C0) rounded box: "Backbone (pretrained)"
     - draw a simple padlock glyph in its top-right corner
     - inside, three faint sub-labels left to right:
       "edges"  ->  "textures"  ->  "object parts"
     - caption under the box: "frozen or gently updated"
  3. GREY rounded box: "Neck (FPN / PAN)"
     - caption: "combines scales"
  4. The Neck FORKS into two boxes stacked vertically:
     TOP    - pale grey, low opacity: "Head: 80 COCO classes"
              marked with a red cross glyph, caption "discarded"
     BOTTOM - AMBER (#F9A825): "Head: 4 our classes"
              marked with a green check glyph,
              caption "re-initialised and trained"
              list inside: ambulance, car, truck, bus

BOTTOM STRIP (full width, 13pt, #616161)
  "About 99% of the weights are reused. We only teach the last part
   a new vocabulary -- that is why a few hundred images are enough."

Emphasis: the visual weight of the blue Backbone box should be large,
and the amber Head box small, so the reader sees at a glance how little
of the network is actually being replaced.""",
)

rtl(
    """<h2>2.3 متى يكفي النموذج الجاهز ومتى نحتاج التدريب؟</h2>

<p>استخدم هذه القاعدة العملية:</p>

<ul>
<li><strong>الفئة التي تحتاجها غير موجودة في قاموس النموذج</strong>
  ← التدريب إلزامي. لا بديل عنه.</li>
<li><strong>الفئة موجودة لكن الأداء ضعيف على صورك</strong>
  ← جرّب أولاً ضبط <code>conf</code> و <code>imgsz</code>، ثم جرّب نموذجاً
  أكبر (<code>yolo11s</code> بدل <code>yolo11n</code>). فإن بقي الأداء ضعيفاً
  فالتدريب هو الحل.</li>
<li><strong>الفئة موجودة والأداء جيد</strong>
  ← لا تدرّب. استخدم الجاهز ووفّر وقتك لبقية النظام.</li>
</ul>

<p>حالتنا من النوع الأول: <code>ambulance</code> غير موجودة، فالقرار محسوم.</p>"""
)


# ===========================================================================
# القسم 3: تجهيز قاعدة البيانات
# ===========================================================================

rtl(
    """<hr />
<h1>3. تجهيز قاعدة البيانات</h1>

<p>هذا أطول أقسام الدرس وأكثرها أهمية عملياً. في المشاريع الحقيقية يذهب
معظم الوقت إلى البيانات لا إلى النموذج، والنموذج الممتاز على بيانات سيّئة
يعطي نتائج سيّئة دائماً.</p>

<h2>3.1 تسمية على مستوى الصورة مقابل تسمية على مستوى الجسم</h2>

<p>قبل أن نبدأ، لا بد من تمييز أساسي. ليست كل مجموعة بيانات فيها صور
ومركبات صالحةً لتدريب كاشف.</p>

<p>في مجلد <code>classification_example/</code> نسخة من ملف توسيم مجموعة
شهيرة لمركبات الطوارئ. لننظر ماذا تحوي:</p>"""
)

code(
    '''classification_labels = pd.read_csv("classification_example/train.csv")

print("الأعمدة:", list(classification_labels.columns))
print("عدد الصفوف:", len(classification_labels))
print()
print(classification_labels.head())
print()
print("توزيع التسميات:")
print(classification_labels["emergency_or_not"].value_counts())'''
)

rtl(
    """<p>عمودان فقط: اسم الصورة، وهل فيها مركبة طوارئ أم لا. هذه تسمية
<strong>على مستوى الصورة</strong> (Image-level)، وهي تكفي لمسألة
<strong>تصنيف</strong> تجيب عن سؤال: "ماذا في هذه الصورة؟"</p>

<p>لكن الكشف يحتاج جواباً عن سؤال أصعب: "<strong>أين</strong> كل جسم،
و<strong>ما</strong> هو؟" وهذا يتطلب تسمية <strong>على مستوى الجسم</strong>
(Object-level): أربعة أرقام تحدّد صندوقاً، وفئة لكل صندوق، لكل جسم في
الصورة على حدة.</p>

<div class="note">
<p><strong>القاعدة:</strong> لا يمكن تدريب كاشف على مجموعة تصنيف. لو رأيت
مجموعة بيانات فيها ملف CSV بعمودين فقط، فهي للتصنيف لا للكشف مهما كان
اسمها. تحقق دائماً من وجود صناديق الإحاطة قبل أن تخطط لتدريب كاشف.</p>
</div>

<h2>3.2 من أين نجمع الصور؟</h2>

<p>القاعدة الذهبية في جمع بيانات الكشف:</p>

<blockquote>
<p><strong>التنوّع أهم من الكم.</strong></p>
</blockquote>

<p>مئتا صورة متنوعة تتفوق على ألفَي صورة متشابهة. تنوَّع في:</p>

<ul>
<li><strong>الإضاءة</strong>: نهار، ليل، غروب، أضواء شوارع.</li>
<li><strong>الطقس</strong>: صحو، مطر، غبار.</li>
<li><strong>الزاوية والبعد</strong>: من الأمام، من الجانب، من الخلف،
قريب وبعيد.</li>
<li><strong>الحجب</strong>: مركبات محجوبة جزئياً خلف غيرها.</li>
<li><strong>الخلفية</strong>: شارع مزدحم، طريق فارغ، ساحة مستشفى.</li>
<li><strong>الأمثلة السلبية</strong>: صور فيها مركبات عادية فقط، بلا إسعاف.
هذه ضرورية ليتعلّم النموذج ما <em>ليس</em> إسعافاً.</li>
</ul>"""
)

figure_todo(
    "TODO-FIG-03",
    "yolo_label_format.png",
    "3.3 صيغة YOLO للتوسيم",
    "لكل صورة ملف نصي واحد يحمل الاسم نفسه بامتداد <code>.txt</code>. كل سطر "
    "في الملف يمثّل جسماً واحداً، وفيه خمسة أرقام. الشكل التالي يشرح هذه "
    "الأرقام الخمسة، وهو أهم شكل في الدرس كله.",
    """FIGURE TODO-FIG-03  ->  Week7/media/yolo_label_format.png
Title: "One line per object: how a YOLO label file is built"
Size : 1600 x 750  (three panels side by side)
Style: see the shared style guide in TODO-FIG-01.

LEFT PANEL -- "the picture"
  A photo of a street scene 640 x 480 with ONE ambulance.
  Draw a green (#2E7D32) box around the ambulance, linewidth 3.
  Add thin dashed grey measurement guides with labels:
    - a vertical dashed line from the box centre to the image top,
      labelled "x_center = 308 px"
    - a horizontal dashed line from the box centre to the image left,
      labelled "y_center = 293 px"
    - a horizontal double-headed arrow across the box: "w = 120 px"
    - a vertical double-headed arrow down the box: "h = 130 px"
  Label the image edges "W = 640" (top) and "H = 480" (left side).

MIDDLE PANEL -- "the arithmetic"
  Four stacked mathtext equations, 16pt, left aligned, with the
  division shown explicitly so students can follow it:
     x = 308 / 640 = 0.4812
     y = 293 / 480 = 0.6104
     w = 120 / 640 = 0.1875
     h = 130 / 480 = 0.2708
  Above them a small heading: "divide by the image size"

RIGHT PANEL -- "the file"
  A monospace code block on #ECEFF1 with a filename caption above it:
      dataset/train/labels/img_042.txt
  Content, exactly two lines:
      0 0.4812 0.6104 0.1875 0.2708
      1 0.7500 0.5500 0.1000 0.0900
  Directly ABOVE the first line, place five small column headers in
  #616161 aligned to the five numbers:
      class_id   x_center   y_center   width   height
  Draw a green arrow from the middle panel's results into the first
  line of the file to show they are the same numbers.
  Add a legend under the block: "0 = ambulance,  1 = car"

BOTTOM NOTE (red #C62828, 13pt, centred)
  "All four coordinates are normalised to [0, 1] -- never pixels.
   This is what makes a label file independent of image size."
""",
)

rtl(
    """<h2>3.4 نكتب ملف توسيم بأيدينا</h2>

<p>أفضل طريقة لفهم الصيغة هي أن نكتبها بأنفسنا مرة واحدة، بلا أي أداة
وبلا إنترنت. سنأخذ صورة من قاعدة بياناتنا، ونحوّل صندوقاً بالبكسل إلى
سطر YOLO، ثم نقرأ السطر ونعيد رسم الصندوق للتحقق.</p>"""
)

code(
    '''# نختار صورة فيها إسعاف واحد لنعمل عليها
for candidate in sorted(Path("dataset/train/images").glob("*.jpg")):
    candidate_label = Path("dataset/train/labels") / (candidate.stem + ".txt")
    ambulance_lines = [
        line for line in candidate_label.read_text().split("\\n")
        if line.strip() and line.split()[0] == "0"
    ]
    if len(ambulance_lines) == 1:
        sample_image_path = candidate
        break

sample_image = cv2.cvtColor(cv2.imread(str(sample_image_path)), cv2.COLOR_BGR2RGB)
image_height, image_width = sample_image.shape[:2]
print("الصورة:", sample_image_path.name, "->", image_width, "x", image_height)

# تخيّل أنك فتحت الصورة في أداة توسيم وقرأت زوايا الصندوق بالبكسل.
# هذه هي الأرقام التي كنت ستراها على الشاشة:
_, gt_xc, gt_yc, gt_w, gt_h = map(float, ambulance_lines[0].split())
x1 = round((gt_xc - gt_w / 2) * image_width)
y1 = round((gt_yc - gt_h / 2) * image_height)
x2 = round((gt_xc + gt_w / 2) * image_width)
y2 = round((gt_yc + gt_h / 2) * image_height)

print(f"الصندوق كما قرأناه بالبكسل: ({x1}, {y1}) -> ({x2}, {y2})")

# الخطوة 1: من الزوايا إلى المركز والأبعاد
box_width = x2 - x1
box_height = y2 - y1
x_center = x1 + box_width / 2
y_center = y1 + box_height / 2

print(f"بالبكسل  -> x_center={x_center:.0f}, y_center={y_center:.0f}, "
      f"w={box_width}, h={box_height}")

# الخطوة 2: التطبيع، أي القسمة على أبعاد الصورة
x_norm = x_center / image_width
y_norm = y_center / image_height
w_norm = box_width / image_width
h_norm = box_height / image_height

CLASS_ID = 0  # ambulance

label_line = f"{CLASS_ID} {x_norm:.6f} {y_norm:.6f} {w_norm:.6f} {h_norm:.6f}"
print("سطر YOLO ->", label_line)'''
)

rtl(
    """<p>الآن نكتب السطر إلى ملف، ثم نقرأه من جديد ونعيد بناء الصندوق
بالبكسل. إن عاد الصندوق إلى مكانه الأصلي فقد فهمنا الصيغة فهماً صحيحاً.</p>"""
)

code(
    '''Path("demo_label.txt").write_text(label_line + "\\n")

# القراءة من الملف كما ستقرأه YOLO تماماً
read_class_id, rx, ry, rw, rh = Path("demo_label.txt").read_text().split()
rx, ry, rw, rh = float(rx), float(ry), float(rw), float(rh)

# عكس التطبيع: من [0,1] إلى بكسل
back_x1 = round((rx - rw / 2) * image_width)
back_y1 = round((ry - rh / 2) * image_height)
back_x2 = round((rx + rw / 2) * image_width)
back_y2 = round((ry + rh / 2) * image_height)

print("الصندوق الأصلي   :", (x1, y1, x2, y2))
print("الصندوق بعد العودة:", (back_x1, back_y1, back_x2, back_y2))

drawn = sample_image.copy()
cv2.rectangle(drawn, (back_x1, back_y1), (back_x2, back_y2), (46, 125, 50), 3)

plt.figure(figsize=(8, 6))
plt.imshow(drawn)
plt.axis("off")
plt.title("Box reconstructed from the normalized label file")
plt.show()'''
)

rtl(
    """<h2>3.5 أدوات التوسيم المستخدمة عملياً</h2>

<p>لن نوسّم قاعدة بيانات كاملة بأيدينا، فهذا عمل أسابيع. الأدوات التالية
هي ما يُستخدم فعلياً في المشاريع:</p>

<table>
<thead>
<tr>
  <th>الأداة</th>
  <th>في المتصفح</th>
  <th>تحتاج تسجيلاً</th>
  <th>تعمل بلا إنترنت</th>
  <th>متى نختارها</th>
</tr>
</thead>
<tbody>
<tr>
  <td><strong>LabelImg</strong></td>
  <td>لا</td><td>لا</td><td>نعم</td>
  <td>الأنسب لحالتنا: برنامج بسيط يعمل بلا إنترنت ويصدّر صيغة YOLO مباشرة</td>
</tr>
<tr>
  <td><strong>labelme</strong></td>
  <td>لا</td><td>لا</td><td>نعم</td>
  <td>حين نحتاج أشكالاً حرة (polygons) لا صناديق فقط</td>
</tr>
<tr>
  <td><strong>makesense.ai</strong></td>
  <td>نعم</td><td>لا</td><td>لا</td>
  <td>حين لا تملك صلاحية تثبيت برامج على الجهاز</td>
</tr>
<tr>
  <td><strong>Roboflow</strong></td>
  <td>نعم</td><td>نعم</td><td>لا</td>
  <td>المعياري صناعياً: توسيم وتعزيز وتصدير وإدارة نسخ</td>
</tr>
<tr>
  <td><strong>CVAT</strong></td>
  <td>نعم</td><td>نعم</td><td>نعم عند التنصيب محلياً</td>
  <td>الفرق الكبيرة وتوسيم الفيديو إطاراً إطاراً</td>
</tr>
</tbody>
</table>

<p>روابط للاطلاع خارج الحصة:
<a href="https://github.com/HumanSignal/labelImg">LabelImg</a> ·
<a href="https://www.makesense.ai/">makesense.ai</a> ·
<a href="https://roboflow.com/annotate">Roboflow Annotate</a> ·
<a href="https://www.cvat.ai/">CVAT</a></p>"""
)

figure_todo(
    "TODO-FIG-04",
    "annot_labelimg.png",
    "دورة توسيم كاملة في LabelImg",
    "اخترنا LabelImg لأنها الأداة الوحيدة في الجدول التي تعمل بلا إنترنت "
    "تماماً مثل بقية هذا الدرس. الشكل التالي يعرض الخطوات الأربع كاملة "
    "حتى لو لم تكن الأداة مثبّتة على جهازك.",
    """FIGURE TODO-FIG-04  ->  Week7/media/annot_labelimg.png
Title: "Annotating one image in LabelImg, end to end"
Size : 1600 x 1200  (a 2 x 2 grid of annotated screenshots)
Style: see the shared style guide in TODO-FIG-01.

Each of the four cells is a screenshot of the LabelImg window, scaled
to the same width, framed with a thin #616161 border. In every cell,
the UI element being discussed is circled with an AMBER (#F9A825)
rounded rectangle of linewidth 3, and a filled amber circle holding a
white step number sits at that rectangle's top-left corner.
A one-line caption in #616161 sits under each cell.

  STEP 1 - "Open Dir" and "Change Save Dir" buttons in the left toolbar
           circled. Caption: "Point at the images folder, then at the
           labels folder. Keep them separate."

  STEP 2 - The format toggle button in the left toolbar circled; it
           must visibly read "YOLO" (not "PascalVOC").
           Caption: "This single button decides the output format.
           Forgetting it is the most common mistake."

  STEP 3 - The "Create RectBox" button circled, a drawn green box
           around an ambulance in the canvas, and the class-picker
           dialog open with "ambulance" selected.
           Caption: "Draw tight around the object, then pick the class."

  STEP 4 - A file manager or text editor showing the produced .txt file
           side by side with the image, the five numbers visible.
           Caption: "One .txt per image, same filename, five numbers
           per object."

If real screenshots cannot be captured, draw faithful flat mock-ups of
the LabelImg window instead: grey window chrome, a left toolbar with
labelled buttons, and a central canvas holding the photo. Accuracy of
the button NAMES matters more than pixel fidelity.""",
    width=1000,
)

rtl(
    """<h2>3.6 بنية المجلدات وملف data.yaml</h2>

<p>مكتبة Ultralytics تتوقع بنية محددة. لنفحص بنية قاعدة بياناتنا:</p>"""
)

code(
    '''dataset_root = Path("dataset")

for split in ["train", "valid", "test"]:
    n_images = len(list((dataset_root / split / "images").glob("*.jpg")))
    n_labels = len(list((dataset_root / split / "labels").glob("*.txt")))
    print(f"{split:6s} -> {n_images:4d} صورة، {n_labels:4d} ملف توسيم")

print()
print("محتوى data.yaml:")
print("-" * 40)
print(Path("dataset/data.yaml").read_text())'''
)

rtl(
    """<p>لاحظ نقطتين مهمتين:</p>

<ul>
<li>كل صورة <code>img_001.jpg</code> يقابلها ملف <code>img_001.txt</code>
بالاسم نفسه تماماً، في مجلد <code>labels</code> الموازي لمجلد
<code>images</code>. هذه ليست عادة تنظيمية بل هي الطريقة التي تعثر بها
Ultralytics على التوسيم.</li>
<li>ترتيب الأسماء في <code>names</code> هو الذي يحدّد
<code>class_id</code>. لو غيّرت الترتيب بعد التوسيم فسدت كل الملفات
دفعة واحدة.</li>
</ul>"""
)

figure_todo(
    "TODO-FIG-05",
    "dataset_structure.png",
    "بنية المجلدات مقابل ملف data.yaml",
    "الشكل التالي يربط بين ما نراه على القرص وما نكتبه في ملف الإعداد، "
    "وهو أكثر موضع يقع فيه الطلاب في الخطأ عند أول تدريب لهم.",
    """FIGURE TODO-FIG-05  ->  Week7/media/dataset_structure.png
Title: "The folder layout and data.yaml must agree"
Size : 1600 x 900  (two panels)
Style: see the shared style guide in TODO-FIG-01.

LEFT PANEL -- the folder tree, monospace on #ECEFF1:
    dataset/
    |-- data.yaml
    |-- train/
    |   |-- images/     img_001.jpg   img_002.jpg  ...
    |   +-- labels/     img_001.txt   img_002.txt  ...
    |-- valid/
    |   |-- images/
    |   +-- labels/
    +-- test/
        |-- images/
        +-- labels/

  Draw a dashed GREEN (#2E7D32) double-headed arrow connecting
  "img_001.jpg" to "img_001.txt", labelled:
      "same name, different extension"
  This pairing is the single most important idea in the figure.

RIGHT PANEL -- the data.yaml contents, syntax-coloured, monospace:
    path: .
    train: train/images
    val:   valid/images
    test:  test/images

    nc: 4
    names: ["ambulance", "car", "truck", "bus"]

  Draw three grey "-|>" arrows from the words train:, val: and test:
  across to the corresponding folder in the LEFT panel tree.

  Below "names", add an amber callout box:
      "The ORDER defines class_id:
       ambulance=0, car=1, truck=2, bus=3.
       Reordering this line silently corrupts every label file."

BOTTOM NOTE (#616161, 13pt)
  "Ultralytics finds labels by swapping /images/ for /labels/ in the
   path. That is why the two folders must sit side by side."
""",
)

rtl(
    """<h2>3.7 التقسيم train / valid / test</h2>

<p>نقسّم البيانات ثلاثة أقسام، ولكل قسم دور مختلف تماماً:</p>

<ul>
<li><strong>train</strong> (70%): النموذج يراها ويتعلّم منها ويعدّل أوزانه
بناءً عليها.</li>
<li><strong>valid</strong> (20%): النموذج لا يتعلّم منها، لكننا نقيس عليها
بعد كل epoch لنختار أفضل نسخة ونعرف متى نتوقف.</li>
<li><strong>test</strong> (10%): لا تُلمس إلا مرة واحدة في النهاية، لتقدير
نزيه للأداء الحقيقي.</li>
</ul>

<div class="note">
<p><strong>الخطأ الذي يفسد كل شيء:</strong> أن تضع صوراً شديدة التشابه في
<code>train</code> و <code>valid</code> معاً. لو أخذت إطارات متتالية من
فيديو واحد ووزّعتها عشوائياً، فسيرى النموذج في <code>valid</code> صوراً
تكاد تطابق ما حفظه من <code>train</code>، وستحصل على أرقام ممتازة كاذبة.
القاعدة: <strong>قسّم حسب المشهد لا حسب الصورة</strong>.</p>
</div>

<p>في قاعدة بياناتنا كل صورة لقطة مستقلة من مصوّر مختلف، فلا يوجد هذا
الخطر، والتقسيم العشوائي سليم هنا.</p>"""
)

figure_todo(
    "TODO-FIG-06",
    "train_val_test_split.png",
    "دور كل قسم من الأقسام الثلاثة",
    "الشكل التالي يلخّص الأدوار الثلاثة والخطأ الشائع في التقسيم.",
    """FIGURE TODO-FIG-06  ->  Week7/media/train_val_test_split.png
Title: "Three splits, three different jobs"
Size : 1600 x 800
Style: see the shared style guide in TODO-FIG-01.

TOP -- one full-width horizontal bar, height about 90px, split into
three proportional segments with the counts written inside in white:
    70%  #1565C0 blue   "train  -  477 images"
    20%  #F9A825 amber  "valid  -  136 images"
    10%  #2E7D32 green  "test   -   69 images"

MIDDLE -- under each segment, a rounded box with its job:
    train : "The model SEES these and updates its weights."
    valid : "The model never learns from these.
             They choose the best epoch and reveal overfitting."
    test  : "Touched exactly once, at the very end.
             Look at it twice and it stops being honest."

BOTTOM -- a red (#C62828) warning strip across the full width:
    "Never split near-identical images across sets."
  To its left draw three tiny thumbnails of ALMOST IDENTICAL
  consecutive video frames, with arrows sending frame 1 and frame 3
  to "train" and frame 2 to "valid", and a red cross over that
  arrangement. Caption under it, 11pt:
    "The model memorises rather than learns, and your validation
     score becomes a comfortable lie."
""",
)

rtl(
    """<h2>3.8 أخطاء التوسيم الشائعة</h2>

<table>
<thead>
<tr><th>الخطأ</th><th>أثره على النموذج</th></tr>
</thead>
<tbody>
<tr><td>صندوق أوسع من الجسم بكثير</td>
    <td>يتعلّم النموذج أن الخلفية جزء من الجسم</td></tr>
<tr><td>صندوق أضيق يقصّ أطراف الجسم</td>
    <td>يتعلّم أجساماً ناقصة ويفشل على الكاملة</td></tr>
<tr><td>جسم موجود لكنه غير موسوم</td>
    <td>الأسوأ على الإطلاق: نعاقب النموذج حين يكون محقاً</td></tr>
<tr><td>الجسم نفسه موسوم بفئتين</td>
    <td>إشارتان متناقضتان على البكسلات نفسها</td></tr>
<tr><td>صندوق واحد يغطي مجموعة أجسام</td>
    <td>يتعلّم النموذج أن الكتلة جسم واحد</td></tr>
<tr><td>توسيم رسم أو صورة داخل صورة</td>
    <td>يتعلّم أن اللوحات والإعلانات مركبات حقيقية</td></tr>
<tr><td>تسمية غير متسقة بين الموسِّمين</td>
    <td>حدود الفئات تصبح ضبابية</td></tr>
<tr><td>تجاهل الأجسام المحجوبة جزئياً</td>
    <td>يفشل النموذج في الازدحام، وهو أهم ما نحتاجه</td></tr>
<tr><td>نسيان تبديل الصيغة إلى YOLO</td>
    <td>ملفات XML لا تقرأها Ultralytics إطلاقاً</td></tr>
<tr><td>تغيير ترتيب الفئات بعد التوسيم</td>
    <td>كل ملفات التوسيم تصبح خاطئة صامتةً</td></tr>
</tbody>
</table>

<div class="note">
<p>الأخطاء الثلاثة الأخيرة في الجدول واجهناها فعلياً أثناء تجهيز قاعدة
بيانات هذا الدرس، وسنرى أثرها في القسم التالي.</p>
</div>

<h2>3.9 من أين نحصل على قواعد بيانات جاهزة؟</h2>

<p>توسيم قاعدة بيانات من الصفر عمل طويل. لحسن الحظ توجد مستودعات كبيرة
فيها قواعد بيانات موسومة جاهزة:</p>

<table>
<thead>
<tr><th>المصدر</th><th>ماذا يقدّم</th><th>كيف يعمل</th></tr>
</thead>
<tbody>
<tr>
  <td><a href="https://universe.roboflow.com/">Roboflow Universe</a></td>
  <td>عشرات الآلاف من قواعد بيانات الكشف الجاهزة بصيغة YOLO</td>
  <td>تختار مشروعاً، وتولّد منه نسخة (version) بالتعزيز الذي تريده، ثم
      تصدّرها بصيغة YOLOv8 عبر رابط مباشر أو حزمة <code>roboflow</code>
      مع مفتاح API مجاني</td>
</tr>
<tr>
  <td><a href="https://storage.googleapis.com/openimages/web/index.html">Open Images</a></td>
  <td>نحو 600 فئة بصناديق موسومة يدوياً على صور حقيقية، ومنها
      <code>Ambulance</code></td>
  <td>تنزّل ملفات التوسيم CSV وتصفّيها بالفئة، ثم تنزّل الصور المطلوبة
      فقط وتحوّلها إلى صيغة YOLO. بلا مفاتيح ولا تسجيل</td>
</tr>
<tr>
  <td><a href="https://www.kaggle.com/datasets">Kaggle Datasets</a></td>
  <td>مجموعات متنوعة جداً، لكن كثيراً منها للتصنيف لا للكشف</td>
  <td>تنزيل يدوي، أو عبر أداة <code>kaggle</code> بملف اعتماد
      <code>kaggle.json</code></td>
</tr>
<tr>
  <td><a href="https://huggingface.co/datasets">Hugging Face</a></td>
  <td>مرايا لمجموعات كثيرة ومجموعات مجتمعية</td>
  <td>عبر حزمة <code>huggingface_hub</code> أو تنزيل مباشر</td>
</tr>
<tr>
  <td><a href="https://cocodataset.org/">COCO</a></td>
  <td>الثمانون فئة العامة التي تدرّب عليها نموذجنا الجاهز</td>
  <td>مرجعي في درسنا: هو مصدر المشكلة لا الحل</td>
</tr>
</tbody>
</table>

<div class="note">
<p><strong>قبل أن تستخدم أي مجموعة، تحقق من أمرين:</strong></p>
<ol>
<li><strong>الرخصة.</strong> هل يُسمح بالاستخدام التعليمي؟ التجاري؟ هل
يجب نسب المصدر؟</li>
<li><strong>جودة التوسيم.</strong> افتح عشرين صورة وانظر إلى صناديقها
بعينك قبل أن تدرّب. عدد كبير من المجموعات المنشورة توسيمها رديء.</li>
</ol>
</div>

<h2>3.10 قاعدة بياناتنا: من أين جاءت وماذا فيها</h2>

<p>قاعدة بيانات هذا الدرس مستخرجة من <strong>Open Images V6/V7</strong>
من Google. اخترناها لأن:</p>

<ul>
<li>الفئة <code>Ambulance</code> موجودة فيها بصناديق موسومة يدوياً على
صور شوارع حقيقية.</li>
<li>الصور برخصة CC BY 2.0 والتوسيم برخصة CC BY 4.0، فيمكن إعادة نشرها
في مستودع تعليمي مفتوح.</li>
<li>التنزيل لا يحتاج حساباً ولا مفتاحاً.</li>
</ul>

<p>تفاصيل الرخصة وخطوات التحويل كاملة في <code>dataset/LICENSE.md</code>،
وسكربت التحويل في <code>tools/prepare_week7_dataset.py</code>.</p>

<p>لنفحصها برمجياً:</p>"""
)

code(
    '''with open("dataset/data.yaml") as handle:
    data_config = yaml.safe_load(handle)

CLASS_NAMES = data_config["names"]
print("الفئات:", CLASS_NAMES)
print()

# نعدّ الصناديق لكل فئة في كل قسم
summary = {}

for split in ["train", "valid", "test"]:
    counts = Counter()
    for label_file in (Path("dataset") / split / "labels").glob("*.txt"):
        for line in label_file.read_text().split("\\n"):
            if line.strip():
                counts[CLASS_NAMES[int(line.split()[0])]] += 1
    summary[split] = counts

distribution = pd.DataFrame(summary).fillna(0).astype(int)
distribution.loc["المجموع"] = distribution.sum()
distribution'''
)

rtl(
    """<p>لننظر أيضاً إلى أحجام الصناديق، فهي تخبرنا هل الأجسام كبيرة
وقريبة أم صغيرة وبعيدة، وهذا يؤثر على اختيار <code>imgsz</code> لاحقاً.</p>"""
)

code(
    '''box_areas = []

for label_file in Path("dataset/train/labels").glob("*.txt"):
    for line in label_file.read_text().split("\\n"):
        if line.strip():
            _, _, _, w, h = line.split()
            box_areas.append(float(w) * float(h))

box_areas = np.array(box_areas)

print(f"عدد الصناديق: {len(box_areas)}")
print(f"وسيط مساحة الصندوق: {np.median(box_areas) * 100:.1f}% من مساحة الصورة")
print(f"أصغر صندوق: {box_areas.min() * 100:.2f}%")
print(f"أكبر صندوق: {box_areas.max() * 100:.1f}%")

plt.figure(figsize=(9, 4))
plt.hist(np.sqrt(box_areas), bins=40, color="#1565C0")
plt.xlabel("Relative box size (sqrt of area fraction)")
plt.ylabel("Number of boxes")
plt.title("How big are the objects in our dataset?")
plt.show()'''
)

rtl(
    """<p>وأخيراً، أهم فحص على الإطلاق: أن ننظر إلى التوسيم بأعيننا. لا
تدرّب أبداً على قاعدة بيانات لم تر صناديقها.</p>"""
)

code(
    '''BOX_COLORS = {
    "ambulance": (198, 40, 40),
    "car": (21, 101, 192),
    "truck": (46, 125, 50),
    "bus": (249, 168, 37),
}

sample_paths = sorted(Path("dataset/train/images").glob("*.jpg"))[:6]

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

for ax, image_path in zip(axes.flat, sample_paths):
    image = cv2.cvtColor(cv2.imread(str(image_path)), cv2.COLOR_BGR2RGB)
    height, width = image.shape[:2]

    label_path = Path("dataset/train/labels") / (image_path.stem + ".txt")

    for line in label_path.read_text().split("\\n"):
        if not line.strip():
            continue

        class_id, xc, yc, bw, bh = line.split()
        class_name = CLASS_NAMES[int(class_id)]
        xc, yc, bw, bh = float(xc), float(yc), float(bw), float(bh)

        p1 = (int((xc - bw / 2) * width), int((yc - bh / 2) * height))
        p2 = (int((xc + bw / 2) * width), int((yc + bh / 2) * height))

        cv2.rectangle(image, p1, p2, BOX_COLORS[class_name], 2)
        cv2.putText(
            image,
            class_name,
            (p1[0], max(p1[1] - 6, 12)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            BOX_COLORS[class_name],
            2,
            cv2.LINE_AA,
        )

    ax.imshow(image)
    ax.axis("off")

plt.suptitle("Ground truth annotations from our dataset", fontsize=16)
plt.tight_layout()
plt.show()'''
)


# ===========================================================================
# الكتابة
# ===========================================================================

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3.11"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(notebook, ensure_ascii=False, indent=1))

n_md = sum(1 for c in cells if c["cell_type"] == "markdown")
n_code = sum(1 for c in cells if c["cell_type"] == "code")
print(f"كُتب {OUT}: {len(cells)} خلية ({n_md} markdown، {n_code} code)")
