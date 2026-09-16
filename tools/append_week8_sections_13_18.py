#!/usr/bin/env python3
"""
يملأ الأقسام 13-18 من دفتر الأسبوع 8 (متى يفشل المتتبع، قياس الجودة،
تمرين صفي، أسئلة مراجعة، بنك Kahoot، الخلاصة)، من عنوان القسم 13 حتى
نهاية الدفتر.

قابل لإعادة التشغيل: يبحث عن عنوان القسم 13 كعلامة بداية، ويحذف كل ما
بعده (لا يوجد قسم تالٍ لأنه آخر الدفتر)، ثم يلحق المحتوى الجديد.

الاستخدام:
    python tools/append_week8_sections_13_18.py
"""

from __future__ import annotations

import json
from pathlib import Path

NOTEBOOK = Path("Week8/week_8_object_tracking.ipynb")
START_MARKER = "<h1>13. متى يفشل المتتبع؟</h1>"

RTL_OPEN = '<div dir="rtl" class="rtl-cell" style="direction:rtl; text-align:right;">'
RTL_CLOSE = "</div>"

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


# ===========================================================================
# 13. متى يفشل المتتبع؟
# ===========================================================================

rtl(
    """<hr />
<h1>13. متى يفشل المتتبع؟</h1>

<h2>13.1 ثلاثة أنواع فشل مختلفة</h2>

<table>
<thead>
<tr><th>النوع</th><th>ماذا يحدث</th><th>رأيناه فعلياً في</th></tr>
</thead>
<tbody>
<tr>
  <td><strong>تبديل الهوية ID Switch</strong></td>
  <td>جسمان يتبادلان هويتيهما عند التقاطع أو الاقتراب الشديد</td>
  <td>القسم 5.3 (SORT، نظرياً)</td>
</tr>
<tr>
  <td><strong>التجزّؤ Fragmentation</strong></td>
  <td>جسم واحد فعلياً يُعطى عدة هويات متتالية بدل هوية واحدة مستمرة</td>
  <td>القسم 9: 29 هوية <code>ambulance</code> لإسعاف واحد فعلي</td>
</tr>
<tr>
  <td><strong>مسار وهمي Ghost Track</strong></td>
  <td>يبقى مسار حياً رغم اختفاء الجسم الحقيقي، بسبب اكتشاف خاطئ متكرر</td>
  <td>خطر متزايد كلما رفعنا <code>track_buffer</code></td>
</tr>
</tbody>
</table>

<p>لاحظ أن ما رأيناه فعلياً في هذا الدرس هو <strong>التجزّؤ</strong> بالدرجة
الأولى، لا تبديل الهوية. السبب: مصدر ضعفنا هنا ليس تقاطع أجسام متشابهة، بل
كشف متذبذب لفئة <code>ambulance</code> نفسها (كما وثّقنا الأسبوع الماضي).
هذا درس مهم: <strong>نوع فشل التتبع الذي تراه يعتمد على نوع ضعف الكاشف الذي
تغذّيه به</strong>.</p>

<h2>13.2 نرى التجزّؤ بالأرقام</h2>

<p>نعود إلى <code>tracking_df</code> الذي بنيناه في القسم 8.3، ونفحص كل
هوية <code>ambulance</code> على حدة: متى ظهرت، ومتى اختفت، وكم إطاراً
عاشت؟</p>"""
)

code(
    '''ambulance_tracks = tracking_df[tracking_df["class"] == "ambulance"]

lifespans = ambulance_tracks.groupby("track_id")["frame"].agg(["min", "max", "count"])
lifespans.columns = ["أول إطار", "آخر إطار", "عدد الإطارات"]
lifespans = lifespans.sort_values("أول إطار")

print(f"عدد الهويات المختلفة لفئة ambulance: {len(lifespans)}")
print(f"متوسط عمر الهوية الواحدة: {lifespans['عدد الإطارات'].mean():.1f} إطار فقط")
print(f"أطول هوية عاشت: {lifespans['عدد الإطارات'].max()} إطاراً")
lifespans.head(10)'''
)

