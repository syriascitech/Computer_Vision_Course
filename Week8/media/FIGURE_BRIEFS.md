# أوصاف أشكال الأسبوع 8

هذا الملف **ليس جزءاً من الدرس**. هو ورقة عمل لمن ينتج الصور: كل شكل مذكور
هنا بوصفه الكامل، والدفتر يشير إليه بمسار نسبي `media/<name>.jpg` مع مرجع
احتياطي على مرآة المستودع العامة (راجع HANDOFF.md #5.2).

الأسماء والأرقام يجب أن تطابق ما في الدفتر تماماً. الأرقام تسلسلية من 1
داخل هذا الأسبوع فقط (لا تكمل ترقيم الأسبوع السابع).

**تنبيه: هذا الأسبوع يخالف قاعدة الأسبوع السابع في لغة النص داخل الشكل** -
راجع سطر "اللغة" في دليل النمط أدناه قبل أن ترسم أي شكل.

---

## دليل النمط الموحّد

يطبَّق على كل شكل في هذا الأسبوع بلا استثناء.

```
Format   : JPG, quality 85, logical width 1600px (1600x900 for wide figures).
Canvas   : explicit solid WHITE (#FFFFFF) background, never transparent,
           so it stays readable in both light and dark Jupyter themes.
Language : Titles, panel/section headings, and explanatory captions or
           sentences INSIDE the figure are ARABIC - written correctly
           shaped and right-to-left, the same as the notebook's own
           prose. Technical terms, algorithm/step names, parameter and
           variable names, and short code-style labels stay in ENGLISH
           exactly as printed in the notebook's code cells - e.g. IoU,
           Kalman, Hungarian, SORT, DeepSORT, ByteTrack, BoT-SORT,
           Detect / Predict / Associate / Update / Create / Delete,
           Tentative / Confirmed / Deleted, min_hits, max_age,
           track_buffer, conf=0.91, T1, D1, ID 7, Track A. This mirrors
           exactly how the notebook's own Arabic markdown mixes in
           English technical terms - do not translate those terms.
Font     : a font with full Arabic glyph coverage and correct shaping
           (e.g. Arial, Tahoma, Noto Sans Arabic - NOT DejaVu Sans,
           which has no Arabic glyphs). English terms inside an Arabic
           sentence stay left-to-right islands within the RTL line,
           exactly like the notebook's own `.rtl-cell` CSS handles
           inline `<code>`.
Palette  : #1565C0 blue   = ground truth / motion-only / "before"
           #2E7D32 green  = correct match / confirmed / high-confidence
           #C62828 red    = error / deleted / wrong pairing
           #F9A825 amber  = warning / low-confidence / tentative / prediction
           #616161 grey   = neutral, arrows, axes, secondary text
           #ECEFF1 light  = panel fills
Drawing  : completely flat. No gradients, no shadows, no 3D, NO EMOJI.
           Boxes: rounded rectangles, pad 0.4, linewidth 2.
           Arrows: plain "-|>" heads in grey (or in the palette colour when
           the arrow itself carries meaning, e.g. a "wrong" arrow in red).
           Check / cross marks: text glyphs are OK, coloured by role.
Type size: title 18-20pt bold, panel titles 14pt bold, labels 13pt,
           annotations 11-12pt. Formulas via matplotlib mathtext or plain
           monospace text (numbers and mathematical symbols are
           language-neutral - keep them as digits/symbols, not spelled out).
Output   : save to Week8/media/<exact filename>, referenced from the
           notebook by a RELATIVE path only.
```

Every brief below marks the exact on-image text in quotes. Text in quotes
that is Arabic is meant to render as Arabic in the final image; short
English tokens quoted alongside it (T1, ID 7, conf=0.91, min_hits, ...)
stay Latin script exactly as shown, inline within the Arabic layout.

---

## Figure 1 — `iou_cost_matrix.jpg`
**موضعه:** القسم 3.2 · **الأولوية:** أساسي

```
Title (Arabic): "بناء مصفوفة التكلفة من IoU"
Size : 1600 x 900

LEFT LABEL (above the grid, right-aligned - Arabic)
  "المسارات (الإطار السابق)" in grey, 13pt

TOP LABEL (above the grid, centred over the columns - Arabic)
  "الاكتشافات (الإطار الحالي)" in grey, 13pt

GRID -- a 3x3 matrix, rows labelled T1/T2/T3 (bold, English, right of
grid since the layout is RTL), columns labelled D1/D2/D3 (bold, English,
above grid). Fill the nine cells with these exact IoU values, so the
figure's numbers match the notebook's own code cell in section 3.3
exactly:

           D1     D2     D3
    T1   0.82   0.10   0.00
    T2   0.15   0.75   0.05
    T3   0.00   0.20   0.68

  Colour each cell by value: >= 0.5 fill GREEN with white bold text,
  0.2-0.5 fill AMBER with white bold text, < 0.2 fill LIGHT (#ECEFF1)
  with grey text. Leave a few pixels of white gap between cells (like a
  confusion-matrix grid, not touching borders).

BOTTOM (well below the grid, generous vertical gap so it never collides
with the grid or the column labels above it) - Arabic sentences with the
technical terms kept in English inline:
  Line 1, 15pt, dark grey: "التكلفة = 1 − IoU   (تكلفة أقل = تشابه أعلى)"
  Line 2, 12pt grey, two lines: "تبحث Hungarian في المصفوفة كاملة عن
  التخصيص الأقل تكلفة إجمالاً - لا عن أكبر قيمة منفردة فقط."

IMPORTANT: leave enough vertical space between the title and the
"الاكتشافات (الإطار الحالي)" label above the grid, and between the grid
and the bottom caption, so nothing overlaps at 1600x900 with the type
sizes above. Remember the overall layout reads right-to-left, so the row
label "المسارات (الإطار السابق)" and the T1/T2/T3 row labels sit on the
RIGHT of the grid, and column order should still visually read D1, D2,
D3 left-to-right beneath "الاكتشافات (الإطار الحالي)" to match the
matrix values above exactly - do not mirror the D1/D2/D3 order itself,
only the overall page direction.
```

---

## Figure 2 — `hungarian_assignment.jpg`
**موضعه:** القسم 3.3 · **الأولوية:** أساسي

```
Title (Arabic): "التخصيص الذي اختارته خوارزمية Hungarian"
Size : 1600 x 800

Same 3x3 grid and same IoU values as Figure 1 (T1/T2/T3 x D1/D2/D3, kept
in English as variable labels), but now recoloured to show the SOLUTION
rather than the raw matrix:
  - Chosen cells (T1-D1 = 0.82, T2-D2 = 0.75, T3-D3 = 0.68): fill GREEN,
    with a thick RED (#C62828) border (linewidth 4) to make the chosen
    diagonal pop out visually, white bold text for the value.
  - All other cells: fill LIGHT (#ECEFF1), thin white border, grey text.

BOTTOM (single line, 14pt, dark grey, comfortable gap below the grid) -
Arabic sentence, keep T1/D1 etc. and the word IoU in English inline:
  "التخصيص المختار: T1-D1, T2-D2, T3-D3   -   مجموع IoU = 2.25 (الحد
  الأقصى الممكن لهذه المصفوفة)"
```

---

## Figure 3 — `kalman_predict_update.jpg`
**موضعه:** القسم 4.3 · **الأولوية:** أساسي

```
Title (Arabic): "دورة التنبؤ ثم التحديث في مرشّح كالمان"
Size : 1600 x 700  (four panels in a row, connected by grey "-|>" arrows)

Each panel is a rounded box, wide enough that its text never clips at the
box edges (make boxes at least 260px wide for the longest label):

  Panel 1 heading "Frame t-1"   (fill BLUE)   -> body text (Arabic):
      "صندوق مسار (مؤكَّد)"
  Panel 2 heading "Predict"     (fill AMBER)  -> body text (Arabic):
      "تحريك الصندوق حسب آخر سرعة معروفة"
  Panel 3 heading "Frame t"     (fill GREEN)  -> body text (Arabic):
      "وصول كشف حقيقي"
  Panel 4 heading "Update"      (fill GREEN)  -> body text (Arabic):
      "تصحيح الصندوق والسرعة باستخدام الكشف"

Panel headings ("Frame t-1", "Predict", "Frame t", "Update" - kept in
English, they are the exact step names used in the notebook's own SORT
pipeline description) sit ABOVE each box in bold black 14pt, not inside
it. The Arabic body text goes INSIDE each box in white.

BOTTOM STRIP (13pt, grey, centred, two lines, clear of the boxes) -
Arabic:
  "تتكرّر هذه الدورة في كل إطار: تنبّأ بموضع الصندوق المتوقَّع، ثم صحِّح
   هذا التنبؤ بالكشف الحقيقي فور وصوله."
```

---

## Figure 4 — `kalman_occlusion.jpg`
**موضعه:** القسم 4.4 · **الأولوية:** أهم شكل في الأقسام 1-7

```
Title (Arabic): "كيف ينقذنا التنبؤ في مرشّح كالمان أثناء حجب كامل"
Size : 1600 x 800  (a five-panel filmstrip)

Five panels, each a light grey (#ECEFF1) "road" rectangle containing one
tracked box, with a small grey ">" arrow between consecutive panels.
Because the page is RTL, lay the five panels out right-to-left so
"frame 1" is on the RIGHT and "frame 5" is on the LEFT, arrows pointing
leftward (matching normal Arabic reading order) - the frame NUMBERS
stay in ascending order 1->5, only their screen position mirrors.

Panel headings ("frame 1" .. "frame 5" - keep "frame" in English exactly
as printed by the notebook's own frame-index prints, e.g. "frame 90")
sit ABOVE each panel in bold, with one line of smaller grey Arabic
caption text below the heading and ABOVE the panel itself (not
overlapping the box or the bottom caption):

  frame 1: solid GREEN box labelled "ID 7" above it.
           Caption (Arabic): "مرئي"
  frame 2: a dark grey solid rectangle (a "حاجز" - e.g. a bus) drawn
    overlapping the tracked box; the tracked box itself becomes a
    DASHED grey rectangle labelled "ID 7" with a small Arabic tag next
    to it: "(تنبؤ)". Caption (Arabic): "محجوب (بلا كشف)"
  frame 3: same as frame 2, occluder still present, dashed grey box has
    moved slightly further along its predicted path. Caption (Arabic):
    "محجوب (بلا كشف)"
  frame 4: occluder gone, a solid GREEN box appears near where the
    dashed prediction had drifted to, labelled "ID 7". Caption (Arabic):
    "يظهر مجدداً - يُطابَق مع التنبؤ"
  frame 5: solid GREEN box, "ID 7". Caption (Arabic): "متتبَّع من جديد"

BOTTOM (well below the filmstrip, two lines, 12-13pt, dark grey/black) -
Arabic, keeping "ID" in English inline:
  "يستمر الصندوق بالحركة بآخر سرعة معروفة طوال الحجب (متقطّع، رمادي)،
   فحين يظهر الجسم مجدداً يكون التنبؤ قريباً بما يكفي لإعادة مطابقة نفس
   الـ ID - بدون هذا التنبؤ لبدا الأمر جسماً جديداً كلياً."

IMPORTANT: give real vertical breathing room between (a) the title,
(b) the panel row, (c) the per-panel caption line, and (d) the bottom
paragraph. Nothing should touch or overlap - this failure mode (text
sitting on top of other text) is the single most common mistake when
this brief gets rendered, watch for it deliberately. Also double-check
the right-to-left panel ordering described above before finalising.
```

---

## Figure 5 — `sort_pipeline.jpg`
**موضعه:** القسم 5.1 · **الأولوية:** أساسي

```
Title (Arabic): "خط أنابيب SORT كاملاً"
Size : 1600 x 550

MAIN ROW, laid out right-to-left (first step on the right, matching
Arabic reading direction), connected by grey "-|>" arrows pointing
leftward, four boxes with these EXACT English labels (these are the
same step names used verbatim in the notebook's own section 5.1 list):
  "Detect" (BLUE) -> "Predict (Kalman)" (AMBER) ->
  "Associate (Hungarian)" (GREEN) -> "Update" (GREEN)

From "Associate (Hungarian)", two additional grey arrows branch off
diagonally to two smaller GREY boxes placed above and below the main
row, positioned so they do NOT overlap the main row's boxes or arrows,
labelled in English (again matching the notebook's own step names):
  upper: "Create (new track)"
  lower: "Delete (lost track)"

BOTTOM STRIP (13pt, grey, single line, clear of every box) - Arabic:
  "الاكتشافات غير المرتبطة تبدأ مسارات جديدة؛ المسارات غير المرتبطة
   تتقادم ثم تُحذف في النهاية."

Make sure the canvas is tall/wide enough (or the branch boxes small and
close enough to the main row) that the bottom strip text never collides
with the "Delete" box above it.
```

---

## Figure 6 — `track_lifecycle_state_machine.jpg`
**موضعه:** القسم 5.2 · **الأولوية:** أساسي

```
Title (Arabic): "دورة حياة المسار: من Tentative إلى Confirmed إلى Deleted"
Size : 1600 x 550

THREE boxes in a row (right-to-left order: "Tentative" on the right ->
"Confirmed" in the middle -> "Deleted" on the left, matching Arabic
reading direction), connected by grey arrows. Keep the three state
names in English exactly - they are the standard tracking-literature
terms used as-is in the notebook prose:
  "Tentative" (AMBER) -> "Confirmed" (GREEN) -> "Deleted" (RED)

Arrow labels, Arabic sentences with the parameter names kept in English
inline:
  Tentative -> Confirmed: "تحقّق min_hits من المطابقات المتتالية"
  Confirmed -> Deleted:   "مرور max_age من الإطارات بلا أي مطابقة"

A FOURTH path, drawn in RED, going directly from "Tentative" down and
across to "Deleted" (bypassing "Confirmed" entirely), labelled in
Arabic:
  "لا مطابقة قبل min_hits -> يُحذف فوراً"
Route this red path clearly below the three main boxes so it never
overlaps the min_hits / max_age labels above the main arrows.
```

---

## Figure 7 — `id_switch_example.jpg`
**موضعه:** القسم 5.3 · **الأولوية:** أساسي

```
Title (Arabic): "تبديل الهوية: جسمان متشابهان يتقاطعان فيتبادلان الهوية"
Size : 1600 x 650  (two side-by-side panels, arranged right-to-left:
"before" panel on the RIGHT, "after" panel on the LEFT, matching Arabic
reading order)

RIGHT PANEL, headed (Arabic) "قبل التقاطع":
  Two open rectangles (no fill, just a coloured outline, linewidth 3):
  a BLUE one labelled "ID 3" above it, a RED one labelled "ID 5" above
  it, approaching each other. A short double-headed arrow between them
  (blue on one half, red on the other half) showing them approaching.
  Caption below, grey, two lines, Arabic: "سيارتان متشابهتان تقتربان
  بشدة من بعضهما"

LEFT PANEL, headed (Arabic) "بعد التقاطع - تبادلت الهويتان":
  Same two rectangles, same relative positions, but now the identity
  colours have swapped: the box that was BLUE/"ID 3" is now RED/"ID 5"
  and vice versa - i.e. the colours (identities) swapped while the
  physical positions stayed put. Caption below, in RED, two lines,
  Arabic: "الربط الحركي وحده اختار الإقران الخطأ عند أقرب نقطة تلاقٍ"

Keep generous vertical space between each panel's heading, its box row,
and its caption. "ID 3" and "ID 5" stay in English/Latin digits in both
panels.
```

---

## Figure 8 — `bytetrack_two_stage.jpg`
**موضعه:** القسم 7.2 · **الأولوية:** أهم شكل في الدرس كله

```
Title (Arabic): "ByteTrack: الربط على مرحلتين"
Size : 1600 x 800

RIGHT COLUMN (first, matching Arabic reading order), headed (Arabic,
bold, 14pt) "اكتشافات هذا الإطار":
  Three GREEN boxes stacked vertically, labels kept in English exactly
  as the notebook prints them: "D1  conf=0.91", "D2  conf=0.88",
  "D3  conf=0.76", with a small green Arabic label under them: "عالية
  الثقة"
  Below that, with a clear vertical gap, two AMBER boxes: "D4  conf=0.31",
  "D5  conf=0.18", with a small amber Arabic label under them: "منخفضة
  الثقة - محفوظة لا مرميّة"

LEFT COLUMN, headed (Arabic, bold, 14pt) "المسارات الموجودة":
  Three boxes stacked vertically: "Track A" (BLUE), "Track B" (BLUE),
  "Track C" with a small Arabic tag next to it "(محجوب)" (GREY)

ARROWS:
  Stage 1 (solid GREEN arrows): D1 -> Track A, D2 -> Track B. Label this
  pair of arrows once, centred between the columns at their height,
  Arabic with "stage 1" written as "المرحلة 1": "المرحلة 1: مطابقة
  الاكتشافات عالية الثقة بالمسارات" - position this label so it sits
  BETWEEN the two arrows, not directly on top of either arrow line.
  Stage 2 (dashed AMBER arrow): D4 -> Track C. Label near it, clear of
  the arrow line itself, Arabic: "المرحلة 2: المسارات المتبقّية بلا
  مطابقة تجرّب مجموعة الثقة المنخفضة بدل أن تُهمَل"

BOTTOM (two lines, 12-13pt, dark grey/black, well clear of the D4/D5
boxes and their "منخفضة الثقة" label above them) - Arabic, keep
"ByteTrack" in English inline:
  "هذا بالضبط سبب نجاة ByteTrack من الحجب الجزئي: جسم بالكاد مرئي ما زال
   ينتج صندوقاً منخفض الثقة، والمرحلة الثانية تمنح مساره فرصة أخيرة قبل
   التخلّي عنه."

IMPORTANT: this is the most-referenced figure in the whole lesson - keep
every label clear of every arrow line and clear of every other label.
Use a tall enough canvas (or smaller boxes) that the two detection
groups, their two Arabic captions, and the bottom paragraph all have
their own clean vertical space with no overlap. Remember the RTL layout:
detections column on the RIGHT, tracks column on the LEFT, arrows
pointing leftward.
```
