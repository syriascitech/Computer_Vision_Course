# 🎓 مسار الرؤية الحاسوبية — مجموعة تمارين تطبيقية (الأسبوع 1 + الأسبوع 2)

> مُشتقة مباشرة من محتوى دفتري: **Week 1 — Python Review, NumPy & Image Representation** و **Week 2 — OpenCV ومعالجة الفيديو**.
> جميع التمارين تلتزم بنفس المصطلحات، المكتبات، ومستوى الصعوبة المستخدم في الدفترين الأصليين، ولا تُقدّم أي مفهوم أو مكتبة لم تُذكر فيهما.

---

## 1. جرد المواضيع المستخرجة (Extracted Programming Topics)

### 🟢 Beginner

| الموضوع | المفاهيم/الدوال المرتبطة | الملف المصدر |
|---|---|---|
| المتغيرات وأنواع البيانات | `int`, `float`, `str`, `bool`, type casting | Week 1 |
| العوامل (Operators) | حسابية، مقارنة، منطقية | Week 1 |
| السلاسل النصية | slicing، `.upper()`, `.strip()`, `.replace()`, `.split()` | Week 1 |
| القوائم (Lists) | `append`, `insert`, `remove`, `pop`, `sort`, slicing | Week 1 |
| Tuples / Sets / Dictionaries | immutability، unique elements، key:value | Week 1 |
| الشروط (if/elif/else) | مقارنات منطقية | Week 1 |
| الحلقات (for/while) | `range()` | Week 1 |
| NumPy: إنشاء المصفوفات | `np.array`, `np.zeros`, `np.ones`, `np.arange`, `np.linspace`, `np.random.rand` | Week 1 |
| خصائص المصفوفة | `shape`, `ndim`, `size`, `dtype`, `.astype()` | Week 1 |
| تمثيل الصورة الرمادية (Grayscale) كمصفوفة 2D | `uint8`, قيم 0–255 | Week 1 |
| تمثيل صورة RGB كمصفوفة 3D | `(H, W, C)`, فهرسة القنوات | Week 1 |
| فضاءات الألوان: Grayscale / RGB / BGR / HSV (مفهومياً) | تفاعل ألوان (ipywidgets) | Week 2 |
| تحميل صورة وعرضها | `requests`, `cv2.imdecode`, `cv2.imread`, `plt.imshow` | Week 2 |
| تصحيح الألوان BGR→RGB | `cv2.cvtColor(..., cv2.COLOR_BGR2RGB)` | Week 2 |
| القص عبر Slicing | `img[y1:y2, x1:x2]` | Week 2 |
| تغيير الحجم | `cv2.resize` | Week 2 |
| الانعكاس | `cv2.flip` (0, 1, -1) | Week 2 |

### 🟡 Intermediate

| الموضوع | المفاهيم/الدوال المرتبطة | الملف المصدر |
|---|---|---|
| الدوال (Functions) | `def`, `return`, `**kwargs` | Week 1 |
| الفهرسة والتقطيع متعدد الأبعاد | `arr[a:b, c:d]`, boolean masking | Week 1 |
| العمليات الرياضية والمحاور | `np.sum`, `np.mean`, `np.max`, `axis=0/1` | Week 1 |
| Broadcasting | توسيع الأبعاد تلقائياً | Week 1 |
| Reshape / Flatten / Transpose | `.reshape()`, `.flatten()`, `.T`, `np.newaxis` | Week 1 |
| المصفوفات العشوائية | `np.random.seed`, `randint`, `randn` | Week 1 |
| ضبط السطوع مع تفادي Overflow | `.astype(int16)`, `np.clip` | Week 1 |
| تحويل RGB→Grayscale يدوياً | `0.299R + 0.587G + 0.114B` | Week 1 |
| فصل القنوات اللونية | `cv2.split` | Week 2 |
| التدوير | `cv2.getRotationMatrix2D`, `cv2.warpAffine` | Week 2 |
| الرسم والتعليق | `cv2.line`, `cv2.rectangle`, `cv2.circle`, `cv2.putText` (على نسخة `.copy()`) | Week 2 |
| الهيستوغرام | `cv2.calcHist` | Week 2 |
| العتبة اليدوية (Thresholding) | `cv2.threshold(..., cv2.THRESH_BINARY)` | Week 2 |

### 🔴 Advanced

| الموضوع | المفاهيم/الدوال المرتبطة | الملف المصدر |
|---|---|---|
| عتبة Otsu التلقائية | `cv2.THRESH_BINARY + cv2.THRESH_OTSU` | Week 2 |
| العتبة التكيّفية | `cv2.adaptiveThreshold` (Mean/Gaussian) | Week 2 |
| العمليات على الصور الثنائية | `cv2.bitwise_not`, `cv2.countNonZero`, boolean masking للتراكب (Overlay) | Week 2 |
| مطابقة الهيستوغرام | `skimage.exposure.match_histograms` | Week 2 |
| معالجة الفيديو | `cv2.VideoCapture`, حلقة `while`, معالجة كل إطار، `cv2.putText` مباشر على الفيديو | Week 2 |

---

## 2. العلاقات بين المواضيع (Topic Relationships)

### Overlapping Topics (مشتركة بين الملفين)
- **تمثيل الصورة الرمادية (Grayscale):** يدوياً كمصفوفة NumPy 2D في الأسبوع 1، وعملياً عبر `cv2.cvtColor` في الأسبوع 2.
- **تمثيل RGB والقنوات:** فهرسة `img[:,:,0]` يدوياً في الأسبوع 1، مقابل `cv2.split` في الأسبوع 2.
- **الفهرسة والتقطيع (Slicing):** أساس القص (Cropping) في الأسبوع 2 هو بالضبط تقطيع المصفوفات من الأسبوع 1.
- **العمليات الإحصائية (`np.mean`, `np.sum`):** تُستخدم في الأسبوع 1 نظرياً، وفي الأسبوع 2 عملياً لحساب متوسط السطوع.

### Complementary Topics (تكمّل بعضها البعض)
- إنشاء المصفوفات العشوائية (W1) + إنشاء صور اختبار للتلاعب بها في OpenCV (W2).
- صيغة التحويل اليدوي RGB→Grayscale (W1) + `cv2.cvtColor` الجاهزة (W2) → تحقّق من صحة النتيجة.
- `np.clip` وضبط السطوع يدوياً (W1) + معالجة صور حقيقية محمّلة عبر OpenCV (W2).
- Boolean Masking و Normalization (W1) + Thresholding والعمليات الثنائية (W2).
- الإحصائيات (`np.mean` بمحور) (W1) + الهيستوغرام وتحليل الإضاءة اللحظي في الفيديو (W2).

---

## 3. خارطة طريق التمارين (Exercise Roadmap)

| # | التمرين | الموضوع الرئيسي | الصعوبة | المفاهيم المدمجة | المصدر |
|---|---|---|---|---|---|
| 1 | صورة رمادية يدوية والوصول للبكسلات | تمثيل الصورة (NumPy) | Beginner | `np.array`, `dtype=uint8`, فهرسة | W1 |
| 2 | إنشاء صورة RGB وتعديل بكسل | تمثيل RGB | Beginner | `np.zeros`, فهرسة القنوات | W1 |
| 3 | تحميل صورة وتصحيح الألوان | Color Spaces + I/O | Beginner | `cv2.imread/imdecode`, `cvtColor` | W2 |
| 4 | فصل القنوات وعرض قناة واحدة | Channel Splitting | Beginner | `cv2.split` | W2 |
| 5 | تغيير الحجم لأبعاد ثابتة | Resizing | Beginner | `cv2.resize` | W2 |
| 6 | خط أنابيب تحويلات هندسية | Resize+Rotate+Crop | Intermediate | `resize`, `getRotationMatrix2D`, `warpAffine`, slicing | W2 |
| 7 | RGB→Grayscale يدوياً مقابل OpenCV | تحويل الألوان | Intermediate | صيغة يدوية + `cvtColor` | W1+W2 |
| 8 | ضبط السطوع مع Clipping على صورة حقيقية | Pixel Manipulation | Intermediate | `astype(int16)`, `np.clip` | W1+W2 |
| 9 | الرسم والتعليق على نسخة من الصورة | Drawing & Annotation | Intermediate | `line`, `rectangle`, `putText`, `.copy()` | W2 |
| 10 | حساب ورسم الهيستوغرام لصورتين | Histogram | Intermediate | `cv2.calcHist`, `plt.plot` | W2 |
| 11 | عتبة ثنائية يدوية على مستند ممسوح | Thresholding | Intermediate | `cv2.threshold(BINARY)` | W2 |
| 12 | تطبيع (Normalize) مصفوفة قبل التحليل | Normalization | Intermediate | `(arr-min)/(max-min)`, boolean masking | W1 |
| 13 | مقارنة العتبة اليدوية وOtsu والتكيّفية | Advanced Thresholding | Advanced | `THRESH_OTSU`, `adaptiveThreshold` | W2 |
| 14 | خط أنابيب عمليات ثنائية (فحص تصنيع) | Binary Operations | Advanced | `bitwise_not`, `countNonZero`, Overlay | W2 |
| 15 | مطابقة الهيستوغرام بين صورتين | Histogram Matching | Advanced | `skimage.exposure.match_histograms` | W2 |
| 16 | تصحيح كود معطوب لتحليل الفيديو | Debugging + Video | Advanced | `VideoCapture`, حلقة `while`, `np.mean` | W2 |
| 17 | تحليل سطوع الفيديو الحي | Video Processing | Advanced | `VideoCapture`, `cvtColor`, `putText` لحظي | W2 |
| 🚀 | **ماسح مستندات ذكي** | تحدٍ نهائي متكامل | Advanced | جميع المفاهيم أعلاه | W1+W2 |