rtl(
    """<p>معظم الهويات تعيش عدداً قليلاً جداً من الإطارات قبل أن تُفقَد
وتُستبدَل بهوية جديدة. هذا هو التجزّؤ حرفياً: نفس الإسعاف الفعلي يُعاد
تعريفه عشرات المرات بدل أن يُعرَّف مرة واحدة ويستمر.</p>

<h2>13.3 جدول الضبط: المعاملات التي تتحكّم بهذا التوازن</h2>

<table>
<thead>
<tr><th>المعامل</th><th>الافتراضي</th><th>رفعه يعني</th><th>خفضه يعني</th></tr>
</thead>
<tbody>
<tr>
  <td><code>track_high_thresh</code></td><td>0.25</td>
  <td>مطابقة أكثر تحفّظاً في المرحلة الأولى</td>
  <td>قبول اكتشافات أضعف كمرحلة أولى، خطر تبديل هوية أعلى</td>
</tr>
<tr>
  <td><code>track_low_thresh</code></td><td>0.10</td>
  <td>مرحلة ثانية أكثر تشدّداً، تجزّؤ أكثر</td>
  <td>إنقاذ أكثر من الحجب، لكن خطر ربط ضجيج بمسار حقيقي</td>
</tr>
<tr>
  <td><code>match_thresh</code></td><td>0.80</td>
  <td>يتطلّب تداخلاً أعلى ليقبل الربط، تجزّؤ أكثر عند الحركة السريعة</td>
  <td>يقبل ربطاً أضعف، خطر تبديل هوية أعلى</td>
</tr>
<tr>
  <td><code>track_buffer</code></td><td>30</td>
  <td>يبقي المسار المفقود حياً فترة أطول، ينجو من حجب أطول</td>
  <td>يحذف المسار المفقود بسرعة، تجزّؤ أكثر عند أي انقطاع قصير</td>
</tr>
</tbody>
</table>

<div class="note">
<p><strong>لا يوجد إعداد "صحيح" مطلق.</strong> كل معامل هنا مقايضة: رفعه
يحلّ مشكلة ويخلق أخرى. الإعداد الأنسب يعتمد على مشهدك: طريق مزدحم بأجسام
متشابهة يحتاج <code>match_thresh</code> أعلى لتفادي تبديل الهوية، بينما
مشهد فيه حجب طويل متكرر يحتاج <code>track_buffer</code> أعلى - حتى لو
كلَّفَ ذلك بعض مسارات الأشباح.</p>
</div>"""
)


# ===========================================================================
# 14. كيف نقيس جودة التتبع؟
# ===========================================================================

rtl(
    """<hr />
<h1>14. كيف نقيس جودة التتبع؟</h1>

<p>الأسبوع الماضي قِسنا جودة الكشف بـ Precision و Recall و mAP. التتبع
يحتاج مقاييس مختلفة، لأنه يضيف بعداً لم يكن موجوداً من قبل: <strong>هل
الهوية نفسها استمرّت بشكل صحيح عبر الزمن؟</strong> هذا القسم مفاهيمي بحت -
فهمُ الرمز أهم من حسابه بأنفسنا اليوم.</p>

<table>
<thead>
<tr><th>المقياس</th><th>يقيس</th><th>حساسيته لتبديل الهوية</th></tr>
</thead>
<tbody>
<tr>
  <td><strong>MOTA</strong><br/>(Multi-Object Tracking Accuracy)</td>
  <td>يجمع الاكتشافات المفقودة (FN) والخاطئة (FP) وتبديلات الهوية في رقم
  واحد</td>
  <td>منخفضة نسبياً - تبديل هوية واحد يُحتسب بوزن صغير مقارنة بآلاف
  الاكتشافات</td>
</tr>
<tr>
  <td><strong>IDF1</strong></td>
  <td>مدى تطابق الهويات المتوقَّعة مع الهويات الحقيقية عبر الزمن كله، لا
  إطاراً بإطار</td>
  <td>عالية - مصمَّم خصيصاً ليعاقب فقدان الاستمرارية</td>
</tr>
<tr>
  <td><strong>HOTA</strong><br/>(Higher Order Tracking Accuracy)</td>
  <td>يفصل بوضوح بين دقة الكشف ودقة الربط، ثم يجمعهما بتوازن مدروس</td>
  <td>عالية، والأحدث والأكثر توازناً بين المقياسين السابقين</td>
</tr>
</tbody>
</table>

<div class="note">
<p><strong>لماذا لم نحسب أياً من هذه الأرقام على مقاطعنا؟</strong> لأن
حسابها يحتاج <strong>توسيماً حقيقياً لكل إطار</strong>: صندوق كل جسم مع
هويته الصحيحة يدوياً، إطاراً إطاراً، طوال المقطع - وهذا عمل توسيم ضخم يفوق
نطاق هذا الدرس. ما فعلناه بدلاً منه في القسم 13 أبسط لكنه صادق بنفس القدر:
عددنا الهويات المختلفة التي أنشأها المتتبع لجسم نعرف يقيناً أنه واحد فعلياً
- وهذا مؤشر تجزّؤ خام لا يحتاج توسيماً على الإطلاق.</p>
</div>"""
)


