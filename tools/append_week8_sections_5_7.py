#!/usr/bin/env python3
"""
يملأ الأقسام 5-7 من دفتر الأسبوع 8 (SORT، DeepSORT، ByteTrack)، بين عنوان
القسم الخامس وعنوان القسم الثامن.

قابل لإعادة التشغيل: يبحث عن عنوان القسم 5 وعنوان القسم 8 كعلامتين،
ويستبدل كل ما بينهما بالمحتوى الجديد.

الاستخدام:
    python tools/append_week8_sections_5_7.py
"""

from __future__ import annotations

import json
from pathlib import Path

NOTEBOOK = Path("Week8/week_8_object_tracking.ipynb")
START_MARKER = "<h1>5. SORT</h1>"
END_MARKER = "<h1>8. عملياً مع Ultralytics</h1>"

RTL_OPEN = '<div dir="rtl" class="rtl-cell" style="direction:rtl; text-align:right;">'
RTL_CLOSE = "</div>"
MIRROR_BASE = "https://raw.githubusercontent.com/syriascitech/Medad-CV-Bootcamp/main/Week8/media"

new_cells: list[dict] = []


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
    new_cells.append(_cell("markdown", f"{RTL_OPEN}\n\n{body.strip()}\n\n{RTL_CLOSE}"))


def code(src: str) -> None:
    new_cells.append(_cell("code", src.strip()))


def figure(number: int, filename: str, alt: str, width: int = 900) -> None:
    new_cells.append(
        _cell(
            "markdown",
            f"""<div style="text-align:center; margin:24px 0;">
<img
src="media/{filename}"
onerror="this.onerror=null;this.src='{MIRROR_BASE}/{filename}';"
alt="Figure {number} - {alt}"
width="{width}">
</div>""",
        )
    )


# ===========================================================================
# 5. SORT
# ===========================================================================

rtl(
    """<hr />
<h1>5. SORT</h1>

<p><strong>SORT</strong> (Simple Online and Realtime Tracking) هو أبسط
متتبع عملي، ويجمع كل ما تعلّمناه في القسمين السابقين: كشف، ثم مرشّح كالمان
للتنبؤ، ثم Hungarian للربط. يستحق دراسته لأن كل متتبع أحدث - بما فيها
ByteTrack التي سنستخدمها فعلياً - هو تطوير على هيكله الأساسي.</p>

<h2>5.1 خط الأنابيب كاملاً</h2>

<p>في كل إطار جديد، تمرّ دورة SORT بخطوات ثابتة:</p>

<ol>
<li><strong>Detect</strong>: شغّل الكاشف على الإطار الحالي، فتحصل على قائمة
صناديق.</li>
<li><strong>Predict</strong>: لكل مسار موجود من الإطار السابق، اطلب من
مرشّح كالمان الخاص به موضعه المتوقَّع في هذا الإطار.</li>
<li><strong>Associate</strong>: ابنِ مصفوفة تكلفة IoU بين المواضع
المتوقَّعة والاكتشافات الجديدة، وحلّها بخوارزمية Hungarian.</li>
<li><strong>Update</strong>: كل مسار ارتُبط بكشف يُحدَّث موضعه وسرعته
الحقيقية من ذلك الكشف.</li>
<li><strong>Create</strong>: كل كشف لم يُربَط بأي مسار يبدأ مساراً جديداً
مرشّحاً (Tentative).</li>
<li><strong>Delete</strong>: كل مسار لم يُربَط بأي كشف لفترة طويلة جداً
يُحذف نهائياً.</li>
</ol>

<p>لاحظ أن هذه الدورة هي حرفياً تجميع للأدوات الثلاث من الأقسام 3 و 4:
IoU، Hungarian، ومرشّح كالمان. SORT لا يضيف فكرة جديدة، بل يرتّب الأفكار
الموجودة في خط إنتاج واحد متكرر.</p>"""
)

figure(5, "sort_pipeline.jpg", "The full SORT pipeline: detect, predict, associate, update, create, delete")

rtl(
    """<h2>5.2 دورة حياة المسار: min_hits و max_age</h2>

<p>لا يصبح كل مسار جديد "رسمياً" فوراً، ولا يُحذف كل مسار فقد كشفاً واحداً.
معاملان يضبطان هذا التوازن:</p>

<ul>
<li><strong><code>min_hits</code></strong>: عدد الإطارات المتتالية التي
يجب أن يُطابَق فيها المسار الجديد قبل أن يُعتبر "مؤكَّداً" ويُعرَض
بهويته. يمنع هذا كشفاً عابراً وهمياً (Flicker) من الحصول على هوية دائمة.</li>
<li><strong><code>max_age</code></strong>: عدد الإطارات التي يُسمح للمسار
بالبقاء بلا أي كشف مطابق قبل حذفه نهائياً. رفعه يمنح المسار فرصة أطول
للنجاة من حجب طويل، لكنه أيضاً يُبقي مسارات وهمية حيّة لفترة أطول.</li>
</ul>"""
)

