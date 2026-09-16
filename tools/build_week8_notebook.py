#!/usr/bin/env python3
"""
يبني هيكل دفتر الأسبوع 8: الشارة، النمط والعنوان، الأهداف، المحتويات،
التهيئة (pip + استنساخ المستودع + الاستيرادات + الجهاز + تحميل النموذج)،
ثم عناوين الأقسام 1-18 فارغة (بلا محتوى بعد).

يُبنى الدفتر من سكربت بدل التحرير اليدوي حتى نضمن تناسق تغليف RTL في كل
خلية، ونتمكن من إعادة التوليد لاحقاً. المحتوى الكامل لكل قسم يُضاف لاحقاً
عبر سكربتات append_week8_*.py على نمط tools/append_week7_sections.py:
تبحث عن عنوان القسم كعلامة، تحذف كل ما بعده، ثم تعيد إلحاقه بعد الإضافة،
فتبقى قابلة لإعادة التشغيل دون إتلاف تعديلات المؤلف اليدوية على الأقسام
السابقة.

الاستخدام:
    python tools/build_week8_notebook.py
"""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path("Week8/week_8_object_tracking.ipynb")
MIRROR_BASE = "https://raw.githubusercontent.com/syriascitech/Medad-CV-Bootcamp/main/Week8/media"
COLAB_URL = (
    "https://colab.research.google.com/github/syriascitech/Medad-CV-Bootcamp/"
    "blob/main/Week8/week_8_object_tracking.ipynb"
)

# نفس كتلة النمط المستخدمة في الأسبوع 7 حرفياً.
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


def _cell(kind: str, text: str) -> dict:
    cell: dict = {
        "cell_type": kind,
        "metadata": {},
        "source": [line + "\n" for line in text.split("\n")],
    }
    if kind == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell


def rtl(body: str) -> None:
    """خلية markdown عربية مغلَّفة بـ div dir=rtl."""
    cells.append(_cell("markdown", f"{RTL_OPEN}\n\n{body.strip()}\n\n{RTL_CLOSE}"))


def code(src: str) -> None:
    cells.append(_cell("code", src.strip()))


def raw_markdown(text: str) -> None:
    """خلية markdown بلا تغليف RTL، للشارة أو صور مستقلة عن النص العربي."""
    cells.append(_cell("markdown", text.strip()))


def figure(number: int, filename: str, alt: str, width: int = 900) -> None:
    """
    شكل بصيغة <img> محلية أولاً مع مرجع احتياطي على المرآة العامة، حسب
    الشكل المطلوب في HANDOFF.md #5.2. يعمل حتى لو لم تُنتَج الصورة بعد:
    يظهر أيقونة صورة معطوبة بدل خطأ، ولا يكسر شيئاً.
    """
    raw_markdown(
        f"""<div style="text-align:center; margin:24px 0;">
<img
src="media/{filename}"
onerror="this.onerror=null;this.src='{MIRROR_BASE}/{filename}';"
alt="Figure {number} - {alt}"
width="{width}">
</div>"""
    )


def section_stub(number: int, title: str) -> None:
    """رأس قسم فارغ، يُملأ لاحقاً عبر append_week8_*.py الذي يبحث عن هذا
    العنوان بالذات كعلامة."""
    rtl(f"""<hr />\n<h1>{number}. {title}</h1>""")


# ===========================================================================
# قائمة عناوين الأقسام 1-18 (تُستخدم هنا وفي المحتويات، فيتطابق العددان
# دائماً - القاعدة 5.8 في HANDOFF).
# ===========================================================================

SECTIONS = [
    "لماذا الكشف وحده لا يكفي؟",
    "تعريف المشكلة: التتبع متعدد الأجسام Multi-Object Tracking",
    "الربط بين الإطارات Data Association",
    "التنبؤ بالحركة: مرشّح كالمان Kalman Filter",
    "SORT",
    "DeepSORT: إضافة المظهر",
    "ByteTrack: الفكرة البسيطة الذكية",
    "عملياً مع Ultralytics",
    "نبني متتبع IoU مصغّراً من الصفر",
    "رسم المسارات Trails وتلوين حسب الـ ID",
    "تشغيل على المقطع الكامل وحفظ الناتج",
    "لمحة أولى: كيف يفتح التتبع باب العدّ؟",
    "متى يفشل المتتبع؟",
    "كيف نقيس جودة التتبع؟",
    "تمرين صفي",
    "أسئلة مراجعة سريعة",
    "بنك أسئلة Kahoot",
    "الخلاصة",
]

assert len(SECTIONS) == 18


# ===========================================================================
# 0 : شارة Colab
# ===========================================================================