---

## 4. التمارين التطبيقية (Practical Exercises)

---

# 🟢 Beginner

---

### 💻 Exercise 1: صورة رمادية يدوية والوصول إلى البكسلات

**Topic:** تمثيل الصورة الرمادية كمصفوفة NumPy
**Related Topics:** `dtype=uint8`، الفهرسة ثنائية الأبعاد
**Difficulty:** Beginner

**Objective:**
ممارسة إنشاء صورة Grayscale يدوياً كمصفوفة NumPy، وفهم أن كل بكسل هو قيمة `uint8` بين 0 و255.

**Task:**
اكتب كوداً يقوم بالتالي:
1. أنشئ مصفوفة `grayscale_image` بأبعاد 4×4 من نوع `uint8` تحتوي على قيم عشوائية بين 0 و255.
2. اطبع شكل المصفوفة (`shape`).
3. اطبع قيمة البكسل في المنتصف تقريباً (الموقع `[1, 2]`).
4. غيّر قيمة البكسل في الموقع `[0, 0]` لتصبح 255 (أبيض خالص).

**Input / Resources:** لا يوجد ملف خارجي — تُنشئ المصفوفة داخل الكود باستخدام `np.random.randint`.

**Expected Result:** طباعة الأبعاد، قيمة بكسل واحد، والمصفوفة بعد التعديل مع ظهور 255 في الزاوية العلوية اليسرى.

**Constraints / Notes:**
- استخدم `dtype=np.uint8` صراحة.
- لا تستخدم OpenCV في هذا التمرين.

**Hints:**
- استخدم `np.random.randint(0, 256, (4,4), dtype=np.uint8)`.
- الفهرسة `arr[row, col]` تماماً كما رأينا في تمارين الأسبوع الأول.

<details>
<summary>Solution</summary>

**Approach:** استخدام `np.random.randint` لإنشاء المصفوفة، ثم الفهرسة المباشرة للقراءة والتعديل.

**Implementation:**
```python
import numpy as np

grayscale_image = np.random.randint(0, 256, (4, 4), dtype=np.uint8)
print("Grayscale image:\n", grayscale_image)
print(f"Shape: {grayscale_image.shape}")

center_pixel = grayscale_image[1, 2]
print(f"Pixel at (1,2): {center_pixel}")

grayscale_image[0, 0] = 255
print("After modifying (0,0):\n", grayscale_image)
```

**Explanation:** استخدام `uint8` يضمن أن القيم تبقى ضمن نطاق 0–255 كما هو معتاد في تمثيل الصور. الفهرسة `[row, col]` تصل مباشرة لبكسل واحد كما تعلمنا في قسم "الوصول إلى القيم".

**Expected Result:** طباعة مصفوفة 4×4 من الأعداد، قيمة بكسل واحدة، ثم نفس المصفوفة مع 255 في `[0,0]`.

**Common Mistakes:**
- نسيان تحديد `dtype=np.uint8` فتصبح القيم `int64` بشكل افتراضي.
- الخلط بين الترتيب `[row, col]` و `[x, y]`.
</details>

---

### 💻 Exercise 2: إنشاء صورة RGB وتعديل بكسل

**Topic:** تمثيل صورة RGB كمصفوفة 3D
**Related Topics:** `np.zeros`, فهرسة القنوات `[:, :, channel]`
**Difficulty:** Beginner

**Objective:** فهم أن صورة RGB هي مصفوفة `(H, W, 3)` وأن كل قناة قابلة للوصول بشكل مستقل.

**Task:**
اكتب كوداً يقوم بالتالي:
1. أنشئ صورة RGB بأبعاد 5×5 كلها سوداء باستخدام `np.zeros`.
2. اجعل جميع بكسلات الصورة زرقاء خالصة `(0, 0, 255)`.
3. غيّر البكسل في الموقع `[2, 2]` إلى اللون الأبيض `(255, 255, 255)`.
4. اطبع القناة الحمراء فقط من الصورة النهائية.

**Input / Resources:** لا يوجد ملف — إنشاء المصفوفة داخلياً.

**Expected Result:** طباعة شكل الصورة، البكسل المركزي بعد التعديل، ثم القناة الحمراء (يجب أن تكون كلها أصفار عدا مركز الصورة الذي يساوي 255).

**Constraints / Notes:**
- استخدم `dtype=np.uint8`.
- لا تستخدم OpenCV.

**Hints:**
- لضبط قناة كاملة: `img[:, :, 2] = 255` (تذكّر ترتيب القنوات R,G,B هنا).
- لتغيير بكسل واحد: `img[row, col] = [255, 255, 255]`.

<details>
<summary>Solution</summary>

**Approach:** بناء المصفوفة بالأصفار ثم استخدام Broadcasting لتلوين قناة كاملة، وفهرسة نقطة واحدة للتعديل.

**Implementation:**
```python
import numpy as np

blue_img = np.zeros((5, 5, 3), dtype=np.uint8)
blue_img[:, :, 2] = 255  # القناة الزرقاء = 255 (ترتيب R,G,B)

print(f"Shape: {blue_img.shape}")

blue_img[2, 2] = [255, 255, 255]
print(f"Center pixel after edit: {blue_img[2, 2]}")

red_channel = blue_img[:, :, 0]
print("Red channel:\n", red_channel)
```

**Explanation:** `img[:, :, 2] = 255` يستخدم Broadcasting لتعيين قيمة واحدة لكل عناصر القناة الثالثة دفعة واحدة، بدلاً من حلقة. تعديل بكسل واحد يتم بتمرير قائمة من 3 قيم.

**Expected Result:** شكل `(5, 5, 3)`، البكسل المركزي `[255 255 255]`، والقناة الحمراء كلها أصفار عدا الموقع `[2,2]` الذي يساوي 255.

**Common Mistakes:**
- الخلط بين ترتيب القنوات RGB و BGR (سنراه لاحقاً في OpenCV).
- استخدام قيمة واحدة بدل قائمة من 3 عناصر عند تعديل بكسل كامل.
</details>

---

### 💻 Exercise 3: تحميل صورة وتصحيح الألوان

**Topic:** Color Spaces + تحميل الصور
**Related Topics:** `cv2.imread`, `cv2.cvtColor`
**Difficulty:** Beginner

**Objective:** ممارسة قراءة صورة بـ OpenCV، وفهم لماذا تظهر الألوان مقلوبة عند العرض بـ Matplotlib، وكيفية تصحيحها.

**Scenario:** لديك صورة باسم `test.jpg` في المجلد الحالي.

**Task:**
اكتب كوداً يقوم بالتالي:
1. قراءة الصورة `test.jpg` وتخزينها في متغير.
2. عرضها مباشرة بـ `plt.imshow` (ستظهر الألوان بشكل خاطئ).
3. تحويلها من `BGR` إلى `RGB` باستخدام `cv2.cvtColor`.
4. عرض الصورتين (قبل وبعد التصحيح) جنباً إلى جنب.

**Input / Resources:** صورة `test.jpg`.

**Expected Result:** لوحتان: الأولى بألوان مقلوبة (البرتقالي بدل الأزرق مثلاً)، والثانية بألوان صحيحة.

**Constraints / Notes:**
- OpenCV تقرأ الصور دائماً بترتيب BGR افتراضياً.
- استخدم `cv2.COLOR_BGR2RGB`.

**Hints:**
- `cv2.imread('test.jpg')` تُرجع مصفوفة NumPy بترتيب BGR.
- استخدم `plt.subplot(1, 2, ...)` لعرض الصورتين معاً.

<details>
<summary>Solution</summary>

**Approach:** القراءة المباشرة بـ `cv2.imread`، ثم التحويل بـ `cv2.cvtColor` تماماً كما في مثال صورة السماء بالدفتر.

**Implementation:**
```python
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('test.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1); plt.imshow(img); plt.title('Wrong Colors (BGR)')
plt.subplot(1, 2, 2); plt.imshow(img_rgb); plt.title('Correct Colors (RGB)')
plt.show()
```

**Explanation:** `cv2.imread` يعيد المصفوفة بترتيب القنوات B,G,R، بينما `plt.imshow` يتوقع R,G,B، لذلك تظهر الألوان بشكل خاطئ قبل التحويل.

**Expected Result:** الصورة الأولى بألوان معكوسة (أزرق↔أحمر)، والثانية بالألوان الطبيعية.

**Common Mistakes:**
- نسيان أن OpenCV تستخدم BGR وليس RGB.
- استخدام `cv2.COLOR_RGB2BGR` بالخطأ بدل `BGR2RGB`.
</details>

---

### 💻 Exercise 4: فصل القنوات وعرض قناة واحدة

**Topic:** Color Channel Splitting
**Related Topics:** `cv2.split`, Grayscale
**Difficulty:** Beginner

**Objective:** فصل الصورة الملونة إلى قنواتها الثلاث وفهم أن كل قناة هي صورة رمادية مستقلة.

**Scenario:** لديك صورة ملونة باسم `test.jpg`.