figure(6, "track_lifecycle_state_machine.jpg", "Track lifecycle state machine: Tentative to Confirmed to Deleted")

rtl(
    """<h2>5.3 نقطة ضعف SORT: تبديل الهوية</h2>

<p>SORT يعتمد <strong>على الحركة فقط</strong>: IoU وموضع متوقَّع من مرشّح
كالمان. لا معلومة عن شكل الجسم أو لونه إطلاقاً. هذا يكفي في أغلب الحالات،
لكنه ينهار في حالة شائعة: <strong>جسمان متشابهان يتقاطعان أو يتقاربان
بشدة</strong>. حين تتداخل الصناديق المتوقَّعة لجسمين قريبين، قد تربط
Hungarian كل مسار بالكشف الخطأ - فتتبادل السيارتان هويتيهما دون أن يخطئ
أي جزء من الخوارزمية على حدة.</p>

<p>هذا يُسمّى <strong>ID Switch</strong>، وهو المقياس الذي سنراه لاحقاً في
القسم 14، وهو بالضبط ما يدفعنا لدراسة DeepSORT وByteTrack.</p>"""
)

figure(7, "id_switch_example.jpg", "An ID switch: two similar objects crossing paths swap identities")


# ===========================================================================
# 6. DeepSORT
# ===========================================================================

rtl(
    """<hr />
<h1>6. DeepSORT: إضافة المظهر</h1>

<h2>6.1 تمثيلات Re-ID</h2>

<p>فكرة DeepSORT مباشرة: بما أن الحركة وحدها لا تكفي لتمييز جسمين
متشابهين، أضِف معلومة <strong>شكل الجسم نفسه</strong>. لكل صندوق كشف، مرّره
عبر شبكة عصبية صغيرة مدرَّبة خصيصاً لهذه المهمة (تسمى شبكة Re-ID)، فتنتج
<strong>متجه سمات (Embedding)</strong> - مجموعة أرقام تلخّص لون الجسم
وملمسه وشكله العام. سيارتان بيضاوان متجاورتان قد تتشابه صندوقاهما، لكن
متجهيهما سيختلفان قليلاً إن اختلف الطراز أو زاوية الإضاءة.</p>

<h2>6.2 التكلفة المُركَّبة</h2>

<p>بدل الاعتماد على IoU وحدها في مصفوفة التكلفة، يجمع DeepSORT بين
مصدرين:</p>

<ul>
<li><strong>تكلفة الحركة</strong>: المسافة بين الموضع المتوقَّع من مرشّح
كالمان والكشف الجديد (تماماً كما في SORT).</li>
<li><strong>تكلفة المظهر</strong>: المسافة (عادة Cosine Distance) بين
متجه سمات الكشف الجديد ومتوسط متجهات المسار من الإطارات الأخيرة.</li>
</ul>

<p>حين تتقاطع حركتا جسمين فتصبح تكلفة الحركة متعادلة تقريباً بينهما، تكسر
تكلفة المظهر التعادل: الجسم الأبيض يبقى مرتبطاً بمتجه المظهر الأبيض حتى
لو تشابهت موضعيهما لحظياً.</p>

<h2>6.3 الثمن: السرعة</h2>

<p>هذه القوة الإضافية ليست مجانية. تشغيل شبكة Re-ID على <strong>كل صندوق
مكتشَف في كل إطار</strong> يضيف عبء استدلال حقيقياً فوق عبء الكاشف نفسه.
على معالج ضعيف أو مع عدد كبير من الأجسام في المشهد، قد يتحوّل هذا العبء
الإضافي إلى عنق الزجاجة الفعلي للنظام بأكمله - وهو ثمن قد لا يستحقه مشهد
بسيط لا تتقاطع فيه الأجسام كثيراً.</p>"""
)


# ===========================================================================
# 7. ByteTrack
# ===========================================================================