raw_markdown(f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB_URL})")


# ===========================================================================
# 1 : النمط + العنوان
# ===========================================================================

cells.append(
    _cell(
        "markdown",
        STYLE
        + "\n"
        + RTL_OPEN
        + """

<h1>الأسبوع 8: تتبع الأجسام</h1>
<h2>Object Tracking</h2>
<hr />
<p><strong>مسار أنظمة المرور الذكية – الرؤية الحاسوبية</strong></p>
<p><strong>المُعد/المؤلف:</strong> المهندس عامر صوان والمهندس حسن صوان</p>
<hr />

<p>في الأسبوع الماضي درّبنا نموذج YOLO على التعرّف على سيارات الإسعاف إلى
جانب السيارات والشاحنات والحافلات. حصلنا على نموذج يجيب بثقة عن سؤالين في
كل إطار على حدة: <strong>ما هذا؟</strong> و<strong>أين هو؟</strong></p>

<p>لكن جرّب هذا السؤال: كم مركبة عبرت التقاطع في آخر دقيقة؟ النموذج وحده لا
يستطيع الإجابة، لأنه <strong>ينسى كل شيء بين إطار وإطار</strong>. لا يعرف أن
سيارة الإسعاف التي رآها في الإطار العاشر هي نفسها التي رآها في الإطار
التاسع. كل إطار بالنسبة له عالم جديد كلياً.</p>

<p>هذا الأسبوع نحلّ هذه المشكلة بـ<strong>التتبع Object Tracking</strong>:
نعطي كل جسم رقماً ثابتاً يلازمه عبر الإطارات، فنستطيع أخيراً الإجابة عن
أسئلة مثل "كم مركبة عبرت؟" و"هل هذا الإسعاف يقترب أم يبتعد؟" - وهذا بالضبط
ما يحتاجه الأسبوع التاسع لبناء منطق أولوية الإشارة.</p>

<div class="note">
<p><strong>كيف يُقرأ هذا الدفتر:</strong> أُعدّ هذا الدفتر وشُغِّل بالكامل
على Google Colab مسبقاً، والمخرجات المحفوظة أمامك هي نتائج حقيقية لا
توقُّعات. في الحصة نفتحه ونقرأه معاً دون تشغيل أي خلية. إن أردت تشغيله
بنفسك في البيت، اضغط شارة Colab أعلى الدفتر وشغّله من الأعلى للأسفل على
جهاز جديد كلياً.</p>
</div>

"""
        + RTL_CLOSE,
    )
)


# ===========================================================================
# 2-3 : الأهداف والمحتويات
# ===========================================================================

rtl(
    """<h2>أهداف الدرس</h2>

<p>في نهاية هذا الدرس ستكون قادراً على أن:</p>

<ol>
<li>تشرح لماذا لا يكفي الكشف وحده للإجابة عن أسئلة تراكمية مثل العدّ.</li>
<li>تفرّق بين <strong>Detection</strong> و <strong>Track</strong> و
<strong>ID</strong>، وتشرح فلسفة Tracking-by-Detection.</li>
<li>تحسب <strong>IoU</strong> بين صندوقين وتبني مصفوفة تكلفة، وتفهم متى
تفشل المطابقة الجشعة (Greedy Matching).</li>
<li>تشرح بحدسٍ سليم كيف يتنبأ <strong>مرشّح كالمان</strong> بموضع جسم أثناء
الحجب Occlusion.</li>
<li>تقارن بين SORT و DeepSORT و ByteTrack: ماذا يضيف كل واحد، وبأي ثمن.</li>
<li>تشغّل <code>model.track()</code> في Ultralytics وتقرأ معرّفات
التتبع من نتائجه.</li>
<li>تبني متتبعاً مبسّطاً بأيدينا وتشاهد <strong>تبديل هوية ID Switch</strong>
يحدث أمامك، فتفهم لماذا نحتاج ما هو أذكى من المطابقة الجشعة.</li>
<li>تشخّص أعطال التتبع الشائعة: تبديل الهوية، التجزّؤ، والمسارات الوهمية.</li>
</ol>"""
)

rtl(
    "<h2>محتويات الدرس</h2>\n\n<ol>\n"
    + "\n".join(f"<li>{title}</li>" for title in SECTIONS)
    + "\n</ol>"
)


# ===========================================================================
# 4-13 : التهيئة (pip، استنساخ، مكتبات، استيرادات، جهاز، تحميل النموذج)
# ===========================================================================

rtl("""<hr />\n<h1>التهيئة</h1>""")