**Task:**
اكتب كوداً يقوم بالتالي:
1. قراءة الصورة وتخزينها في متغير.
2. تحويل الصورة من `BGR` إلى التدرج الرمادي `Grayscale`.
3. فصل قنوات الصورة الملونة إلى `(B, G, R)` باستخدام `cv2.split`، ثم اعرض **القناة الخضراء (G)** فقط.

**Input / Resources:** صورة `test.jpg`.

**Expected Result:** صورتان معروضتان: النسخة الرمادية الكاملة، والقناة الخضراء المعروضة بـ `cmap='gray'` أو `cmap='Greens'`.

**Constraints / Notes:**
- تذكّر أن ترتيب الإخراج من `cv2.split` هو `B, G, R` وليس `R, G, B`.

**Hints:**
- `B, G, R = cv2.split(img)`.
- كل قناة مُخرجة هي مصفوفة 2D يمكن عرضها بـ `plt.imshow(channel, cmap='gray')`.

<details>
<summary>Solution</summary>

**Approach:** تحويل رمادي أولاً، ثم فصل القنوات من الصورة الأصلية الملونة وعرض قناة G فقط.

**Implementation:**
```python
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

B, G, R = cv2.split(img)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1); plt.imshow(gray, cmap='gray'); plt.title('Grayscale'); plt.axis('off')
plt.subplot(1, 2, 2); plt.imshow(G, cmap='Greens'); plt.title('Green Channel'); plt.axis('off')
plt.show()
```

**Explanation:** `cv2.split` يفكك المصفوفة الملونة إلى ثلاث مصفوفات 2D منفصلة، تماماً كما في مثال فصل قنوات صورة السماء بالدفتر.

**Expected Result:** صورة رمادية عادية، وصورة أخرى تُظهر شدة اللون الأخضر فقط في كل بكسل.

**Common Mistakes:**
- الاعتقاد أن ترتيب الإخراج R, G, B (وهو في الحقيقة B, G, R).
- استخدام `cmap` افتراضي (ملون) بدلاً من `gray` عند عرض قناة واحدة.
</details>

---

### 💻 Exercise 5: تغيير الحجم لأبعاد ثابتة

**Topic:** Resizing
**Related Topics:** `cv2.resize`
**Difficulty:** Beginner

**Objective:** ممارسة تغيير أبعاد الصورة لتوحيد المقاسات، كخطوة تحضيرية شائعة قبل إدخال الصور لنموذج ذكاء اصطناعي.

**Task:**
اكتب كوداً يقوم بالتالي:
1. قراءة صورة `test.jpg` وتحويلها إلى RGB.
2. تصغيرها إلى 200×150 بكسل.
3. تكبيرها إلى 800×600 بكسل.
4. عرض الصورة الأصلية والنسختين (المصغّرة والمكبّرة) في صف واحد مع عناوين تحتوي على الأبعاد الجديدة.

**Input / Resources:** صورة `test.jpg`.

**Expected Result:** 3 صور معروضة جنباً إلى جنب بأبعاد مختلفة، وطباعة الأبعاد الجديدة في العنوان.

**Constraints / Notes:**
- `cv2.resize` يأخذ الأبعاد بترتيب `(width, height)` وليس `(height, width)`.

**Hints:**
- استخدم `cv2.resize(img_rgb, (200, 150))`.
- تحقق من `.shape` بعد التغيير للتأكد من الترتيب.

<details>
<summary>Solution</summary>

**Approach:** نفس المثال الثابت للتصغير والتكبير من الدفتر.

**Implementation:**
```python
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('test.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

resized_small = cv2.resize(img_rgb, (200, 150))
resized_large = cv2.resize(img_rgb, (800, 600))

plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1); plt.imshow(img_rgb); plt.title(f'Original {img_rgb.shape[1]}x{img_rgb.shape[0]}')
plt.subplot(1, 3, 2); plt.imshow(resized_small); plt.title('Resized 200x150')
plt.subplot(1, 3, 3); plt.imshow(resized_large); plt.title('Resized 800x600')
plt.show()
```

**Explanation:** `cv2.resize` يأخذ tuple `(width, height)` — عكس ترتيب `.shape` الذي يعطي `(height, width, channels)`.

**Expected Result:** 3 لوحات بأحجام مرئية مختلفة بوضوح.

**Common Mistakes:**
- تبديل width وheight عن طريق الخطأ.
- نسيان تحويل الصورة إلى RGB قبل العرض بـ Matplotlib.
</details>

---

# 🟡 Intermediate

---

### 💻 Exercise 6: خط أنابيب تحويلات هندسية (Resize → Rotate → Crop)

**Topic:** Image Transformations (متعددة الخطوات)
**Related Topics:** `cv2.resize`, `cv2.getRotationMatrix2D`, `cv2.warpAffine`, Slicing
**Difficulty:** Intermediate

**Objective:** دمج عدة عمليات هندسية متتابعة في خط أنابيب واحد، تماماً كما يُطلب عند تجهيز صورة لنموذج ذكاء اصطناعي.

**Scenario:** لديك صورة بأبعاد كبيرة جداً وتريد تجهيزها لإدخالها في نموذج ذكاء اصطناعي.

**Task:**
اكتب كوداً يقوم بالتالي:
1. تغيير أبعاد الصورة (Resize) لتصبح 300×300 بكسل.
2. تدوير الصورة بزاوية 90 درجة باتجاه عقارب الساعة.
3. قص (Crop) منتصف الصورة تماماً ليصبح بأبعاد 100×100.

**Input / Resources:** صورة `test.jpg`.

**Expected Result:** صورة نهائية بأبعاد 100×100 تُظهر مركز الصورة بعد الدوران، وعرض جميع المراحل الوسيطة.

**Constraints / Notes:**
- الزاوية الموجبة في `cv2.getRotationMatrix2D` تعني عكس عقارب الساعة، لذا للدوران باتجاه عقارب الساعة استخدم زاوية سالبة (-90).
- لحساب مركز الصورة للقص استخدم `shape[1]//2` و `shape[0]//2`.

**Hints:**
- `M = cv2.getRotationMatrix2D(center, -90, 1.0)` ثم `cv2.warpAffine(img, M, (w, h))`.
- بعد الدوران بزاوية 300×300، القص للمنتصف بأبعاد 100×100 يعني أخذ الشريحة `[100:200, 100:200]`.

<details>
<summary>Solution</summary>

**Approach:** تطبيق العمليات الثلاث بالترتيب المطلوب تماماً كما يُدرَّس في قسم التحويلات الهندسية.

**Implementation:**
```python
import cv2

img = cv2.imread('test.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 1. Resize إلى 300x300
resized = cv2.resize(img_rgb, (300, 300))

# 2. تدوير 90 درجة باتجاه عقارب الساعة (زاوية سالبة)
(h, w) = resized.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, -90, 1.0)
rotated = cv2.warpAffine(resized, M, (w, h))

# 3. قص المنتصف 100x100
start = (300 - 100) // 2  # = 100
cropped = rotated[start:start+100, start:start+100]

print(f"Final shape: {cropped.shape}")
```

**Explanation:** الترتيب مهم — القص يتم بعد الدوران وليس قبله، لأن السؤال يطلب قص "منتصف الصورة" بعد أن أصبحت مُدوَّرة ومُغيَّرة الحجم.

**Expected Result:** مصفوفة نهائية بشكل `(100, 100, 3)`.

**Common Mistakes:**
- استخدام زاوية +90 بدلاً من -90 فيصبح الدوران عكس عقارب الساعة.
- حساب نقطة بداية القص بشكل خاطئ فتُنتج صورة غير مُمركزة.
</details>

---

### 💻 Exercise 7: تحويل RGB→Grayscale يدوياً مقابل OpenCV

**Topic:** تحويل الألوان (مقارنة)
**Related Topics:** صيغة `0.299R+0.587G+0.114B`, `cv2.cvtColor`
**Difficulty:** Intermediate

**Objective:** التحقق من أن الصيغة اليدوية لتحويل RGB إلى Grayscale (من الأسبوع الأول) تُعطي نفس نتيجة `cv2.cvtColor` تقريباً (الأسبوع الثاني).

**Task:**
اكتب كوداً يقوم بالتالي:
1. اقرأ صورة `test.jpg` وحوّلها إلى RGB.
2. طبّق صيغة التحويل اليدوي: `Gray = 0.299*R + 0.587*G + 0.114*B` باستخدام NumPy فقط (بدون OpenCV) واحصل على `dtype=uint8`.
3. احسب النسخة الرمادية بواسطة `cv2.cvtColor(..., cv2.COLOR_RGB2GRAY)`.
4. قارن بين الصورتين بطباعة الفرق المطلق الأقصى بين المصفوفتين.

**Input / Resources:** صورة `test.jpg`.

**Expected Result:** صورتان رماديتان متشابهتان بصرياً، وفرق أقصى صغير جداً (عادة 0 أو 1 بسبب التقريب).

**Constraints / Notes:**
- استخرج القنوات R, G, B بالفهرسة `img_rgb[:,:,0]` إلخ، لا تستخدم `cv2.split` على الصورة بترتيب RGB (فهو مخصص لـ BGR أصلاً لكنه يعمل تقنياً بنفس الطريقة على أي 3 قنوات).
- تذكّر تحويل النتيجة إلى `uint8` باستخدام `.astype(np.uint8)`.