# ===========================================================================
# 15. تمرين صفي
# ===========================================================================

rtl(
    """<hr />
<h1>15. تمرين صفي</h1>

<h3>المهمة 1: أثر track_buffer</h3>
<p>عدّل قيمة <code>track_buffer</code> في إعداد ByteTrack: جرّبها 5 ثم
100 (بدل الافتراضي 30)، وأعد حساب عدد هويات <code>ambulance</code>
المختلفة كما في القسم 8.2. هل النتيجة كما توقّعت من جدول القسم 13.3؟</p>"""
)

code(
    '''# TODO: انسخ إعداد bytetrack الافتراضي وعدّل track_buffer فيه، ثم أعد القياس
custom_tracker_yaml = """
tracker_type: bytetrack
track_high_thresh: 0.25
track_low_thresh: 0.1
new_track_thresh: 0.25
track_buffer: 30
match_thresh: 0.8
fuse_score: True
"""
# 1. غيّر track_buffer أعلاه إلى 5، احفظ الملف، أعد تشغيل count_unique_ambulance_ids
# 2. كرّر بقيمة 100
# 3. سجّل النتيجتين وقارنهما بنتيجة القسم 8.2 (22 مع القيمة الافتراضية 30)

Path("custom_bytetrack.yaml").write_text(custom_tracker_yaml)
print("عدّل الملف أعلاه ثم شغّل:")
print('count_unique_ambulance_ids("custom_bytetrack.yaml")')'''
)

rtl(
    """<h3>المهمة 2: ByteTrack مقابل BoT-SORT بصرياً</h3>
<p>في القسم 8.2 كانت أعداد الهويات متساوية بين الاثنين. أعد توليد الفيديو
المتتبَّع في القسم 11 مرة بـ <code>tracker="botsort.yaml"</code> بدل
<code>bytetrack.yaml</code>. شاهد الفيديوين جنباً إلى جنب: هل تلاحظ أي فرق
بصري رغم تساوي العدد الإجمالي؟</p>

<h3>المهمة 3: أثر max_age في متتبعنا المصغّر</h3>
<p>في القسم 9، جرّب <code>SimpleIoUTracker(max_age=1)</code> ثم
<code>SimpleIoUTracker(max_age=20)</code> بدل الافتراضي 5. سجّل عدد هويات
<code>ambulance</code> في كل حالة.</p>"""
)

code(
    '''# TODO: جرّب القيمتين وسجّل النتيجة في كل مرة
for trial_max_age in [1, 20]:
    trial_model = YOLO(MODEL_PATH)
    trial_tracker = SimpleIoUTracker(max_age=trial_max_age, iou_threshold=0.3)
    trial_ever_created = {}

    for result in trial_model.predict(source=AMBULANCE_CLIP, conf=0.25, device=DEVICE, stream=True, verbose=False):
        boxes = result.boxes.xyxy.cpu().numpy() if result.boxes is not None else np.zeros((0, 4))
        classes = [trial_model.names[int(c)] for c in result.boxes.cls] if result.boxes is not None else []
        existing_ids = set(trial_tracker.tracks.keys())
        trial_tracker.update(boxes, classes)
        for new_id in set(trial_tracker.tracks.keys()) - existing_ids:
            trial_ever_created[new_id] = trial_tracker.tracks[new_id]["class"]

    n_ids = sum(1 for c in trial_ever_created.values() if c == "ambulance")
    print(f"max_age={trial_max_age:3d}  ->  عدد هويات ambulance: {n_ids}")

# فسّر: لماذا يقلّل max_age الكبير عدد الهويات؟ وما ثمنه المحتمل (مسارات وهمية)؟'''
)

