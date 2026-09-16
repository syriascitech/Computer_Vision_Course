<div dir="rtl">

# المصادر والرخص — الأسبوع 8

## مقاطع الفيديو

كل مقاطع هذا الأسبوع من **[Pexels](https://www.pexels.com/)**، برخصة
[Pexels License](https://www.pexels.com/license/): استخدام حر بلا حاجة
لنسب المصدر، مع قيود بسيطة (لا إعادة بيع للمحتوى كما هو، لا إيحاء بتأييد
شخص أو جهة). ننسب المصدر هنا رغم عدم إلزاميته.

| الملف | المصدر الأصلي | الوصف |
|---|---|---|
| `videos/traffic_clip.mp4` | [Dash cam footage in city driving](https://www.pexels.com/video/dash-cam-footage-in-city-driving-4644521/) (Pexels, video 4644521) | مقطع كاميرا سيارة نهاري في مونتريال، فيه ازدحام كافٍ لحجب جزئي بين المركبات. اقتُطعت منه ثوانٍ 28-43 وأُعيد ترميزها. |
| `videos/ambulance_clip.mp4` | [Footage of the street with ambulance passing by](https://www.pexels.com/video/footage-of-the-street-with-ambulance-passing-by-3759222/) (Pexels, video 3759222) | سيارة إسعاف تابعة لمستشفى NewYork-Presbyterian تعبر تقاطعاً نهاراً في مدينة نيويورك. |
| `videos/reference_tracking_output.mp4` | من إنتاجنا | نفس `ambulance_clip.mp4` بعد تشغيل ByteTrack عليه (القسم 11 من الدفتر)، مع صناديق وهويات ومسارات مرسومة. |

جرى ترميز المقطعين المصدرين مجدداً عبر:
```
ffmpeg -i in.mp4 -t 15 -vf scale=640:-2 -c:v libx264 -crf 30 -an out.mp4
```
لضبط الدقة والحجم وحذف الصوت، بلا أي تعديل على المحتوى المرئي.

## النموذج

`models/emergency_best.pt` و `models/yolo11n.pt` منسوخان من الأسبوع
السابع. راجع [`Week7/CREDITS.md`](../Week7/CREDITS.md) لتفاصيل ترخيص
Ultralytics (AGPL-3.0) ومصدر قاعدة بيانات التدريب (Open Images، CC BY).

<div class="note" style="background-color: rgba(249, 168, 37, 0.14); border-right: 5px solid #F9A825; padding: 12px 18px; margin: 16px 0; border-radius: 6px;">
<p><strong>ملاحظة مهمة لمن يحدّث هذا المجلد لاحقاً:</strong> يوجد داخل
مستودع الأسبوع السابع نسختان مختلفتان فعلياً من
<code>emergency_best.pt</code> (بصمتان مختلفتان تماماً)، رغم تطابق
الاسم:</p>
<ul>
<li><code>Week7/models/emergency_best.pt</code> ناتج تدريب <strong>مصغّر</strong>
فقط (5 دورات، 320px، عيّنة مصغّرة من البيانات) - وهذا هو الأضعف.</li>
<li><code>Week8/models/emergency_best.pt</code> (المنسوخ هنا فعلياً) ناتج
التدريب <strong>الكامل</strong> (60 دورة، 416px، قاعدة البيانات كاملة) -
وهو المطابق للأرقام المذكورة في تقييم الأسبوع السابع
(mAP@50 = 0.879 لفئة ambulance).</li>
</ul>
<p>تحقّقنا من هذا مباشرة بفحص <code>train_args</code> المحفوظة داخل كل
ملف <code>.pt</code>، وباختبار الكشف فعلياً على مقاطع هذا الأسبوع. النموذج
المستخدم في دفتر الأسبوع 8 هو النسخة الجيدة - لا تستبدله بنسخة Week7 عن
طريق الخطأ.</p>
</div>

## الأشكال التوضيحية

الأشكال في `media/` من إعداد فريق الدورة بناءً على الأوصاف الكاملة في
[`media/FIGURE_BRIEFS.md`](media/FIGURE_BRIEFS.md).

</div>
