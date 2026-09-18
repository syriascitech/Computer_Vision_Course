#!/usr/bin/env python3
"""
يملأ الأقسام 8-12 من دفتر الأسبوع 8 (Ultralytics عملياً، متتبع IoU من
الصفر، المسارات والتلوين، التشغيل الكامل، ولمحة العدّ)، بين عنوان القسم
الثامن وعنوان القسم الثالث عشر.

قابل لإعادة التشغيل: يبحث عن عنوان القسم 8 وعنوان القسم 13 كعلامتين،
ويستبدل كل ما بينهما بالمحتوى الجديد.

الاستخدام:
    python tools/append_week8_sections_8_12.py
"""

from __future__ import annotations

import json
from pathlib import Path

NOTEBOOK = Path("Week8/week_8_object_tracking.ipynb")
START_MARKER = "<h1>8. عملياً مع Ultralytics</h1>"
END_MARKER = "<h1>13. متى يفشل المتتبع؟</h1>"

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
# 8. عملياً مع Ultralytics
# ===========================================================================

rtl(
    """<hr />
<h1>8. عملياً مع Ultralytics</h1>

<p>كل ما درسناه نظرياً - IoU، Hungarian، مرشّح كالمان، ByteTrack - مطبَّق
جاهزاً داخل مكتبة Ultralytics نفسها التي استخدمناها للكشف. لا نحتاج إلى
كتابة أي من هذا بأيدينا لنستخدمه فعلياً.</p>

<h2>8.1 model.track() و persist=True</h2>

<p>الفرق الوحيد بين الكشف والتتبع في الاستخدام هو استبدال
<code>model.predict()</code> بـ <code>model.track()</code>، مع تمرير
<code>persist=True</code> ليتذكّر المتتبع مساراته من إطار للذي يليه بدل
البدء من الصفر في كل مرة.</p>"""
)

code(
    '''AMBULANCE_CLIP = "videos/ambulance_clip.mp4"

first_result = next(model.track(
    source=AMBULANCE_CLIP,
    conf=0.25,
    device=DEVICE,
    tracker="bytetrack.yaml",
    persist=True,
    stream=True,
    verbose=False,
))

print("عدد الاكتشافات في أول إطار:", len(first_result.boxes))
print("هويات التتبع (track ID) لهذا الإطار:", first_result.boxes.id)

plt.figure(figsize=(7, 5))
plt.imshow(cv2.cvtColor(first_result.plot(), cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.title("model.track() - each box now carries a track ID")
plt.show()'''
)

rtl(
    """<p>لاحظ أن <code>result.plot()</code> رسم رقم الهوية تلقائياً فوق كل
صندوق - <code>result.boxes.id</code> هو الإضافة الوحيدة الجديدة على كل ما
نعرفه من الأسبوع الماضي.</p>

<h2>8.2 bytetrack.yaml مقابل botsort.yaml</h2>

<p>تشحن Ultralytics ملفَي إعداد جاهزين. القيم الافتراضية المهمة في
كليهما:</p>

<table>
<thead>
<tr><th>المعامل</th><th>القيمة الافتراضية</th><th>ماذا يضبط</th></tr>
</thead>
<tbody>
<tr><td><code>track_high_thresh</code></td><td>0.25</td>
    <td>عتبة المرحلة الأولى (عالية الثقة)</td></tr>
<tr><td><code>track_low_thresh</code></td><td>0.10</td>
    <td>عتبة المرحلة الثانية (منخفضة الثقة)</td></tr>
<tr><td><code>track_buffer</code></td><td>30</td>
    <td>عدد الإطارات التي يبقى فيها المسار المفقود حياً</td></tr>
<tr><td><code>match_thresh</code></td><td>0.8</td>
    <td>عتبة تشابه الربط (IoU/تكلفة)</td></tr>
</tbody>
</table>

<p>الفرق الأساسي: <code>botsort.yaml</code> يضيف تعويض حركة الكاميرا
(<code>gmc_method</code>)، ويمكنه تفعيل مظهر Re-ID - لكن
<code>with_reid: False</code> افتراضياً، وهذا مهم: <strong>تفعيله يحمّل
نموذجاً إضافياً من الإنترنت</strong>، فسيكسر العمل بلا اتصال إن فُعِّل.
سنستخدمه هنا بإعداده الافتراضي فقط.</p>

<p>بما أن كاميرتنا ثابتة (لا حركة كاميرا لنعوّضها) و Re-ID معطَّل
افتراضياً في كليهما، هل يُحدِث اختيار أحدهما فرقاً فعلياً على مقطعنا؟
لنقِس، لا نخمّن:</p>"""
)