rtl(
    """<hr />
<h1>7. ByteTrack: الفكرة البسيطة الذكية</h1>

<h2>7.1 المشكلة: نرمي الاكتشافات الضعيفة</h2>

<p>تذكّر الأسبوع الماضي: نضبط عتبة <code>conf</code> لنتجاهل الاكتشافات
الضعيفة الثقة، لأن أغلبها إنذارات كاذبة. لكن هذا القرار له ثمن خفي في
التتبع: حين يبدأ جسم حقيقي بالاختفاء تدريجياً خلف حاجز، لا تسقط ثقة
الكاشف به إلى صفر فجأة - بل تنخفض تدريجياً (0.9 ثم 0.6 ثم 0.3...) قبل أن
تختفي تماماً. تلك الاكتشافات الضعيفة في المنتصف <strong>حقيقية غالباً</strong>،
لكن SORT وDeepSORT يرميانها فوراً لأنها تحت العتبة - أي يفقدان الجسم في
اللحظة التي يحتاجان فيها أكثر ما يحتاجان إلى أي دليل عليه.</p>

<h2>7.2 الربط على مرحلتين</h2>

<p>فكرة ByteTrack بسيطة وذكية: <strong>لا ترمِ شيئاً، واستخدمه في مرحلة
ثانية.</strong></p>

<ol>
<li><strong>المرحلة الأولى</strong>: اربط المسارات بالاكتشافات
<strong>عالية الثقة</strong> فقط، بنفس طريقة SORT تماماً.</li>
<li><strong>المرحلة الثانية</strong>: خذ المسارات التي <strong>لم</strong>
تُربَط في المرحلة الأولى (مرشَّحة لأن تكون محجوبة)، وحاول ربطها بالاكتشافات
<strong>منخفضة الثقة</strong> التي رميناها في الطرق التقليدية - باستخدام
IoU فقط، دون شرط الثقة إطلاقاً.</li>
</ol>

<p>النتيجة: مسار كان سيُحذف في المرحلة الأولى (لعدم وجود كشف عالي الثقة
يطابقه) يحصل على فرصة أخيرة في المرحلة الثانية، بدليل ضعيف لكنه أفضل من
لا شيء.</p>"""
)

figure(8, "bytetrack_two_stage.jpg", "ByteTrack's two-stage association: high-confidence first, then low-confidence recovery")

rtl(
    """<h2>7.3 لماذا ينجو من الحجب</h2>

<p>هذا يحل بالضبط المشكلة التي واجهناها في القسم 4: الحجب الجزئي (لا
الكلي) ينتج اكتشافات ضعيفة الثقة لا اكتشافات معدومة. ByteTrack يستغل هذه
المنطقة الرمادية بدل تجاهلها، فيمدّد عمر المسار عبر لحظات الحجب الجزئي
دون الحاجة إلى شبكة Re-ID مكلفة كما في DeepSORT - وهذا سرّ شعبيته: يحسّن
النجاة من الحجب بسرعة SORT نفسها تقريباً.</p>

<h2>7.4 مقارنة: SORT مقابل DeepSORT مقابل ByteTrack مقابل BoT-SORT</h2>

<table>
<thead>
<tr><th></th><th>SORT</th><th>DeepSORT</th><th>ByteTrack</th><th>BoT-SORT</th></tr>
</thead>
<tbody>
<tr><td>مصدر الربط</td><td>حركة (IoU)</td><td>حركة + مظهر (Re-ID)</td>
    <td>حركة (IoU) على مرحلتين</td><td>حركة + تعويض حركة الكاميرا، ومظهر اختياري</td></tr>
<tr><td>يستخدم اكتشافات ضعيفة الثقة</td><td>لا</td><td>لا</td>
    <td>نعم - هذا جوهر الفكرة</td><td>نعم (موروث من ByteTrack)</td></tr>
<tr><td>مقاومة تبديل الهوية</td><td>ضعيفة</td><td>جيدة</td>
    <td>جيدة</td><td>الأفضل عادة</td></tr>
<tr><td>السرعة</td><td>الأسرع</td><td>أبطأ (عبء Re-ID)</td>
    <td>سريع، قريب من SORT</td><td>سريع، أبطأ قليلاً إن فُعِّل Re-ID</td></tr>
<tr><td>ماذا يضيف فوق سابقه</td><td>-</td><td>المظهر</td>
    <td>استغلال الاكتشافات الضعيفة</td><td>تعويض حركة الكاميرا + مظهر اختياري</td></tr>
</tbody>
</table>

<div class="note">
<p>مكتبة Ultralytics التي سنستخدمها في القسم التالي تشحن ByteTrack
و BoT-SORT جاهزين (<code>bytetrack.yaml</code> و <code>botsort.yaml</code>)،
ولن نحتاج إلى تنزيل أي شيء إضافي لتجربتهما.</p>
</div>"""
)


# ===========================================================================
# الدمج مع الدفتر الموجود
# ===========================================================================


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    cells = notebook["cells"]

    def source_of(cell: dict) -> str:
        return "".join(cell["source"])

    start_idx = next(i for i, c in enumerate(cells) if START_MARKER in source_of(c))
    end_idx = next(
        i for i, c in enumerate(cells) if i > start_idx and END_MARKER in source_of(c)
    )

    cells[start_idx:end_idx] = new_cells
    NOTEBOOK.write_text(json.dumps(notebook, ensure_ascii=False, indent=1))

    n_md = sum(1 for c in cells if c["cell_type"] == "markdown")
    n_code = sum(1 for c in cells if c["cell_type"] == "code")
    print(f"{NOTEBOOK}: {len(cells)} خلية ({n_md} markdown، {n_code} code)")
    print(f"استُبدلت الأقسام 5-7 بـ {len(new_cells)} خلية.")


if __name__ == "__main__":
    main()
