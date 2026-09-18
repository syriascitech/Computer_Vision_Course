#!/usr/bin/env python3
"""
يملأ الأقسام 1-4 من دفتر الأسبوع 8 (لماذا التتبع، تعريف MOT، الربط بين
الإطارات، مرشّح كالمان)، بين عنوان القسم الأول وعنوان القسم الخامس.

قابل لإعادة التشغيل: يبحث عن عنوان القسم 1 وعنوان القسم 5 كعلامتين،
ويستبدل كل ما بينهما بالمحتوى الجديد، فلا يمسّ خلايا التهيئة قبله ولا
عناوين الأقسام 5-18 بعده (والتي لا تزال فارغة بانتظار سكربتات لاحقة).

الاستخدام:
    python tools/append_week8_sections_1_4.py
"""

from __future__ import annotations

import json
from pathlib import Path

NOTEBOOK = Path("Week8/week_8_object_tracking.ipynb")
START_MARKER = "<h1>1. لماذا الكشف وحده لا يكفي؟</h1>"
END_MARKER = "<h1>5. SORT</h1>"

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
# 1. لماذا الكشف وحده لا يكفي؟
# ===========================================================================

rtl(
    """<hr />
<h1>1. لماذا الكشف وحده لا يكفي؟</h1>

<h2>1.1 تجربة حية: ثلاثة إطارات متتالية</h2>

<p>لنبدأ بتجربة بسيطة. المجلد <code>frames/</code> يحوي ثلاثة إطارات
متتالية مستخرجة من <code>videos/traffic_clip.mp4</code>، بفارق جزء من
الثانية بين كل إطار والذي يليه. سنشغّل نموذجنا على كل إطار على حدة، تماماً
كما فعلنا الأسبوع الماضي.</p>"""
)

code(
    '''from pathlib import Path

frame_paths = sorted(Path("frames").glob("*.jpg"))
print("عدد الإطارات:", len(frame_paths))

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

for ax, frame_path in zip(axes, frame_paths):
    result = model.predict(source=str(frame_path), conf=0.25, device=DEVICE, verbose=False)[0]
    detected_cars = sum(1 for c in result.boxes.cls if model.names[int(c)] == "car")

    ax.imshow(cv2.cvtColor(result.plot(), cv2.COLOR_BGR2RGB))
    ax.set_title(f"{frame_path.name}\\ncars detected: {detected_cars}", fontsize=12)
    ax.axis("off")

plt.suptitle("Same detector, three consecutive frames", fontsize=15)
plt.tight_layout()
plt.show()'''
)

rtl(
    """<p>النتيجة: كل إطار من الثلاثة فيه <strong>سيارتان مكتشفتان</strong>.
لكن انظر جيداً إلى الصور: هاتان السيارتان متوقفتان عند إشارة حمراء، ولم
تتحركا عملياً بين الإطارات الثلاثة. النموذج لا "يعرف" هذه الحقيقة - فهو
يعالج كل إطار من الصفر، وكأنه يرى الصورة للمرة الأولى في كل مرة.</p>

<h2>1.2 مشكلة العدّ المضاعف</h2>

<p>لنأخذ هذه الملاحظة إلى أقصاها. لو أردنا الإجابة عن سؤال بسيط: "كم سيارة
ظهرت في هذا المقطع؟"، وكانت طريقتنا الساذجة هي: <strong>اجمع عدد السيارات
المكتشفة في كل إطار على حدة</strong>. لنجرّب هذا فعلياً على المقطع كاملاً:</p>"""
)

code(
    '''naive_car_count = 0
n_frames_processed = 0

for result in model.predict(
    source="videos/traffic_clip.mp4", conf=0.25, device=DEVICE, stream=True, verbose=False
):
    n_frames_processed += 1
    naive_car_count += sum(1 for c in result.boxes.cls if model.names[int(c)] == "car")

print(f"عدد الإطارات في المقطع: {n_frames_processed}")
print(f"مجموع اكتشافات (car) عبر كل الإطارات: {naive_car_count}")
print(f"لو صدّقنا هذا الرقم حرفياً، لقلنا إن {naive_car_count} سيارة مختلفة عبرت في {n_frames_processed / 30:.0f} ثانية فقط.")'''
)