rtl(
    """<h3>المهمة 4: أوجد لحظة الانهيار بنفسك</h3>
<p>شغّل <code>SimpleIoUTracker</code> على مقطع الإسعاف إطاراً إطاراً، واطبع
رقم الإطار وهوية <code>ambulance</code> الحالية في كل مرة. حدّد
<strong>الإطار بالضبط</strong> الذي تتغيّر فيه الهوية لأول مرة، وافحص تلك
اللحظة بصرياً (هل توقّف الكشف؟ هل تغيّرت زاوية الإسعاف؟). اكتب سطرين
تشرحان السبب الأرجح.</p>"""
)


# ===========================================================================
# 16. أسئلة مراجعة سريعة
# ===========================================================================

rtl(
    """<hr />
<h1>16. أسئلة مراجعة سريعة</h1>

<h3>سؤال 1</h3>
<p>لماذا يفشل العدّ الساذج الذي يجمع عدد الاكتشافات في كل إطار على حدة؟</p>

<h3>سؤال 2</h3>
<p>عرّف الفرق بين Detection و Track و ID بكلماتك الخاصة.</p>

<h3>سؤال 3</h3>
<p>لماذا تُفضَّل خوارزمية Hungarian على المطابقة الجشعة في الربط بين
الإطارات؟ اذكر مثالاً يوضّح الفرق.</p>

<h3>سؤال 4</h3>
<p>كيف ينقذنا مرشّح كالمان أثناء الحجب الكامل؟ وما حدود هذا الإنقاذ - متى
يفشل هو الآخر؟</p>

<h3>سؤال 5</h3>
<p>ما الفرق الجوهري بين SORT و DeepSORT و ByteTrack من حيث مصدر معلومة
الربط التي يعتمد عليها كل منها؟</p>

<h3>سؤال 6</h3>
<p>ما الفرق بين تبديل الهوية (ID Switch) والتجزّؤ (Fragmentation)؟ أيّهما
شاهدناه فعلياً في تجربتنا، ولماذا برأيك؟</p>

<h3>سؤال 7</h3>
<p>لماذا لا يمكننا حساب MOTA أو IDF1 أو HOTA على مقاطعنا الخاصة في هذا
الدرس؟ ماذا كان سيتطلّب ذلك؟</p>"""
)


# ===========================================================================
# 17. بنك أسئلة Kahoot
# ===========================================================================