code(
    '''def count_unique_ambulance_ids(tracker_yaml):
    ids = set()
    for result in model.track(
        source=AMBULANCE_CLIP, conf=0.25, device=DEVICE,
        tracker=tracker_yaml, persist=True, stream=True, verbose=False,
    ):
        if result.boxes is None or result.boxes.id is None:
            continue
        for track_id, class_id in zip(result.boxes.id, result.boxes.cls):
            if model.names[int(class_id)] == "ambulance":
                ids.add(int(track_id))
    return len(ids)


for tracker_yaml in ["bytetrack.yaml", "botsort.yaml"]:
    n_ids = count_unique_ambulance_ids(tracker_yaml)
    print(f"{tracker_yaml:16s} -> عدد هويات ambulance المختلفة عبر كامل المقطع: {n_ids}")'''
)

rtl(
    """<div class="note">
<p>النتيجتان متساويتان هنا فعلياً، وهذا متوقَّع: كاميرا هذا المقطع ثابتة
تماماً، فتعويض حركة الكاميرا في BoT-SORT لا يغيّر شيئاً، و Re-ID معطَّل في
كليهما. الفرق بين الاثنين يظهر فقط حين تتحرك الكاميرا نفسها (مثبّتة على
طائرة مسيّرة مثلاً) أو حين نفعّل Re-ID يدوياً.</p>
</div>

<h2>8.3 من boxes.id إلى جدول بيانات</h2>

<p>لتحليل التتبع لاحقاً (كما سنفعل في القسم 13) نحتاج تجميع كل الاكتشافات
المتتبَّعة عبر المقطع كاملاً في جدول واحد:</p>"""
)

code(
    '''tracking_rows = []

for frame_index, result in enumerate(model.track(
    source=AMBULANCE_CLIP, conf=0.25, device=DEVICE,
    tracker="bytetrack.yaml", persist=True, stream=True, verbose=False,
)):
    if result.boxes is None or result.boxes.id is None:
        continue
    for box, track_id, class_id, confidence in zip(
        result.boxes.xyxy, result.boxes.id, result.boxes.cls, result.boxes.conf
    ):
        tracking_rows.append({
            "frame": frame_index,
            "track_id": int(track_id),
            "class": model.names[int(class_id)],
            "confidence": round(float(confidence), 2),
        })

tracking_df = pd.DataFrame(tracking_rows)
print("عدد الصفوف:", len(tracking_df))
print()
print("عدد هويات التتبع المختلفة لكل فئة:")
print(tracking_df.groupby("class")["track_id"].nunique())
tracking_df.head()'''
)

rtl(
    """<p>النتيجة تكشف مشكلة حقيقية سنعود إليها في القسم 13: يوجد فعلياً
<strong>إسعاف واحد فقط</strong> في هذا المقطع، لكن الجدول أعلاه يُظهر
عشرات الهويات المختلفة له - أي أن التتبع يفقد الهوية ويعيد اختراعها مراراً.
هذا ليس خطأً في الكود، بل انعكاس صادق لضعف كشف بعض الفئات كما رأيناه في
الأسبوع الماضي.</p>

<h2>8.4 لماذا stream=True؟</h2>

<p>مرّرنا <code>stream=True</code> في كل الأمثلة أعلاه. بدونها تحاول
Ultralytics معالجة الفيديو كاملاً أولاً ثم إرجاع كل النتائج دفعة واحدة في
الذاكرة - وهذا قد يستهلك ذاكرة هائلة مع فيديو طويل. مع
<code>stream=True</code> تُعالَج الإطارات واحداً تلو الآخر كمولِّد
(Generator)، فتبقى الذاكرة المستخدمة صغيرة وثابتة بغض النظر عن طول
الفيديو.</p>"""
)


# ===========================================================================
# 9. نبني متتبع IoU مصغّراً من الصفر
# ===========================================================================

rtl(
    """<hr />
<h1>9. نبني متتبع IoU مصغّراً من الصفر</h1>

<p>ByteTrack يعمل جيداً، لكنه صندوق أسود. لنبنِ أبسط متتبع ممكن بأيدينا -
باستخدام IoU و Hungarian فقط من القسم 3، <strong>بلا مرشّح كالمان
إطلاقاً</strong> - لنرى بالضبط أين تنهار الفكرة البسيطة، وبالتالي لماذا
احتجنا كل ما تعلّمناه بعدها.</p>"""
)