rtl(
    """<div class="note">
<p><strong>هذا رقم سخيف، وهذا بالضبط بيت القصيد.</strong> المقطع خمس عشرة
ثانية فقط، وفيه على الأرجح أقل من عشر سيارات مختلفة إجمالاً. المجموع
الكبير الذي حصلنا عليه لا يقيس عدد السيارات، بل يقيس <strong>عدد
الإطارات التي ظهرت فيها سيارة</strong> - وهذان سؤالان مختلفان تماماً.</p>
<p>السيارتان اللتان رأيناهما متوقفتين في 1.1 يُعاد عدّهما في كل واحد من
الإطارات الأربعمئة وتسعة وأربعين، لأن الكشف عديم الذاكرة: لا يعرف أن
السيارة في الإطار رقم 200 هي نفسها التي في الإطار رقم 201.</p>
</div>

<h2>1.3 الكشف مقابل التتبع</h2>

<table>
<thead>
<tr><th></th><th>Detection (كشف)</th><th>Tracking (تتبع)</th></tr>
</thead>
<tbody>
<tr><td>يُجيب عن</td><td>ما هذا؟ وأين هو؟ (في إطار واحد)</td>
    <td>هل هذا هو نفسه الذي رأيته سابقاً؟</td></tr>
<tr><td>الذاكرة</td><td>لا ذاكرة بين الإطارات</td>
    <td>يحمل هوية (ID) ثابتة عبر الزمن</td></tr>
<tr><td>يمكّن من</td><td>"يوجد إسعاف في هذا الإطار"</td>
    <td>"هذا الإسعاف نفسه اقترب 30 متراً خلال ثانيتين"</td></tr>
<tr><td>يحتاج</td><td>نموذجاً مدرَّباً فقط</td>
    <td>كاشفاً + خوارزمية ربط بين الإطارات</td></tr>
</tbody>
</table>

<p>التتبّع لا يستبدل الكشف، بل <strong>يبني فوقه</strong>: في كل إطار
نكشف الأجسام كما تعلّمنا، ثم نضيف طبقة جديدة تربط اكتشافات هذا الإطار
باكتشافات الإطار السابق.</p>

<h2>فكر قبل المتابعة</h2>

<ol>
<li>لو حرّكنا الكاميرا بدل السيارة، هل تبقى مشكلة العدّ المضاعف قائمة؟</li>
<li>ما أبسط معلومة يمكن استخدامها للربط بين صندوق في الإطار الحالي وصندوق
في الإطار السابق؟</li>
<li>هل يحتاج التتبع نموذج كشف مختلفاً عن الذي درّبناه الأسبوع الماضي؟</li>
</ol>"""
)


# ===========================================================================
# 2. تعريف المشكلة: التتبع متعدد الأجسام
# ===========================================================================