rtl(
    """<hr />
<h1>17. بنك أسئلة Kahoot</h1>

<div class="note">
<p>هذه الأسئلة جاهزة للنسخ إلى Kahoot. الحدود المسموحة في المنصة: نص
السؤال حتى 120 حرفاً، وكل خيار حتى 75 حرفاً، وأربعة خيارات، وإجابة صحيحة
واحدة.</p>
</div>

<h3>سؤال 1</h3>
<p><strong>السؤال:</strong> ما الذي يفتقر إليه الكشف وحده مقارنة بالتتبع؟</p>
<ul>
<li>أ) الدقة</li>
<li>ب) الذاكرة بين الإطارات</li>
<li>ج) السرعة</li>
<li>د) الألوان</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 2</h3>
<p><strong>السؤال:</strong> ما الذي يضيفه التتبع فوق الكشف؟</p>
<ul>
<li>أ) فئة جديدة كلياً</li>
<li>ب) هوية ثابتة تلازم الجسم عبر الزمن</li>
<li>ج) دقة صناديق أعلى</li>
<li>د) نموذجاً أكبر حجماً</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 3</h3>
<p><strong>السؤال:</strong> ما الذي تقيسه IoU بين صندوقين؟</p>
<ul>
<li>أ) الفرق في الألوان بينهما</li>
<li>ب) نسبة التقاطع إلى الاتحاد</li>
<li>ج) سرعة حركة الجسم</li>
<li>د) عدد البكسلات داخل الصندوق</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 4</h3>
<p><strong>السؤال:</strong> لماذا قد تفشل المطابقة الجشعة رغم أن كل خطوة
تبدو منطقية؟</p>
<ul>
<li>أ) لأنها بطيئة جداً في التنفيذ</li>
<li>ب) لأنها لا ترى مصفوفة التكلفة كاملة دفعة واحدة</li>
<li>ج) لأنها تحتاج كرت شاشة قوياً</li>
<li>د) لأنها لا تدعم أكثر من صندوقين</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 5</h3>
<p><strong>السؤال:</strong> ماذا يفعل مرشّح كالمان أثناء حجب كامل للجسم؟</p>
<ul>
<li>أ) يتوقف عن العمل فوراً</li>
<li>ب) يواصل التنبؤ بلا تصحيح من كشف حقيقي</li>
<li>ج) يحذف المسار في الحال</li>
<li>د) يطلب كشفاً جديداً من المستخدم</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 6</h3>
<p><strong>السؤال:</strong> ما الذي يضيفه DeepSORT فوق SORT؟</p>
<ul>
<li>أ) سرعة معالجة أعلى</li>
<li>ب) معلومة المظهر عبر شبكة Re-ID</li>
<li>ج) دقة صناديق أعلى تلقائياً</li>
<li>د) عتبة ثقة أقل للكاشف</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 7</h3>
<p><strong>السؤال:</strong> ما الفكرة الجوهرية في ByteTrack؟</p>
<ul>
<li>أ) تجاهل كل الاكتشافات ضعيفة الثقة</li>
<li>ب) استخدام الاكتشافات الضعيفة بدل رميها فوراً</li>
<li>ج) إضافة كاميرا ثانية للمشهد</li>
<li>د) تدريب نموذج كشف أكبر حجماً</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 8</h3>
<p><strong>السؤال:</strong> أي معامل يضبط مدة بقاء المسار المفقود حياً؟</p>
<ul>
<li>أ) conf</li>
<li>ب) track_buffer</li>
<li>ج) imgsz</li>
<li>د) batch</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 9</h3>
<p><strong>السؤال:</strong> كم هوية ambulance أنشأها متتبعنا المصغّر لإسعاف
واحد فعلياً في تجربتنا؟</p>
<ul>
<li>أ) 1</li>
<li>ب) 5</li>
<li>ج) 29</li>
<li>د) 100</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ج</p>

<h3>سؤال 10</h3>
<p><strong>السؤال:</strong> لماذا تساوى عدد الهويات بين bytetrack و botsort
في مقطعنا؟</p>
<ul>
<li>أ) الكاميرا ثابتة و Re-ID معطَّل في كليهما افتراضياً</li>
<li>ب) الملفّان متطابقان حرفياً بلا أي فرق</li>
<li>ج) خطأ برمجي في خلية المقارنة</li>
<li>د) النموذج لا يفرّق بين المتتبعين إطلاقاً</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> أ</p>

<h3>سؤال 11</h3>
<p><strong>السؤال:</strong> لماذا أعدنا تحميل نموذج جديد قبل قسم 9 بدل
استخدام model نفسه؟</p>
<ul>
<li>أ) للتسريع فقط، بلا أثر على النتائج</li>
<li>ب) لأن track السابق غيّر حالة النموذج بصمت فتختلف النتائج</li>
<li>ج) عادة برمجية شائعة بلا سبب حقيقي</li>
<li>د) لتوفير مساحة تخزين على القرص</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>

<h3>سؤال 12</h3>
<p><strong>السؤال:</strong> ما الخطر الأكبر من رفع track_buffer كثيراً؟</p>
<ul>
<li>أ) بطء شديد لا يُحتمل في المعالجة</li>
<li>ب) مسارات وهمية تبقى حيّة طويلاً بلا داعٍ</li>
<li>ج) فقدان ملف الفيديو الأصلي</li>
<li>د) تعطّل النموذج عن العمل تماماً</li>
</ul>
<p><strong>الإجابة الصحيحة:</strong> ب</p>"""
)