**Hints:**
- فصل القنوات: `R = img_rgb[:,:,0].astype(np.float64)` وهكذا للبقية لتفادي overflow أثناء الضرب.
- استخدم `np.max(np.abs(manual_gray.astype(int) - cv2_gray.astype(int)))` للمقارنة.

<details>
<summary>Solution</summary>

**Approach:** تطبيق الصيغة اليدوية بنفس أسلوب تحدي الأسبوع الأول، ثم مقارنتها بدالة OpenCV الجاهزة من الأسبوع الثاني.

**Implementation:**
```python
import cv2
import numpy as np

img = cv2.imread('test.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

R = img_rgb[:, :, 0].astype(np.float64)
G = img_rgb[:, :, 1].astype(np.float64)
B = img_rgb[:, :, 2].astype(np.float64)

manual_gray = (0.299 * R + 0.587 * G + 0.114 * B).astype(np.uint8)

cv2_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

max_diff = np.max(np.abs(manual_gray.astype(int) - cv2_gray.astype(int)))
print(f"Max difference between manual and OpenCV grayscale: {max_diff}")
```

**Explanation:** التحويل الداخلي في OpenCV يستخدم نفس المعاملات تقريباً (مع تقريب مختلف قليلاً)، لذلك الفرق الأقصى المتوقع صغير جداً (0 أو 1) وليس صفراً بالضرورة بسبب التقريب الداخلي في OpenCV.

**Expected Result:** طباعة رقم صغير جداً يثبت تطابق الطريقتين تقريباً.

**Common Mistakes:**
- عدم تحويل القنوات إلى `float` قبل الضرب، مما يسبب overflow في `uint8`.
- مقارنة القيم بدون تحويلها إلى `int` قبل الطرح (يسبب أخطاء عند القيم القريبة من الصفر في uint8).
</details>

---

### 💻 Exercise 8: ضبط السطوع مع Clipping على صورة حقيقية

**Topic:** Pixel Manipulation (Brightness Adjustment)
**Related Topics:** `.astype(np.int16)`, `np.clip`, صورة حقيقية عبر OpenCV
**Difficulty:** Intermediate

**Objective:** تطبيق تقنية زيادة السطوع مع تفادي الـ overflow (من الأسبوع الأول) على صورة حقيقية مُحمَّلة بـ OpenCV بدلاً من مصفوفة تجريبية صغيرة.

**Task:**
اكتب كوداً يقوم بالتالي:
1. اقرأ صورة `test.jpg` وحوّلها إلى Grayscale.
2. زد سطوع الصورة بإضافة 40 لكل بكسل، مع التحويل إلى `int16` أولاً لتفادي الـ overflow، ثم استخدم `np.clip` لإعادة القيم إلى النطاق [0, 255]، ثم أعد التحويل إلى `uint8`.
3. اطبع القيمة القصوى والدنيا في الصورة الأصلية والصورة المعدَّلة.
4. اعرض الصورتين جنباً إلى جنب.

**Input / Resources:** صورة `test.jpg`.

**Expected Result:** صورة أكثر سطوعاً بشكل واضح، مع تأكيد أن أعلى قيمة لا تتجاوز 255.

**Constraints / Notes:**
- يجب استخدام `astype(np.int16)` قبل الجمع لتفادي التفاف القيم (wrap-around) في `uint8`.

**Hints:**
- الخطوات: `astype(int16) → +40 → np.clip(0,255) → astype(uint8)` بالضبط كما في مثال الأسبوع الأول.

<details>
<summary>Solution</summary>

**Approach:** نفس تقنية الأسبوع الأول لضبط السطوع، لكن على صورة حقيقية بدل مصفوفة 2×2 تجريبية.

**Implementation:**
```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

brighter = gray.astype(np.int16) + 40
brighter = np.clip(brighter, 0, 255).astype(np.uint8)

print(f"Original range: [{gray.min()}, {gray.max()}]")
print(f"Brighter range: [{brighter.min()}, {brighter.max()}]")

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1); plt.imshow(gray, cmap='gray'); plt.title('Original'); plt.axis('off')
plt.subplot(1, 2, 2); plt.imshow(brighter, cmap='gray'); plt.title('Brighter (+40)'); plt.axis('off')
plt.show()
```

**Explanation:** التحويل إلى `int16` يسمح للقيم بتجاوز 255 مؤقتاً أثناء الجمع دون أن "تلتف" حول الصفر كما يحدث في `uint8`؛ ثم `np.clip` يقصّها إلى الحد الأقصى 255 قبل إعادتها إلى `uint8`.

**Expected Result:** صورة أفتح وضوحاً، وأعلى قيمة في الصورة الجديدة تساوي 255 وليس رقماً ملتفّاً من حول الصفر.

**Common Mistakes:**
- إضافة 40 مباشرة على مصفوفة `uint8` بدون تحويل النوع أولاً، مما يسبب التفاف القيم (مثلاً 250+40 يصبح رقماً صغيراً بدل 255).
- نسيان إعادة التحويل النهائي إلى `uint8` قبل العرض.
</details>

---

### 💻 Exercise 9: الرسم والتعليق على نسخة من الصورة

**Topic:** Drawing & Annotation
**Related Topics:** `cv2.line`, `cv2.rectangle`, `cv2.putText`, `.copy()`
**Difficulty:** Intermediate

**Objective:** ممارسة رسم أشكال هندسية ونصوص فوق صورة دون إتلاف الصورة الأصلية.

**Scenario:** تريد تحديد منطقة في صورة وتوضيحها بعنوان نصي (مثلاً لتوضيح نتيجة لعرض تقديمي).

**Task:**
اكتب كوداً يقوم بالتالي:
1. اقرأ صورة `test.jpg` وحوّلها إلى RGB.
2. خذ نسخة (`.copy()`) من الصورة قبل الرسم عليها.
3. ارسم مستطيلاً أخضر اللون حول منطقة اخترتها من الصورة.
4. اكتب فوق المستطيل نصاً "Region of Interest" باستخدام `cv2.putText`.
5. اعرض الصورة الأصلية بجانب الصورة المُعلَّق عليها للتأكد أن الأصلية لم تتأثر.

**Input / Resources:** صورة `test.jpg`.

**Expected Result:** صورتان: الأصلية بدون أي رسم، والنسخة تحتوي على مستطيل ونص فوقها.

**Constraints / Notes:**
- دوال الرسم في OpenCV تُعدّل الصورة In-place، لذلك **يجب** أخذ نسخة أولاً.
- الألوان في `cv2.rectangle`/`cv2.putText` تكون بترتيب قنوات الصورة الممرَّرة (RGB هنا لأننا حوّلنا الصورة مسبقاً).

**Hints:**
- `cv2.rectangle(draw_img, pt1, pt2, color, thickness)`.
- `cv2.putText(draw_img, text, org, font, fontScale, color, thickness)`.

<details>
<summary>Solution</summary>

**Approach:** أخذ نسخة من الصورة، ثم الرسم عليها بدالتي `rectangle` و`putText` تماماً كما شُرح في قسم الرسم والتعليق.

**Implementation:**
```python
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('test.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

draw_img = img_rgb.copy()

cv2.rectangle(draw_img, (50, 50), (250, 200), (0, 255, 0), 3)
cv2.putText(draw_img, "Region of Interest", (50, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1); plt.imshow(img_rgb); plt.title('Original (untouched)'); plt.axis('off')
plt.subplot(1, 2, 2); plt.imshow(draw_img); plt.title('Annotated Copy'); plt.axis('off')
plt.show()
```

**Explanation:** استخدام `.copy()` يضمن أن `img_rgb` الأصلية تبقى نظيفة، لأن دوال الرسم في OpenCV تعدّل المصفوفة الممرَّرة مباشرة.

**Expected Result:** الصورة الأصلية بدون أي أثر رسم، والنسخة الثانية تُظهر مستطيلاً أخضر مع تسمية نصية فوقه.

**Common Mistakes:**
- الرسم مباشرة على `img_rgb` دون نسخ، مما يُتلف الصورة الأصلية لبقية الكود.
- وضع نص `cv2.putText` خارج حدود الصورة فلا يظهر.
</details>

---

### 💻 Exercise 10: حساب ورسم الهيستوغرام لصورتين

**Topic:** Histogram
**Related Topics:** `cv2.calcHist`, `plt.plot`
**Difficulty:** Intermediate

**Objective:** فهم كيف يختلف شكل الهيستوغرام باختلاف ظروف الإضاءة، عبر مقارنة صورتين (نهار وليل مثلاً).

**Task:**
اكتب كوداً يقوم بالتالي:
1. حمّل صورتين: `day_time.jpg` و `night_time.jpg`.
2. حوّل كل واحدة إلى Grayscale.
3. احسب الهيستوغرام لكل صورة باستخدام `cv2.calcHist`.
4. اعرض كل صورة بجانب الهيستوغرام الخاص بها في شبكة 2×2.

**Input / Resources:** صورتان `day_time.jpg`, `night_time.jpg`.

**Expected Result:** هيستوغرام صورة النهار يميل نحو القيم الأعلى (أكثر إضاءة)، بينما هيستوغرام صورة الليل يتركز في القيم المنخفضة (أغمق).

**Constraints / Notes:**
- `cv2.calcHist([gray], [0], None, [256], [0, 256])` هو الاستدعاء القياسي لصورة رمادية واحدة.

**Hints:**
- استخدم دالة مساعدة واحدة تُطبَّق على كل صورة لتفادي تكرار الكود (نفس فكرة `plot_hist_side_by_side` في الدفتر).