rtl(
    """<hr />
<h1>2. تعريف المشكلة: التتبع متعدد الأجسام Multi-Object Tracking</h1>

<h2>2.1 ثلاثة مصطلحات أساسية</h2>

<ul>
<li><strong>Detection (كشف)</strong>: صندوق واحد + فئة + ثقة، ناتج عن
النموذج في إطار واحد فقط. لا يحمل أي معلومة عن الزمن.</li>
<li><strong>Track (مسار)</strong>: سلسلة من الاكتشافات عبر إطارات متتالية،
تنتمي جميعها - حسب اعتقاد المتتبع - لنفس الجسم الفعلي.</li>
<li><strong>ID (هوية)</strong>: رقم صحيح ثابت يُلصَق بمسار واحد طوال حياته.
هو الشيء الوحيد الجديد الذي يضيفه التتبع فوق الكشف.</li>
</ul>

<h2>2.2 فلسفة Tracking-by-Detection</h2>

<p>كل المتتبعات التي سندرسها اليوم (SORT و DeepSORT و ByteTrack) تتبع
الفلسفة نفسها، وهي الأشيع عملياً في الصناعة:</p>

<blockquote>
<p>شغّل كاشفاً جيداً في كل إطار على حدة، ثم اربط اكتشافات الإطار الحالي
بمسارات موجودة من الإطارات السابقة.</p>
</blockquote>

<p>بعبارة أخرى: <strong>لا يوجد نموذج واحد "يتتبّع"</strong>. يوجد كاشف
(النموذج الذي درّبناه) وخوارزمية ربط منفصلة تعمل فوقه. هذا الفصل بين
المهمتين هو ما يجعل هذه الطريقة عملية: يمكن تحسين الكاشف والمتتبع كلٌّ على
حدة.</p>

<h2>2.3 أربعة تحديات تواجه أي متتبع</h2>

<table>
<thead>
<tr><th>التحدي</th><th>ماذا يحدث</th><th>مثال من مقاطعنا</th></tr>
</thead>
<tbody>
<tr>
  <td><strong>الحجب Occlusion</strong></td>
  <td>يختفي الجسم مؤقتاً خلف جسم آخر، فلا يكشفه النموذج لعدة إطارات</td>
  <td>سيارة تختفي خلف حافلة عند التقاطع</td>
</tr>
<tr>
  <td><strong>التشابه Similarity</strong></td>
  <td>جسمان متشابهان جداً بصرياً يتبادلان الأماكن قرب بعضهما</td>
  <td>سيارتان بيضاوان متجاورتان في زحمة السير</td>
</tr>
<tr>
  <td><strong>الدخول والخروج Entry/Exit</strong></td>
  <td>يجب أن يعرف المتتبع متى يولد مسار جديد ومتى يُغلق مسار قديم</td>
  <td>سيارة تدخل من حافة الإطار، وإسعاف يغادر المشهد</td>
</tr>
<tr>
  <td><strong>الحركة السريعة Fast Motion</strong></td>
  <td>يتحرك الجسم مسافة كبيرة بين إطارين فتقل نسبة التداخل بينهما</td>
  <td>إسعاف يتجاوز بسرعة أثناء انخفاض معدل الإطارات</td>
</tr>
</tbody>
</table>

<p>ستلاحظ أن كل تحدٍّ من هذه الأربعة سيظهر لنا عملياً لاحقاً في هذا الدرس -
ليست تحديات نظرية فقط.</p>"""
)


# ===========================================================================
# 3. الربط بين الإطارات (Data Association)
# ===========================================================================

rtl(
    """<hr />
<h1>3. الربط بين الإطارات Data Association</h1>

<h2>3.1 IoU كمقياس تشابه</h2>

<p>أبسط فكرة للربط بين صندوق في الإطار الحالي وصندوق في الإطار السابق:
افترض أن الجسم لا يتحرك كثيراً بين إطارين متتاليين (فارق جزء من الثانية
فقط)، فصندوقاه في الإطارين سيتداخلان بشدة. نقيس هذا التداخل بـ
<strong>IoU</strong> نفسها التي استخدمناها الأسبوع الماضي لتقييم الكشف -
لكن هنا نستخدمها للربط بدل التقييم.</p>"""
)

code(
    '''def iou(box_a, box_b):
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


track_box = (100, 100, 300, 250)       # صندوق مسار من الإطار السابق
detection_box = (112, 108, 308, 255)   # صندوق كشف في الإطار الحالي

print("IoU بين المسار والكشف:", round(iou(track_box, detection_box), 3))'''
)

rtl(
    """<h2>3.2 مصفوفة التكلفة</h2>

<p>في إطار حقيقي لا يوجد مسار واحد وكشف واحد، بل عدة مسارات وعدة اكتشافات
في آنٍ واحد. نبني <strong>مصفوفة تكلفة</strong>: صف لكل مسار، وعمود لكل
كشف، وكل خانة هي <code>1 - IoU</code> (تكلفة منخفضة = تشابه عالٍ). المطلوب
بعدها: أي مسار يُربَط بأي كشف بحيث يكون <strong>مجموع التكلفة الكلي أصغر
ما يمكن</strong>؟</p>"""
)

figure(1, "iou_cost_matrix.jpg", "Building a cost matrix from IoU between tracks and detections")

rtl(
    """<h2>3.3 خوارزمية Hungarian، محلولة يدوياً</h2>

<p>هذه مسألة تخصيص كلاسيكية، ولها حل مضبوط في زمن معقول:
<strong>خوارزمية Hungarian</strong>. لن نشتق الخوارزمية، لكن سنراها تحل
مثالاً حقيقياً بثلاثة مسارات وثلاثة اكتشافات.</p>"""
)