rtl(
    """<p>هذا الدفتر يعمل على <strong>Google Colab</strong>: يحتاج إنترنت
لتثبيت المكتبات ولاستنساخ ملفات هذا الدرس مرة واحدة عند بداية كل جلسة
Colab جديدة. الخلية التالية تثبّت المكتبات بصمت.</p>"""
)

code(
    '''import sys

!{sys.executable} -m pip install -q ultralytics opencv-python pandas matplotlib pyyaml numpy scipy imageio-ffmpeg
!{sys.executable} -m pip install -q torch torchvision'''
)

rtl(
    """<p>جلسة Colab الجديدة لا تملك أياً من ملفات هذا الدرس: الفيديوهات
والنموذج المدرَّب والأشكال. الخلية التالية تستنسخ المستودع مرة واحدة فقط،
ولا تفعل شيئاً إن كانت الملفات موجودة أصلاً (كأن تشغّل الدفتر محلياً من
داخل مجلد <code>Week8</code>).</p>"""
)

code(
    '''import os
from pathlib import Path

# على Colab لا توجد ملفات المستودع، فننسخها مرة واحدة.
if not Path("videos").exists() and not Path("models/emergency_best.pt").exists():
    !git clone -q https://github.com/syriascitech/Medad-CV-Bootcamp.git /content/repo
    os.chdir("/content/repo/Week8")

print("مجلد العمل:", os.getcwd())'''
)

code(
    '''import importlib.util

REQUIRED = ["ultralytics", "cv2", "torch", "pandas", "matplotlib", "yaml", "scipy"]

missing = [name for name in REQUIRED if importlib.util.find_spec(name) is None]

if missing:
    print("المكتبات الناقصة:", "، ".join(missing))
    print("أعد تشغيل الخلية الأولى في هذا القسم، ثم أعد تشغيل النواة.")
else:
    print("كل المكتبات المطلوبة متوفرة.")'''
)

rtl(
    """<h2>الاستيرادات وإعدادات العمل</h2>

<p>مكتبة Ultralytics تحاول الاتصال بالإنترنت في أكثر من موضع حتى أثناء
الاستدلال: لتحميل الأوزان إن لم تجدها محلياً، ولإرسال إحصاءات استخدام.
الخلية التالية تشير إلى نسخة النموذج المحفوظة محلياً وتُسكِت هذه المحاولات.
كما تضبط دقة الرسوم البيانية لإبقاء حجم هذا الدفتر معقولاً رغم أنه يُحفظ
بكل مخرجاته.</p>"""
)

code(
    '''import os

# يمنع تعارض OpenMP بين Ultralytics و OpenCV على بعض الأجهزة.
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["YOLO_VERBOSE"] = "False"

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from scipy.optimize import linear_sum_assignment

from ultralytics import YOLO, settings

settings.update({"sync": False})  # إيقاف إرسال إحصاءات الاستخدام

# دقة معتدلة لكل الرسوم البيانية، فلا يتضخّم حجم الدفتر مع عشرات المخرجات.
plt.rcParams["figure.dpi"] = 90

MODEL_PATH = "models/emergency_best.pt"  # مسار محلي: لا تحميل من الإنترنت

print("PyTorch:", torch.__version__)
print("النموذج:", MODEL_PATH)'''
)

rtl(
    """<h2>الجهاز المستخدم</h2>

<p>على Colab غالباً يتوفّر كرت شاشة T4 مجاني. إن كنت تشغّل هذا الدفتر
محلياً على معالج فقط، ستعمل كل الخلايا لكنها ستستغرق وقتاً أطول - القيم
القصوى للإطارات في هذا الدرس مضبوطة لتبقى معقولة على المعالج أيضاً.</p>"""
)

code(
    '''DEVICE = 0 if torch.cuda.is_available() else "cpu"

print("الجهاز المستخدم:", DEVICE)
print("عدد أنوية المعالج المتاحة:", os.cpu_count())'''
)

rtl(
    """<h2>تحميل النموذج المدرَّب من الأسبوع السابع</h2>

<p>هذا هو النموذج نفسه الذي درَّبناه الأسبوع الماضي على أربع فئات، ونسخناه
هنا في <code>Week8/models/</code> ليعمل هذا الدرس بشكل مستقل. لن ندرّب أي
شيء اليوم - سنستخدم هذا النموذج كما هو، ونضيف عليه القدرة على التتبع.</p>"""
)

code(
    '''model = YOLO(MODEL_PATH)

print("الفئات التي يعرفها النموذج:", model.names)
print("عدد الفئات:", len(model.names))'''
)


# ===========================================================================
# عناوين الأقسام 1-18 (فارغة بعد - تُملأ عبر append_week8_*.py)
# ===========================================================================

for index, title in enumerate(SECTIONS, start=1):
    section_stub(index, title)


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