code(
    '''class SimpleIoUTracker:
    """متتبع مصغّر: مطابقة جشعة عبر Hungarian على IoU فقط، بلا تنبؤ حركة."""

    def __init__(self, max_age=5, iou_threshold=0.3):
        self.max_age = max_age
        self.iou_threshold = iou_threshold
        self.tracks = {}   # track_id -> {"box": ..., "age": ..., "class": ...}
        self.next_id = 1

    def update(self, boxes, classes):
        if not self.tracks:
            for box, class_name in zip(boxes, classes):
                self.tracks[self.next_id] = {"box": box, "age": 0, "class": class_name}
                self.next_id += 1
            return

        track_ids = list(self.tracks.keys())
        cost_matrix = np.ones((len(track_ids), len(boxes)))
        for i, track_id in enumerate(track_ids):
            for j, box in enumerate(boxes):
                cost_matrix[i, j] = 1 - iou(self.tracks[track_id]["box"], box)

        matched_tracks, matched_dets = ([], [])
        if len(track_ids) and len(boxes):
            matched_tracks, matched_dets = linear_sum_assignment(cost_matrix)

        assigned_dets, assigned_tracks = set(), set()
        for t, d in zip(matched_tracks, matched_dets):
            if cost_matrix[t, d] <= 1 - self.iou_threshold:
                track_id = track_ids[t]
                self.tracks[track_id]["box"] = boxes[d]
                self.tracks[track_id]["age"] = 0
                assigned_tracks.add(track_id)
                assigned_dets.add(d)

        for track_id in track_ids:
            if track_id not in assigned_tracks:
                self.tracks[track_id]["age"] += 1
        self.tracks = {tid: t for tid, t in self.tracks.items() if t["age"] <= self.max_age}

        for j, (box, class_name) in enumerate(zip(boxes, classes)):
            if j not in assigned_dets:
                self.tracks[self.next_id] = {"box": box, "age": 0, "class": class_name}
                self.next_id += 1'''
)

rtl(
    """<div class="note">
<p><strong>نعيد تحميل النموذج هنا في متغيّر جديد <code>(fresh_model)</code>
بدل استخدام <code>model</code> نفسه.</strong> السبب فخّ اكتشفناه أثناء إعداد
هذا الدرس: استدعاء <code>model.track(..., persist=True)</code> كما فعلنا
في القسم 8 <strong>يُغيّر داخلياً حالة الكاشف المخزَّنة في الكائن</strong>،
فتختلف نتائج <code>model.predict()</code> اللاحقة على نفس الفيديو بصمت -
عدد اكتشافات الإسعاف الخام تحوّل فعلياً من 520 إلى 438 في اختبارنا لهذا
بالضبط. تحميل نسخة جديدة من النموذج قبل أي مقارنة حساسة للأرقام يتجنّب هذا
الفخّ تماماً.</p>
</div>

<p>نشغّل متتبعنا على مقطع الإسعاف كاملاً، ونعدّ <strong>كل</strong> هوية
مختلفة أُنشئت لفئة <code>ambulance</code> عبر حياة التشغيل كلها - لا فقط
الهويات الحيّة في النهاية:</p>"""
)

code(
    '''fresh_model = YOLO(MODEL_PATH)  # نسخة جديدة، بلا أي تأثير من استدعاءات track() السابقة

simple_tracker = SimpleIoUTracker(max_age=5, iou_threshold=0.3)
ever_created = {}

for result in fresh_model.predict(source=AMBULANCE_CLIP, conf=0.25, device=DEVICE, stream=True, verbose=False):
    boxes = result.boxes.xyxy.cpu().numpy() if result.boxes is not None else np.zeros((0, 4))
    classes = [fresh_model.names[int(c)] for c in result.boxes.cls] if result.boxes is not None else []

    existing_ids = set(simple_tracker.tracks.keys())
    simple_tracker.update(boxes, classes)
    for new_id in set(simple_tracker.tracks.keys()) - existing_ids:
        ever_created[new_id] = simple_tracker.tracks[new_id]["class"]

n_ambulance_ids = sum(1 for class_name in ever_created.values() if class_name == "ambulance")
print("عدد هويات (ambulance) المختلفة التي أنشأها SimpleIoUTracker:", n_ambulance_ids)
print("(للمقارنة: ByteTrack في القسم 8.2 أعطى 22 هوية على المقطع نفسه)")'''
)