code(
    '''import numpy as np
from scipy.optimize import linear_sum_assignment

# صفوف = مسارات T1..T3 من الإطار السابق، أعمدة = اكتشافات D1..D3 في الإطار الحالي
iou_matrix = np.array([
    [0.82, 0.10, 0.00],   # T1
    [0.15, 0.75, 0.05],   # T2
    [0.00, 0.20, 0.68],   # T3
])

cost_matrix = 1.0 - iou_matrix

track_indices, detection_indices = linear_sum_assignment(cost_matrix)

print("مصفوفة IoU:")
print(iou_matrix)
print()
for t, d in zip(track_indices, detection_indices):
    print(f"T{t + 1} <-> D{d + 1}   (IoU = {iou_matrix[t, d]:.2f})")

total_iou = iou_matrix[track_indices, detection_indices].sum()
print(f"\\nمجموع IoU للحل الأمثل: {total_iou:.2f}")'''
)

figure(2, "hungarian_assignment.jpg", "The Hungarian algorithm solving a 3x3 track-to-detection assignment")

rtl(
    """<h2>3.4 لماذا تفشل المطابقة الجشعة؟</h2>

<p>وسيلة أبسط تخطر بالبال: بدل حل المسألة كاملة، لماذا لا نأخذ في كل مرة
أعلى قيمة IoU في المصفوفة كلها، ونثبّت ذلك الربط، ثم نكرّر على ما تبقّى؟
هذه <strong>المطابقة الجشعة Greedy Matching</strong>. المثال التالي يبيّن
لماذا قد تعطي نتيجة أسوأ من الحل الأمثل:</p>"""
)

code(
    '''# مثال مضاد: مسار T1 قريب جداً من كشفين معاً، ومسار T2 قريب من كشف واحد فقط
iou_matrix_2 = np.array([
    [0.90, 0.85],   # T1: قريب جداً من كلا الكشفين
    [0.85, 0.00],   # T2: قريب من D1 فقط
])

# الحل الجشع: خذ أعلى قيمة في كل المصفوفة أولاً
greedy_pairs = []
remaining = iou_matrix_2.copy()
for _ in range(remaining.shape[0]):
    t, d = np.unravel_index(np.argmax(remaining), remaining.shape)
    greedy_pairs.append((t, d, remaining[t, d]))
    remaining[t, :] = -1
    remaining[:, d] = -1

greedy_total = sum(score for _, _, score in greedy_pairs)
print("الحل الجشع:")
for t, d, score in greedy_pairs:
    print(f"  T{t + 1} <-> D{d + 1}   (IoU = {score:.2f})")
print(f"  مجموع IoU (الجشع)  : {greedy_total:.2f}")

# الحل الأمثل عبر Hungarian
t_idx, d_idx = linear_sum_assignment(1.0 - iou_matrix_2)
optimal_total = iou_matrix_2[t_idx, d_idx].sum()
print("\\nالحل الأمثل (Hungarian):")
for t, d in zip(t_idx, d_idx):
    print(f"  T{t + 1} <-> D{d + 1}   (IoU = {iou_matrix_2[t, d]:.2f})")
print(f"  مجموع IoU (الأمثل) : {optimal_total:.2f}")'''
)

rtl(
    """<div class="note">
<p>المطابقة الجشعة تأخذ <code>T1-D1</code> فوراً لأنها أعلى قيمة في
المصفوفة كلها (0.90)، فتضطر بعدها إلى ربط <code>T2</code> بـ
<code>D2</code> رغم أن IoU بينهما صفر - أي لا علاقة بينهما إطلاقاً.
Hungarian ترى الصورة كاملة وتختار <code>T1-D2</code> و <code>T2-D1</code>
معاً، فيكون المجموع الكلي أعلى رغم أن كل قيمة على حدة أقل من 0.90.</p>
<p><strong>القاعدة:</strong> القرار الأفضل محلياً في كل خطوة على حدة ليس
بالضرورة الأفضل إجمالاً. هذا بالضبط سبب استخدام SORT وأغلب المتتبعات
الحديثة لخوارزمية Hungarian لا للمطابقة الجشعة.</p>
</div>"""
)


# ===========================================================================
# 4. التنبؤ بالحركة: مرشّح كالمان
# ===========================================================================