<details>
<summary>Solution</summary>

**Approach:** بناء دالة عامة تحسب الهيستوغرام وتعرضه بجانب الصورة، ثم استدعاؤها مرتين.

**Implementation:**
```python
import cv2
import matplotlib.pyplot as plt

def show_image_and_histogram(filename, title, ax_img, ax_hist):
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

    ax_img.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax_img.set_title(title)
    ax_img.axis('off')

    ax_hist.plot(hist, color='black')
    ax_hist.fill_between(range(256), hist.flatten(), color='gray', alpha=0.3)
    ax_hist.set_title(f'Histogram — {title}')

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
show_image_and_histogram('day_time.jpg', 'Day', axes[0, 0], axes[0, 1])
show_image_and_histogram('night_time.jpg', 'Night', axes[1, 0], axes[1, 1])
plt.tight_layout()
plt.show()
```

**Explanation:** `cv2.calcHist` يُنتج توزيعاً لعدد البكسلات لكل قيمة إضاءة من 0 إلى 255؛ صور الليل تُظهر تركيزاً في القيم المنخفضة، بينما صور النهار تمتد نحو القيم المرتفعة.

**Expected Result:** فرق واضح في موقع الذروة بين الهيستوغرامين.

**Common Mistakes:**
- نسيان `.flatten()` عند استخدام `fill_between` مع نتيجة `calcHist` (تكون بشكل `(256,1)`).
- عدم تحويل الصورة لرمادي قبل حساب الهيستوغرام (calcHist يحتاج قناة واحدة هنا).
</details>

---

### 💻 Exercise 11: عتبة ثنائية يدوية على مستند ممسوح

**Topic:** Thresholding (يدوي)
**Related Topics:** `cv2.threshold(cv2.THRESH_BINARY)`
**Difficulty:** Intermediate

**Objective:** استخدام عتبة ثابتة لتحويل مستند ممسوح ضوئياً إلى أبيض وأسود نقي، للتخلص من الظلال وخلفية الورقة.

**Scenario:** لديك صورة لورقة ممسوحة ضوئياً (Scanned Document).

**Task:**
اكتب كوداً يقوم بالتالي:
1. حوّل الصورة إلى التدرج الرمادي.
2. طبّق عليها عتبة ثنائية `cv2.threshold` بحيث: أي بكسل قيمته الإضاءتية أعلى من 130 يتحول إلى أبيض (255)، وما دونه يتحول إلى أسود (0).
3. اعرض الصورة الرمادية بجانب النتيجة الثنائية.

**Input / Resources:** صورة `scanned_document.jpg`.

**Expected Result:** صورة أبيض وأسود نقية يسهل فيها تمييز النص عن خلفية الورقة.

**Constraints / Notes:**
- استخدم `cv2.THRESH_BINARY` تحديداً (وليس `THRESH_BINARY_INV`).

**Hints:**
- `_, binary = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)`.

<details>
<summary>Solution</summary>

**Approach:** تطبيق عتبة ثابتة مباشرة كما في مثال الكتاب (`Book2.jpeg`) بالدفتر.

**Implementation:**
```python
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('scanned_document.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, binary = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1); plt.imshow(gray, cmap='gray'); plt.title('Grayscale'); plt.axis('off')
plt.subplot(1, 2, 2); plt.imshow(binary, cmap='gray'); plt.title('Binary (threshold=130)'); plt.axis('off')
plt.show()
```

**Explanation:** كل بكسل أعلى من 130 يصبح 255 (أبيض)، وكل ما دونه يصبح 0 (أسود)، مما يفصل الحبر الغامق عن خلفية الورقة الفاتحة.

**Expected Result:** نص واضح بالأسود على خلفية بيضاء نقية.

**Common Mistakes:**
- استخدام `THRESH_BINARY_INV` عن طريق الخطأ فتنعكس الألوان (نص أبيض على خلفية سوداء).
- اختيار عتبة غير مناسبة للإضاءة الفعلية للصورة فتضيع تفاصيل النص.
</details>

---

### 💻 Exercise 12: تطبيع (Normalize) مصفوفة قبل التحليل

**Topic:** Normalization
**Related Topics:** `(arr - min) / (max - min)`, boolean masking
**Difficulty:** Intermediate

**Objective:** ممارسة تطبيع قيم مصفوفة صورة إلى المجال [0, 1]، وهي خطوة تحضيرية شائعة قبل أي تحليل إحصائي أو تمرير للصورة لنموذج تعلّم آلي.

**Task:**
اكتب كوداً يقوم بالتالي:
1. اقرأ صورة `test.jpg` وحوّلها إلى Grayscale.
2. طبّع قيم الصورة لتصبح بين 0 و1 باستخدام الصيغة `(arr - min) / (max - min)`.
3. باستخدام Boolean Masking على الصورة المطبَّعة، اطبع نسبة البكسلات التي قيمتها أعلى من 0.5 (أي أكثر سطوعاً من المتوسط النسبي).

**Input / Resources:** صورة `test.jpg`.

**Expected Result:** مصفوفة قيمها بين 0.0 و1.0، ونسبة مئوية توضح مقدار السطوع النسبي في الصورة.

**Constraints / Notes:**
- تجنّب القسمة على صفر إن كانت الصورة موحّدة اللون تماماً (max == min)، لكن لا حاجة لمعالجة هذه الحالة الحدّية هنا إلا إذا رغبت.

**Hints:**
- حوّل الصورة إلى `float` قبل التطبيع لتفادي القسمة الصحيحة.
- استخدم `mask = normalized > 0.5` ثم `mask.sum() / mask.size`.

<details>
<summary>Solution</summary>

**Approach:** تطبيق نفس صيغة التطبيع من تمارين الأسبوع الأول، ثم استخدام Boolean Masking من نفس الأسبوع لتحليل النتيجة.

**Implementation:**
```python
import cv2
import numpy as np

img = cv2.imread('test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float64)

min_val, max_val = gray.min(), gray.max()
normalized = (gray - min_val) / (max_val - min_val)

mask = normalized > 0.5
bright_ratio = mask.sum() / mask.size * 100
print(f"Percentage of pixels brighter than relative midpoint: {bright_ratio:.2f}%")
```

**Explanation:** التطبيع يعيد توزيع قيم الصورة الأصلية (0-255) إلى نطاق موحّد [0,1]، مما يسهّل مقارنة صور مختلفة الإضاءة. الـ Boolean Mask يُنتج مصفوفة من True/False يمكن استخدامها مباشرة للعد أو التصفية.

**Expected Result:** رقم نسبة مئوية يعكس مدى سطوع الصورة نسبياً.

**Common Mistakes:**
- نسيان تحويل الصورة إلى `float` قبل الطرح والقسمة، مما يسبب أخطاء تقريب مع `uint8`.
- الخلط بين `mask.sum()` (عدد True) و `mask.size` (عدد كل العناصر).
</details>

---

# 🔴 Advanced

---

### 💻 Exercise 13: مقارنة العتبة اليدوية وOtsu والعتبة التكيّفية

**Topic:** Advanced Thresholding
**Related Topics:** `cv2.THRESH_BINARY`, `cv2.THRESH_OTSU`, `cv2.adaptiveThreshold`
**Difficulty:** Advanced

**Scenario:** أنت تعمل على تحضير صورة مستند (`Book2.jpeg`) لمرحلة OCR، والإضاءة على الصفحة غير متساوية تماماً (أغمق قليلاً من جهة).

**Objective:** مقارنة ثلاث طرق مختلفة لاختيار العتبة، وفهم متى تُستخدم كل طريقة.

**Task:**
اكتب كوداً يقوم بالتالي:
1. اقرأ الصورة وحوّلها إلى Grayscale.
2. طبّق عتبة يدوية ثابتة بقيمة 127.
3. طبّق عتبة Otsu التلقائية (`cv2.THRESH_BINARY + cv2.THRESH_OTSU`)، واطبع القيمة التي اختارها Otsu تلقائياً.
4. طبّق العتبة التكيّفية الغاوسية `cv2.ADAPTIVE_THRESH_GAUSSIAN_C` بحجم جوار 11 وثابت 2.
5. اعرض النتائج الثلاث جنباً إلى جنب مع الصورة الأصلية.

**Input / Resources:** صورة `Book2.jpeg`.

**Expected Result:** لوحة من 4 صور: الرمادية، اليدوية، Otsu، والتكيّفية — مع ملاحظة أن التكيّفية تتعامل بشكل أفضل مع تفاوت الإضاءة داخل نفس الصورة.

**Constraints / Notes:**
- عند استخدام Otsu، مرّر 0 كقيمة عتبة ابتدائية.
- العتبة التكيّفية تحتاج `blockSize` فردياً (مثل 11) و`C` كثابت طرح.

**Hints:**
- الاستدعاء: `cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)` يُرجع القيمة المُختارة كعنصر أول.
- لاحظ الفرق في المناطق التي بها ظل خفيف بين Otsu والتكيّفية.

<details>
<summary>Solution</summary>

**Approach:** تطبيق الطرق الثلاث بالتتابع تماماً كما شُرحت في قسم "كيف نختار قيمة العتبة المناسبة" بالدفتر.