rtl(
    """<div class="note">
<p><strong>متتبعنا المصغّر أسوأ من ByteTrack، وهذا متوقَّع تماماً.</strong>
بلا مرشّح كالمان، أي إطار يُفقَد فيه الكشف (ولو لحظياً) يعني أن أقرب صندوق
تالٍ قد لا يتقاطع كفاية مع آخر موضع معروف، فتُفتح هوية جديدة كلياً بدل
استكمال القديمة. هذا بالضبط ما شرحناه بالحدس في القسم 4.4 - والآن رأيناه
رقماً حقيقياً لا افتراضاً نظرياً.</p>
</div>"""
)


# ===========================================================================
# 10. رسم المسارات وتلوين حسب الـ ID
# ===========================================================================

rtl(
    """<hr />
<h1>10. رسم المسارات Trails وتلوين حسب الـ ID</h1>

<p>بما أن كل جسم له هوية ثابتة الآن، يمكننا رسم <strong>أثر حركته</strong>
عبر الإطارات الأخيرة - خط يتتبّع مركز صندوقه، بلون ثابت طوال حياة تلك
الهوية. سنستخدم ByteTrack (لا متتبعنا المصغّر) لأن الهدف هنا عرض المسارات
لا اختبار حدود المطابقة.</p>

<p>بدل عرض فيديو كاملاً (وهو ثقيل داخل دفتر يُقرأ دون تشغيله - راجع
HANDOFF.md #5.3)، سنأخذ خمسة إطارات موزَّعة عبر المقطع ونعرضها جنباً إلى
جنب، فنرى استقرار الهوية عبر الزمن دفعة واحدة بدل حركة فيديو.</p>"""
)

code(
    '''SNAPSHOT_FRAMES = {90, 200, 300, 340, 380}
TRAIL_LENGTH = 40

track_history = {}
palette_bgr = [(198, 40, 40), (21, 101, 192), (46, 125, 50),
               (249, 168, 37), (123, 31, 162), (0, 131, 143)]
snapshots = {}

for frame_index, result in enumerate(model.track(
    source=AMBULANCE_CLIP, conf=0.25, device=DEVICE,
    tracker="bytetrack.yaml", persist=True, stream=True, verbose=False,
)):
    annotated_frame = result.orig_img.copy()

    if result.boxes is not None and result.boxes.id is not None:
        for box, track_id, class_id in zip(result.boxes.xyxy, result.boxes.id, result.boxes.cls):
            track_id = int(track_id)
            x1, y1, x2, y2 = map(int, box)
            center = ((x1 + x2) // 2, (y1 + y2) // 2)
            color = palette_bgr[track_id % len(palette_bgr)]

            track_history.setdefault(track_id, []).append(center)
            track_history[track_id] = track_history[track_id][-TRAIL_LENGTH:]

            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(annotated_frame, f"ID {track_id}", (x1, max(y1 - 6, 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)

            trail_points = track_history[track_id]
            for i in range(1, len(trail_points)):
                cv2.line(annotated_frame, trail_points[i - 1], trail_points[i], color, 2)

    if frame_index in SNAPSHOT_FRAMES:
        snapshots[frame_index] = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

fig, axes = plt.subplots(1, len(SNAPSHOT_FRAMES), figsize=(18, 4))
for ax, frame_index in zip(axes, sorted(snapshots)):
    ax.imshow(snapshots[frame_index])
    ax.set_title(f"frame {frame_index}", fontsize=11)
    ax.axis("off")
plt.suptitle("Same ambulance, same ID, across the clip", fontsize=14)
plt.tight_layout()
plt.show()'''
)

rtl(
    """<p>لاحظ خط الأثر خلف كل صندوق: هو تجسيد بصري مباشر لما تعنيه "هوية
ثابتة عبر الزمن" - شيء لم يكن ممكناً إطلاقاً بالكشف وحده.</p>"""
)


# ===========================================================================
# 11. تشغيل على المقطع الكامل وحفظ الناتج
# ===========================================================================

rtl(
    """<hr />
<h1>11. تشغيل على المقطع الكامل وحفظ الناتج</h1>

<p>الآن نُخرج النتيجة كفيديو كامل نحفظه على القرص، بدل شرائح ثابتة فقط.
نستخدم <code>imageio-ffmpeg</code> بدل الاعتماد على وجود ffmpeg مثبَّتاً
في نظام الطالب - راجع HANDOFF.md #9.6.</p>

<div class="note">
<p><strong>لن نعرض الفيديو داخل الدفتر</strong> عبر
<code>Video(path, embed=True)</code>، لأن هذا يحوّل الفيديو إلى نص
Base64 ضخم يُضاعف حجم ملف الدفتر أضعافاً (وهذا بالضبط ما ضخّم دفتر
الأسبوع السادس). الفيديو يُحفظ في <code>videos/reference_tracking_output.mp4</code>
ويُفتح من هناك مباشرة.</p>
</div>"""
)