rtl(
    """<hr />
<h1>4. التنبؤ بالحركة: مرشّح كالمان Kalman Filter</h1>

<h2>4.1 الفكرة بحدس بسيط</h2>

<p>IoU وحدها تفترض أن الجسم لا يتحرك كثيراً بين إطارين. هذا صحيح غالباً،
لكنه يفشل تماماً في حالتين: حين يتحرك الجسم بسرعة، وحين <strong>يختفي
لعدة إطارات</strong> بسبب الحجب. في الحالة الثانية لا يوجد صندوق كشف
أصلاً لنقارنه بأي شيء.</p>

<p>الحل: بدل الاكتفاء بآخر موضع معروف، نبني نموذجاً بسيطاً لحركة الجسم
يجيب عن السؤال: <strong>"لو استمرّ هذا الجسم بنفس سرعته، أين سيكون في
الإطار القادم؟"</strong> هذا هو <strong>مرشّح كالمان</strong>. سنأخذه
بمستوى الحدس فقط، دون اشتقاق رياضي كامل.</p>

<h2>4.2 متجه الحالة</h2>

<p>يمثّل مرشّح كالمان في SORT كل مسار بسبعة أرقام:</p>

<p style="text-align:center; direction:ltr;">
<code>[x, y, s, r, vx, vy, vs]</code>
</p>

<ul>
<li><code>x, y</code>: مركز الصندوق.</li>
<li><code>s</code>: مساحة الصندوق (Scale)، و <code>r</code>: نسبة العرض
إلى الارتفاع (تُفترض شبه ثابتة لكل جسم).</li>
<li><code>vx, vy, vs</code>: سرعة تغيّر كل من <code>x</code> و
<code>y</code> و <code>s</code> بين إطار وآخر.</li>
</ul>

<p>أول أربعة أرقام تصف <strong>أين الجسم الآن</strong>، والثلاثة الأخيرة
تصف <strong>كيف يتحرك</strong> - وهذا الجزء الثاني هو ما يمكّننا من
التنبؤ.</p>

<h2>4.3 دورة التنبؤ ثم التحديث</h2>

<p>في كل إطار جديد، يمرّ كل مسار بخطوتين:</p>

<ol>
<li><strong>Predict (تنبأ)</strong>: بافتراض استمرار السرعة الحالية،
احسب أين يُفترض أن يكون الصندوق في هذا الإطار.
<span style="direction:ltr; display:inline-block;">
<code>x_predicted = x + vx</code></span></li>
<li><strong>Update (حدّث)</strong>: إذا وُجد كشف قريب من الموضع المتنبَّأ
به (بحساب IoU كما تعلّمنا)، اربطهما، واستخدم الكشف الحقيقي لتصحيح تقدير
المرشّح وتحديث السرعة.</li>
</ol>"""
)

figure(3, "kalman_predict_update.jpg", "The predict-update cycle of a Kalman filter across frames")

rtl(
    """<h2>4.4 لماذا ينقذنا أثناء الحجب</h2>

<p>هنا تكمن القوة الحقيقية للفكرة: إن اختفى الجسم فجأة خلف حاجز (حافلة
مثلاً) فلن يصلنا أي كشف له لعدة إطارات. لكن مرشّح كالمان لا يتوقف - يستمر
في خطوة <strong>Predict</strong> فقط (بلا Update، لعدم وجود كشف يصحّحه)،
فيواصل تحريك الصندوق المتوقَّع بنفس السرعة الأخيرة المعروفة.</p>

<p>حين يخرج الجسم من الحجب ويظهر كشف جديد، يكون الصندوق المتوقَّع من
المرشّح قريباً بما يكفي من الكشف الحقيقي لتتطابق معه IoU، فيُربَطان معاً
بنفس الهوية القديمة - <strong>رغم انقطاع الكشف تماماً في الوسط.</strong>
بدون هذا التنبؤ، كان المتتبع سيعتبر ظهور الجسم مجدداً "جسماً جديداً
كلياً" ويعطيه هوية مختلفة.</p>"""
)

figure(4, "kalman_occlusion.jpg", "How Kalman prediction bridges a full occlusion without losing the track ID")


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
    print(f"استُبدلت الأقسام 1-4 بـ {len(new_cells)} خلية.")


if __name__ == "__main__":
    main()