**Implementation:**
```python
import cv2
import matplotlib.pyplot as plt

gray = cv2.cvtColor(cv2.imread('Book2.jpeg'), cv2.COLOR_BGR2GRAY)

_, manual_thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

otsu_val, otsu_thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print(f"Otsu chose threshold value: {otsu_val}")

adaptive_gauss = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
)

fig, axes = plt.subplots(1, 4, figsize=(20, 5))
titles = ['Grayscale', 'Manual (127)', f'Otsu ({otsu_val:.0f})', 'Adaptive Gaussian']
images = [gray, manual_thresh, otsu_thresh, adaptive_gauss]
for ax, title, im in zip(axes, titles, images):
    ax.imshow(im, cmap='gray'); ax.set_title(title); ax.axis('off')
plt.show()
```

**Explanation:** العتبة اليدوية تفترض إضاءة موحّدة، وOtsu يختار العتبة المثلى تلقائياً بناءً على شكل الهيستوغرام (قمتان)، بينما التكيّفية تحسب عتبة مختلفة لكل منطقة محلية بناءً على جيرانها، فتتعامل بشكل أفضل مع الظل غير المنتظم.

**Expected Result:** ملاحظة أن نتيجة Otsu قريبة من اليدوية إن كانت الإضاءة شبه موحّدة، بينما التكيّفية تُبقي على تفاصيل النص حتى في المناطق المظللة التي فشلت فيها الطريقتان الأخريان.

**Common Mistakes:**
- تمرير قيمة عتبة غير صفرية مع علم `THRESH_OTSU` (يجب أن تكون 0).
- اختيار `blockSize` زوجي في `adaptiveThreshold` (يجب أن يكون فردياً).
</details>

---

### 💻 Exercise 14: خط أنابيب عمليات ثنائية (فحص تصنيع)

**Topic:** Binary Image Operations
**Related Topics:** `cv2.bitwise_not`, `cv2.countNonZero`, Overlay (Boolean Masking)
**Difficulty:** Advanced

**Scenario:** أنت تعمل في خط فحص تصنيع، وتريد قياس نسبة مساحة قطعة معينة (تظهر داكنة على خلفية فاتحة) في صورة، وتوضيح موقعها بصرياً.

**Objective:** دمج التحويل الثنائي مع العمليات الثنائية (الانعكاس، حساب المساحة، والتراكب اللوني) في خط أنابيب واحد.

**Task:**
اكتب كوداً يقوم بالتالي:
1. اقرأ الصورة، حوّلها لرمادي، ثم طبّق عتبة ثنائية بقيمة 127 (الجسم الداكن سيظهر أسود، والخلفية بيضاء).
2. اعكس الصورة الثنائية باستخدام `cv2.bitwise_not` ليصبح الجسم أبيض (المقدّمة) والخلفية سوداء.
3. احسب عدد البكسلات البيضاء (`cv2.countNonZero`) والنسبة المئوية للمساحة التي تشغلها القطعة من إجمالي الصورة.
4. أنشئ نسخة ملوّنة من الصورة الأصلية وظلّل مكان القطعة (البكسلات البيضاء في القناع) باللون الأحمر (Overlay).
5. اعرض: الصورة الأصلية، الصورة الثنائية بعد الانعكاس، ونسخة التراكب، مع طباعة النسبة المئوية للمساحة.

**Input / Resources:** صورة `part.jpg` (قطعة داكنة على خلفية فاتحة).

**Expected Result:** طباعة نسبة مساحة القطعة، وصورة تراكب تُظهر منطقة القطعة مُلوَّنة بالأحمر فوق الصورة الأصلية.

**Constraints / Notes:**
- يجب استخدام `.copy()` قبل تعديل الصورة الملونة للتراكب.
- المقارنة `overlay[binary == 255] = [255, 0, 0]` هي شكل من Boolean Masking تعلمناه في الأسبوع الأول.

**Hints:**
- الترتيب: `threshold` → `bitwise_not` → `countNonZero` → Overlay بالقناع.

<details>
<summary>Solution</summary>

**Approach:** تسلسل تماماً كما في قسم "العمليات على الصور الثنائية" بالدفتر: تحضير الصورة الثنائية، ثم الانعكاس، ثم القياس، ثم التراكب.

**Implementation:**
```python
import cv2
import matplotlib.pyplot as plt

img_bgr = cv2.imread('part.jpg')
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
inverted = cv2.bitwise_not(binary)  # الجسم الداكن أصبح أبيض الآن

white_pixels = cv2.countNonZero(inverted)
total_pixels = inverted.shape[0] * inverted.shape[1]
pct = 100 * white_pixels / total_pixels
print(f"Part area: {white_pixels} px ({pct:.2f}% of image)")

overlay = img_rgb.copy()
overlay[inverted == 255] = [255, 0, 0]

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
axes[0].imshow(img_rgb); axes[0].set_title('Original'); axes[0].axis('off')
axes[1].imshow(inverted, cmap='gray'); axes[1].set_title('Binary (inverted)'); axes[1].axis('off')
axes[2].imshow(overlay); axes[2].set_title(f'Overlay — {pct:.1f}% area'); axes[2].axis('off')
plt.show()
```

**Explanation:** بعد العتبة، القطعة الداكنة تصبح سوداء (0) والخلفية بيضاء (255) — عكس ما نريد، لذلك نستخدم `bitwise_not` لجعل القطعة نفسها هي البكسلات البيضاء (المقدّمة)، مما يسمح لـ `countNonZero` بقياس مساحتها مباشرة، وللقناع `inverted == 255` بتحديد موقعها للتراكب.

**Expected Result:** نسبة مساحة دقيقة، وصورة تراكب واضحة تُظهر بالضبط أين تقع القطعة.

**Common Mistakes:**
- نسيان الانعكاس (`bitwise_not`) فتُحسب مساحة الخلفية بدلاً من القطعة.
- تعديل `img_rgb` مباشرة بدل نسخة منها، مما يُفسد أي استخدام لاحق للصورة الأصلية.
</details>

---

### 💻 Exercise 15: مطابقة الهيستوغرام بين صورتين

**Topic:** Histogram Matching
**Related Topics:** `skimage.exposure.match_histograms`
**Difficulty:** Advanced

**Scenario:** لديك صورتان لنفس المشهد (مثلاً مدينة حلب) مُلتقطتان في ظروف إضاءة مختلفة، وتريد توحيد مظهرهما لتسهيل أي معالجة آلية لاحقة (كما في توحيد صور الأقمار الصناعية أو الصور الطبية).

**Objective:** استخدام مطابقة الهيستوغرام لجعل صورة Source تأخذ نفس التوزيع الإحصائي لصورة Reference.

**Task:**
اكتب كوداً يقوم بالتالي:
1. اقرأ صورة المصدر `aleppo_source.jpg` والصورة المرجعية `aleppo_ref.jpg` وحوّلهما إلى RGB.
2. طبّق `match_histograms` من `skimage.exposure` لمطابقة إضاءة/ألوان صورة المصدر مع المرجعية.
3. اعرض الصور الثلاث (Source، Reference، والنتيجة بعد المطابقة) في صف واحد.
4. احسب الهيستوغرام (بعد تحويل كل صورة إلى رمادي) لصورة Source قبل وبعد المطابقة، وقارنهما بصرياً مع هيستوغرام Reference.

**Input / Resources:** صورتان `aleppo_source.jpg`, `aleppo_ref.jpg`.

**Expected Result:** الصورة الناتجة تحمل نفس "شخصية" الإضاءة والألوان الخاصة بالصورة المرجعية، وهيستوغرامها بعد المطابقة يصبح أقرب بشكل واضح لهيستوغرام المرجعية.

**Constraints / Notes:**
- `match_histograms` تحتاج معامل `channel_axis=-1` (أو `multichannel=True` في إصدارات أقدم من scikit-image) عند العمل على صور ملوّنة.

**Hints:**
- `matched = exposure.match_histograms(src_img, ref_img, channel_axis=-1)`.

<details>
<summary>Solution</summary>

**Approach:** استخدام أداة `skimage` تماماً كما وردت في قسم مطابقة الهيستوغرام بالدفتر، ثم التحقق بصرياً عبر رسم الهيستوغرامات.

**Implementation:**
```python
import cv2
import matplotlib.pyplot as plt
from skimage import exposure

src_img = cv2.cvtColor(cv2.imread('aleppo_source.jpg'), cv2.COLOR_BGR2RGB)
ref_img = cv2.cvtColor(cv2.imread('aleppo_ref.jpg'), cv2.COLOR_BGR2RGB)

matched = exposure.match_histograms(src_img, ref_img, channel_axis=-1)

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
axes[0].imshow(src_img); axes[0].set_title('Source'); axes[0].axis('off')
axes[1].imshow(ref_img); axes[1].set_title('Reference'); axes[1].axis('off')
axes[2].imshow(matched.astype('uint8')); axes[2].set_title('Matched'); axes[2].axis('off')
plt.show()

def gray_hist(img):
    gray = cv2.cvtColor(img.astype('uint8'), cv2.COLOR_RGB2GRAY)
    return cv2.calcHist([gray], [0], None, [256], [0, 256])

plt.figure(figsize=(10, 4))
plt.plot(gray_hist(src_img), label='Source (before)')
plt.plot(gray_hist(matched), label='Source (after matching)')
plt.plot(gray_hist(ref_img), label='Reference', linestyle='--')
plt.legend()
plt.title('Histogram comparison')
plt.show()
```

**Explanation:** `match_histograms` تُعيد توزيع قيم بكسلات صورة المصدر بحيث يقترب هيستوغرامها من هيستوغرام صورة المرجع، دون تغيير المحتوى الهيكلي (الأشكال) في الصورة.