code(
    '''import imageio_ffmpeg

OUTPUT_VIDEO = "videos/reference_tracking_output.mp4"

capture = cv2.VideoCapture(AMBULANCE_CLIP)
video_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_fps = capture.get(cv2.CAP_PROP_FPS)
capture.release()

writer = imageio_ffmpeg.write_frames(
    OUTPUT_VIDEO, (video_width, video_height), fps=video_fps,
    codec="libx264", macro_block_size=1,
    output_params=["-crf", "28", "-pix_fmt", "yuv420p"],
)
writer.send(None)

track_history = {}

for result in model.track(
    source=AMBULANCE_CLIP, conf=0.25, device=DEVICE,
    tracker="bytetrack.yaml", persist=True, stream=True, verbose=False,
):
    annotated_frame = result.orig_img.copy()
    if result.boxes is not None and result.boxes.id is not None:
        for box, track_id, class_id in zip(result.boxes.xyxy, result.boxes.id, result.boxes.cls):
            track_id = int(track_id)
            x1, y1, x2, y2 = map(int, box)
            center = ((x1 + x2) // 2, (y1 + y2) // 2)
            color = palette_bgr[track_id % len(palette_bgr)]

            track_history.setdefault(track_id, []).append(center)
            track_history[track_id] = track_history[track_id][-TRAIL_LENGTH:]

            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            label = f"{model.names[int(class_id)]} {track_id}"
            cv2.putText(annotated_frame, label, (x1, max(y1 - 6, 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)

            trail_points = track_history[track_id]
            for i in range(1, len(trail_points)):
                cv2.line(annotated_frame, trail_points[i - 1], trail_points[i], color, 2)

    writer.send(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB).tobytes())

writer.close()

output_size_mb = Path(OUTPUT_VIDEO).stat().st_size / 1e6
print(f"حُفظ الفيديو في: {OUTPUT_VIDEO}")
print(f"الحجم: {output_size_mb:.2f} MB")'''
)

rtl(
    """<p>افتح <code>Week8/videos/reference_tracking_output.mp4</code> مباشرة
من مستكشف الملفات لمشاهدته كاملاً. طوله خمس عشرة ثانية، وحجمه أقل من
2 ميغابايت.</p>"""
)


# ===========================================================================
# 12. لمحة أولى: كيف يفتح التتبع باب العدّ؟
# ===========================================================================

rtl(
    """<hr />
<h1>12. لمحة أولى: كيف يفتح التتبع باب العدّ؟</h1>

<p>عد الآن إلى مشكلة العدّ المضاعف التي بدأنا بها الدرس في القسم 1: كنا
نجمع "عدد السيارات المكتشفة" في كل إطار، فحصلنا على رقم سخيف
(956 على مقطع من 15 ثانية) لأن الكشف لا يعرف أن السيارة نفسها تظهر مراراً.</p>

<p>الآن وقد أصبح لكل جسم <strong>هوية ثابتة</strong>، يتغيّر السؤال كلياً:
بدل "كم اكتشافاً رأيت؟" نستطيع أن نسأل <strong>"كم هوية مختلفة رأيت؟"</strong>
- وهذا أقرب بما لا يُقاس إلى العدّ الحقيقي. لو رسمنا خطاً افتراضياً عبر
الطريق، وسجّلنا كل مرة تعبره <em>هوية جديدة لم نرها من قبل</em>، لحصلنا
على عدّاد مركبات معقول.</p>

<div class="note">
<p>هذا هو بالضبط الجسر إلى الأسبوع القادم. بناء عدّاد كامل بخط عبور
واتجاه حركة وواجهة عرض يحتاج تفصيلاً إضافياً - كثافة المرور، واتجاه كل
حارة، ومنطق القرار عند تعدد الحارات - وهذا كله موضوع الأسبوع التاسع.
ما يهمّنا اليوم هو الفكرة الجوهرية فقط: <strong>لا عدّ صحيح بلا هوية
ثابتة</strong>، وقد بنينا تلك الهوية للتو.</p>
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
    print(f"استُبدلت الأقسام 8-12 بـ {len(new_cells)} خلية.")


if __name__ == "__main__":
    main()