# ===========================================================================
# 18. الخلاصة
# ===========================================================================

rtl(
    """<hr />
<h1>18. الخلاصة</h1>

<p>ما فعلناه في هذا الدرس:</p>

<ul>
<li>أثبتنا أن العدّ الساذج بجمع اكتشافات كل إطار على حدة يعطي أرقاماً
سخيفة (956 "سيارة" في 15 ثانية)، لأن الكشف عديم الذاكرة بين الإطارات.</li>
<li>بنينا الأدوات الثلاث الأساسية للربط بين الإطارات: IoU، مصفوفة التكلفة،
وخوارزمية Hungarian - ورأينا بالأرقام لماذا تتفوّق على المطابقة الجشعة.</li>
<li>فهمنا بالحدس كيف ينقذنا مرشّح كالمان أثناء الحجب، بالتنبؤ بالحركة بدل
انتظار كشف قد لا يصل أبداً.</li>
<li>قارنّا SORT و DeepSORT و ByteTrack: كل واحد يحلّ نقطة ضعف في سابقه،
بثمن مختلف في كل مرة.</li>
<li>بنينا متتبعاً مصغّراً بأيدينا فأنتج 29 هوية لإسعاف واحد فعلياً - ورأينا
التجزّؤ رقماً حقيقياً لا افتراضاً نظرياً.</li>
<li>استخدمنا <code>model.track()</code> من Ultralytics عملياً، ورسمنا
مسارات وهويات ثابتة، وحفظنا فيديو متتبَّعاً كاملاً على القرص.</li>
<li>اكتشفنا فخّاً حقيقياً في Ultralytics: <code>track(persist=True)</code>
يغيّر حالة النموذج بصمت، فيؤثر على استدعاءات <code>predict()</code>
اللاحقة - ووثّقناه ليتجنّبه غيرنا.</li>
</ul>

<h2>في الأسبوع القادم</h2>

<p>أصبح لدينا الآن ما كان ناقصاً في نهاية الأسبوع السابع: <strong>هوية
ثابتة لكل جسم عبر الزمن</strong>. الأسبوع التاسع يبني على هذا مباشرة:
عدّ حقيقي للمركبات بخط عبور، وتقدير كثافة المرور، ثم منطق القرار الكامل
لنظام "الإسعاف له الأولوية" - من رؤية الإسعاف إلى فتح الإشارة له فعلياً.</p>

<hr />
<h2>مصادر للاستزادة</h2>

<ul>
<li><a href="https://docs.ultralytics.com/modes/track/">Ultralytics — Track mode</a></li>
<li><a href="https://docs.ultralytics.com/reference/trackers/">Ultralytics — Trackers reference</a></li>
<li><a href="https://arxiv.org/abs/1602.00763">SORT: Simple Online and Realtime Tracking (الورقة الأصلية)</a></li>
<li><a href="https://arxiv.org/abs/1703.07402">DeepSORT (الورقة الأصلية)</a></li>
<li><a href="https://arxiv.org/abs/2110.06864">ByteTrack (الورقة الأصلية)</a></li>
<li><a href="https://arxiv.org/abs/2206.14651">BoT-SORT (الورقة الأصلية)</a></li>
<li><a href="https://motchallenge.net/">MOTChallenge — المرجع القياسي لتقييم التتبع</a></li>
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

    start_idx = next(i for i, c in enumerate(cells) if START_MARKER in source_of(c))
    del cells[start_idx:]

    cells.extend(new_cells)
    NOTEBOOK.write_text(json.dumps(notebook, ensure_ascii=False, indent=1))

    n_md = sum(1 for c in cells if c["cell_type"] == "markdown")
    n_code = sum(1 for c in cells if c["cell_type"] == "code")
    print(f"{NOTEBOOK}: {len(cells)} خلية ({n_md} markdown، {n_code} code)")
    print(f"استُبدلت الأقسام 13-18 بـ {len(new_cells)} خلية.")


if __name__ == "__main__":
    main()