**Expected Result:** منحنى هيستوغرام "Source (after matching)" يقترب بشكل واضح من منحنى "Reference" مقارنة بمنحنى "Source (before)".

**Common Mistakes:**
- نسيان `channel_axis=-1` عند العمل على صور RGB فتفشل الدالة أو تُعطي نتيجة خاطئة.
- عدم تحويل النتيجة إلى `uint8` قبل العرض أو حساب الهيستوغرام (تُعاد كـ float من الدالة).
</details>

---

### 💻 Exercise 16: تصحيح كود معطوب لتحليل الفيديو (Debugging)

**Topic:** Debugging + Video Processing
**Related Topics:** `cv2.VideoCapture`, حلقة `while`, `np.mean`
**Difficulty:** Advanced

**Objective:** إيجاد وتصحيح الأخطاء في كود يحاول تحليل متوسط سطوع الفيديو الحي لكنه لا يعمل بشكل صحيح.

**Task:**
الكود التالي يحتوي على 3 أخطاء تمنعه من العمل بشكل صحيح. اعثر عليها وصحّحها:

```python
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)  # خطأ 1
    brightness = np.mean(gray)

    cv2.putText(gray, str(brightness), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))  # خطأ 2

    cv2.imshow('Video', gray)

    if cv2.waitKey(1) == ord('q'):
        break
    # خطأ 3: لا يوجد تحقق من ret ولا تحرير للموارد بعد الحلقة

cv2.destroyAllWindows()
```

**Input / Resources:** كاميرا افتراضية (index 0).

**Expected Result:** بعد التصحيح، يجب أن يعمل الفيديو بشكل صحيح، ويعرض قيمة السطوع كنص متحرك، ويُغلق بأمان عند الضغط على `q`.

**Constraints / Notes:**
- لاحظ اتجاه التحويل اللوني المستخدم.
- لاحظ عدم التحقق من نجاح القراءة (`ret`) قبل المعالجة.
- لاحظ عدم استدعاء `cap.release()` بعد الحلقة.

**Hints:**
- اتجاه التحويل الصحيح لصورة ملوّنة من الكاميرا هو من BGR إلى Grayscale وليس العكس.
- تحقق من `if not ret: break` مباشرة بعد `cap.read()`.
- يجب استدعاء `cap.release()` قبل أو بعد `cv2.destroyAllWindows()`.

<details>
<summary>Solution</summary>

**Approach:** تحديد الأخطاء الثلاثة وتصحيحها مع الحفاظ على بقية الهيكل كما هو.

**Implementation:**
```python
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:  # تصحيح خطأ 3 (جزء أول): التحقق من نجاح القراءة
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # تصحيح خطأ 1: اتجاه التحويل الصحيح
    brightness = np.mean(gray)

    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)  # لعرض نص ملوّن فوق صورة رمادية
    cv2.putText(gray_bgr, f"{brightness:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  # تصحيح خطأ 2: إضافة سماكة الخط

    cv2.imshow('Video', gray_bgr)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()  # تصحيح خطأ 3 (جزء ثاني): تحرير الكاميرا
cv2.destroyAllWindows()
```

**Explanation:**
1. **خطأ 1:** الكود الأصلي يحوّل من Gray إلى BGR بينما `frame` أصلاً ملوّن BGR من الكاميرا — يجب التحويل من BGR إلى Gray لحساب السطوع بشكل صحيح.
2. **خطأ 2:** `cv2.putText` استُدعيت بدون `thickness`، وأيضاً كانت تُكتب فوق صورة رمادية بقناة واحدة بلون RGB ثلاثي القنوات، مما يسبب خطأ في عدد القنوات — لذلك حوّلنا الصورة الرمادية إلى BGR ثلاثية القنوات قبل الرسم.
3. **خطأ 3:** لم يكن هناك تحقق من `ret` (قد تفشل القراءة فيتوقف الكود بخطأ)، ولا تحرير للكاميرا (`cap.release()`) عند الخروج من الحلقة، مما يترك الكاميرا مشغولة.

**Expected Result:** فيديو حي يعرض قيمة السطوع اللحظية كنص أخضر فوق الصورة الرمادية، ويُغلق بأمان دون تجميد الكاميرا.

**Common Mistakes:**
- الخلط بين اتجاهي `COLOR_BGR2GRAY` و`COLOR_GRAY2BGR`.
- الرسم بلون 3 قنوات على صورة أحادية القناة دون تحويلها أولاً.
</details>

---

### 💻 Exercise 17: تحليل سطوع الفيديو الحي (التطبيق النهائي المصغّر)

**Topic:** Video Processing
**Related Topics:** `cv2.VideoCapture`, `cv2.cvtColor`, `np.mean`, `cv2.putText` لحظي
**Difficulty:** Advanced

**Objective:** دمج معالجة الإطارات، التحويل اللوني، الإحصائيات، والرسم اللحظي في تطبيق فيديو مباشر واحد.

**Task:**
اكتب كوداً يقوم بتشغيل الكاميرا وتحليل مستوى إضاءة المشهد في الوقت الفعلي:
1. التقط بث الكاميرا الافتراضية.
2. داخل حلقة `while`، اقرأ الإطارات وحوّل كل إطار فوراً إلى التدرج الرمادي.
3. احسب متوسط قيمة البكسلات (`np.mean`) للإطار الرمادي لمعرفة مستوى الإضاءة العام.
4. استخدم `cv2.putText` لطباعة قيمة هذا المتوسط كنص متحرك مباشرة فوق الفيديو أثناء عرضه.
5. اعرض الفيديو، وأغلق النافذة والكاميرا بأمان عند الضغط على مفتاح `"q"`.

**Input / Resources:** كاميرا افتراضية (index 0).

**Expected Result:** نافذة فيديو حية تعرض قيمة السطوع المحدَّثة في كل إطار، وتُغلق بأمان عند الضغط على `q`.

**Constraints / Notes:**
- يعمل هذا الكود في بيئة محلية تدعم `cv2.imshow`، وليس بالضرورة داخل Colab.
- تذكّر التحقق من `ret` وتحرير الكاميرا في النهاية.

**Hints:**
- لعرض نص ملوّن، حوّل الإطار الرمادي إلى BGR ثلاثي القنوات أولاً (كما في التمرين السابق) أو ارسم النص مباشرة على الإطار الملوّن الأصلي مع كتابة القيمة المحسوبة من نسخته الرمادية.

<details>
<summary>Solution</summary>

**Approach:** بناء على الهيكل الأساسي لمعالجة الفيديو في الدفتر، مع إضافة حساب الإحصائية والرسم اللحظي.

**Implementation:**
```python
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)

    cv2.putText(frame, f"Brightness: {brightness:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Video - Brightness Analysis', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

**Explanation:** نحسب السطوع من النسخة الرمادية للحصول على قيمة تمثل الإضاءة العامة، لكننا نرسم النص فوق الإطار الملوّن الأصلي `frame` كي يظهر بلون واضح (أخضر) دون الحاجة لتحويل إضافي.

**Expected Result:** فيديو حي مع رقم متحرك يعكس تغيّر الإضاءة لحظة بلحظة (مثلاً عند تغطية الكاميرا باليد تنخفض القيمة).

**Common Mistakes:**
- حساب `np.mean` على الإطار الملوّن مباشرة بدل النسخة الرمادية (يُعطي نتيجة مختلفة لأنه متوسط 3 قنوات).
- استخدام `cv2.waitKey(1) == ord('q')` بدون `& 0xFF` على بعض الأنظمة التي قد تسبب مشاكل في القراءة.
</details>

---

## 5. التحدي النهائي (Final Challenge)

### 🚀 Final Challenge: ماسح مستندات ذكي (Smart Document Scanner & Quality Report)

**Scenario:**
تعمل في شركة تُحوّل الأوراق الممسوحة ضوئياً (فواتير، عقود، صفحات كتب) إلى صيغة رقمية نظيفة جاهزة لمرحلة OCR لاحقة، وتحتاج أداة تقوم تلقائياً بتنظيف كل صورة، تحليلها، وإصدار "تقرير جودة" مرئي عليها.

**Objective:**
اكتب برنامجاً يأخذ صورة مستند ممسوح (`document.jpg`) وينتج نسخة نظيفة ثنائية اللون، مع تقرير مرئي يوضح جودة المسح.

**Requirements:**
1. اقرأ الصورة وحوّلها إلى RGB وإلى Grayscale.
2. طبّق **عتبة Otsu التلقائية** لتحويل الصفحة إلى أبيض وأسود نقي (نص أسود على خلفية بيضاء)، واطبع القيمة التي اختارها Otsu.
3. تحقّق أي الحالتين تُمثّل "النص" (البكسلات الداكنة) عبر حساب `cv2.countNonZero` على كل من النتيجة الأصلية والمعكوسة (`bitwise_not`)، واختر النسخة التي فيها عدد البكسلات البيضاء (المفترضة = نص) هو **الأقل** (لأن النص عادة أقل مساحة من الخلفية) — واعتبرها "قناع النص".
4. احسب النسبة المئوية لمساحة النص من كامل الصفحة باستخدام `countNonZero`.
5. أنشئ صورة "تراكب جودة" (Overlay) فوق النسخة الملوّنة الأصلية، تُظهر مناطق النص المكتشفة مظلّلة باللون الأحمر الشفاف الخفيف (يمكن تحقيق الشفافية عبر `cv2.addWeighted` أو تظليل مباشر كما في تمارين سابقة).
6. ارسم فوق الصورة النهائية (بـ `cv2.putText`) ملخصاً نصياً يحوي: قيمة عتبة Otsu، ونسبة مساحة النص.
7. اعرض في لوحة واحدة: الصورة الأصلية، النسخة الثنائية النظيفة، وصورة تقرير الجودة النهائية مع النص المرسوم عليها.

**Expected Behavior:**
عند تشغيل البرنامج على أي صورة مستند ممسوح، يجب أن يُنتج:
- صورة Otsu ثنائية نظيفة.
- رقم نسبة مئوية منطقي لمساحة النص (عادة نسبة صغيرة من إجمالي الصفحة).
- صورة نهائية "تقرير" تجمع تظليل مناطق النص + نص توضيحي يحمل الأرقام الفعلية المحسوبة (وليس نصاً ثابتاً).

**Optional Extensions:**
- إضافة مقارنة بين نتيجة Otsu ونتيجة العتبة التكيّفية لنفس الصورة (من تمرين 13) وعرض الاثنين جنباً إلى جنب في التقرير.
- تحويل الكود إلى نسخة تعمل على **فيديو حي** (كاميرا مستندات) بدلاً من صورة ثابتة، بحيث يُحدَّث تقرير النسبة المئوية إطاراً بإطار كما في تمرين 17.

---

### Solution — الحل المرجعي الكامل

**Approach:**
دمج: تحميل الصورة (W2) → Grayscale (W1/W2) → Otsu Thresholding (W2) → اختيار قناع النص عبر `countNonZero` (W2) → حساب النسبة المئوية (W1: إحصائيات + W2: عمليات ثنائية) → Overlay بالتظليل (W2: Boolean Masking فوق الصورة) → Drawing & Annotation بالنص النهائي (W2).

**Implementation:**
```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. تحميل الصورة
img_bgr = cv2.imread('document.jpg')
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# 2. عتبة Otsu التلقائية
otsu_val, otsu_binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print(f"Otsu threshold value: {otsu_val:.1f}")

# 3. تحديد أي نسخة تمثل قناع النص (الأقل مساحة بيضاء عادة هو النص)
white_original = cv2.countNonZero(otsu_binary)
inverted_binary = cv2.bitwise_not(otsu_binary)
white_inverted = cv2.countNonZero(inverted_binary)

if white_original < white_inverted:
    text_mask = otsu_binary
else:
    text_mask = inverted_binary

# 4. نسبة مساحة النص
total_pixels = gray.shape[0] * gray.shape[1]
text_pixels = cv2.countNonZero(text_mask)
text_pct = 100 * text_pixels / total_pixels
print(f"Text area: {text_pct:.2f}% of the page")

# 5. تراكب شفاف يُظهر مناطق النص المكتشفة
overlay = img_rgb.copy()
red_layer = img_rgb.copy()
red_layer[text_mask == 255] = [255, 0, 0]
overlay = cv2.addWeighted(red_layer, 0.35, img_rgb, 0.65, 0)

# 6. رسم ملخص نصي فوق صورة التقرير النهائية
report_img = overlay.copy()
summary_line1 = f"Otsu threshold: {otsu_val:.0f}"
summary_line2 = f"Text area: {text_pct:.2f}%"
cv2.putText(report_img, summary_line1, (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 128, 0), 2)
cv2.putText(report_img, summary_line2, (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 128, 0), 2)

# 7. عرض النتائج
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
axes[0].imshow(img_rgb); axes[0].set_title('Original'); axes[0].axis('off')
axes[1].imshow(otsu_binary, cmap='gray'); axes[1].set_title(f'Otsu Binary ({otsu_val:.0f})'); axes[1].axis('off')
axes[2].imshow(report_img); axes[2].set_title('Quality Report'); axes[2].axis('off')
plt.tight_layout()
plt.show()
```

**Explanation:**
- **Otsu** يختار العتبة الفاصلة تلقائياً بناءً على شكل الهيستوغرام، وهو مناسب هنا لأن الصفحة عادة ما يكون لها قمتان واضحتان (خلفية فاتحة + نص داكن).
- الاختيار بين النسخة الأصلية والمعكوسة عبر مقارنة `countNonZero` هو أسلوب عملي وبسيط لتحديد أي مجموعة بكسلات تمثل "المقدّمة" (النص) دون افتراض مسبق لاتجاه الإضاءة.
- استخدام `cv2.addWeighted` يُنتج تظليلاً شفافاً بدل استبدال الألوان بالكامل، فتبقى تفاصيل الصورة الأصلية مرئية تحت التظليل.
- الرسم النهائي بـ `cv2.putText` يحوّل الأرقام المحسوبة برمجياً (وليست نصاً ثابتاً) إلى تقرير مرئي مباشر فوق الصورة، وهو بالضبط أسلوب "الرسم والتعليق" المُتعلَّم في الأسبوع الثاني.

**Expected Result:**
ثلاث لوحات: الصورة الأصلية، نسخة Otsu الثنائية النظيفة، وصورة "التقرير" النهائية التي تُظهر مناطق النص مظلّلة بأحمر خفيف مع سطرين نصيين أعلى الصورة يحملان قيمة عتبة Otsu ونسبة مساحة النص الفعليتين.

**Common Mistakes:**
- افتراض دائم أن نتيجة `THRESH_BINARY` تجعل النص أبيض دوماً — هذا يعتمد على إضاءة الخلفية مقارنة بالنص، لذلك المقارنة بـ `countNonZero` بين النسخة والمعكوسة ضرورية.
- استخدام `overlay[mask] = color` مباشرة بدل `cv2.addWeighted` يُنتج تظليلاً صلباً غير شفاف، مما يُخفي تفاصيل الصورة الأصلية تماماً في تلك المناطق.
- رسم النص بحجم خط كبير جداً فيتجاوز حدود الصورة أو يُغطي مناطق مهمة من المستند.

---

## 6. مصفوفة التغطية (Coverage Matrix)

| الموضوع | المصدر | الصعوبة | التمرين | مغطّى |
|---|---|---|---|---|
| تمثيل Grayscale كمصفوفة 2D | W1 | Beginner | Exercise 1 | ✓ |
| تمثيل RGB كمصفوفة 3D وفهرسة القنوات | W1 | Beginner | Exercise 2 | ✓ |
| تحميل صورة وتصحيح BGR→RGB | W2 | Beginner | Exercise 3 | ✓ |
| فصل القنوات (`cv2.split`) | W2 | Beginner | Exercise 4 | ✓ |
| تغيير الحجم (`cv2.resize`) | W2 | Beginner | Exercise 5 | ✓ |
| التدوير والقص (`warpAffine`, Slicing) | W2 | Intermediate | Exercise 6 | ✓ |
| صيغة RGB→Grayscale اليدوية مقابل `cvtColor` | Both | Intermediate | Exercise 7 | ✓ |
| ضبط السطوع (`astype`, `np.clip`) | Both | Intermediate | Exercise 8 | ✓ |
| الرسم والتعليق (`line/rectangle/putText`) | W2 | Intermediate | Exercise 9 | ✓ |
| الهيستوغرام (`calcHist`) | W2 | Intermediate | Exercise 10 | ✓ |
| العتبة الثنائية اليدوية | W2 | Intermediate | Exercise 11 | ✓ |
| التطبيع وBoolean Masking | W1 | Intermediate | Exercise 12 | ✓ |
| Otsu والعتبة التكيّفية | W2 | Advanced | Exercise 13 | ✓ |
| العمليات الثنائية (`bitwise_not`, `countNonZero`, Overlay) | W2 | Advanced | Exercise 14 | ✓ |
| مطابقة الهيستوغرام (`skimage`) | W2 | Advanced | Exercise 15 | ✓ |
| Debugging لكود معالجة فيديو | W2 | Advanced | Exercise 16 | ✓ |
| معالجة الفيديو الحي (`VideoCapture`) | W2 | Advanced | Exercise 17 | ✓ |
| دمج شامل لكل المفاهيم أعلاه | W1+W2 | Advanced | Final Challenge | ✓ |
| أساسيات بايثون (متغيرات، شروط، حلقات، دوال، بنى بيانات) | W1 | Beginner | مُغطّاة بالكامل ضمن تمارين الدفتر الأصلي نفسه؛ لم تُكرَّر هنا لتفادي الازدواجية | ✓ (في المصدر) |
| NumPy: إنشاء، خصائص، Broadcasting، Reshape، عشوائيات | W1 | Beginner–Intermediate | مُغطّاة ضمن تمارين الدفتر الأصلي، وتُستخدم كأساس تقني في التمارين 1، 2، 7، 8، 12 هنا | ✓ |

> **ملاحظة على التغطية:** المفاهيم الأساسية لبايثون وNumPy الخام (بدون صور) موجودة بكثافة داخل الدفتر الأول نفسه مع حلول جاهزة لكل موضوع على حدة، لذلك ركّزت هذه المجموعة الإضافية من التمارين على **نقطة التقاء** الأسبوعين: استخدام NumPy لتمثيل الصور ثم البناء عليها بأدوات OpenCV الحقيقية، تماماً كما تنص خلاصة الدفتر الأول على أن الخطوة التالية هي "استخدام NumPy فقط لعمليات حقيقية على الصور".
