# مصدر قاعدة البيانات ورخصتها

استُخرجت هذه المجموعة من **Open Images Dataset V6/V7** من Google.

- صفحة المجموعة: https://storage.googleapis.com/openimages/web/index.html
- **الصور**: منشورة على Flickr برخصة [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)، وحقوقها لأصحابها الأصليين.
- **التوسيم (صناديق الإحاطة)**: من Google برخصة [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## ما فعلناه بها

1. اخترنا أربع فئات فقط: ambulance، car، truck، bus.
2. أخذنا كل صورة تحتوي على `ambulance`، وأضفنا عيّنة من صور المركبات العادية كأمثلة سلبية.
3. تجاهلنا الصناديق المعلّمة `IsGroupOf` (صندوق يغطي مجموعة أجسام) و `IsDepiction` (رسم أو صورة داخل صورة).
4. صغّرنا كل صورة إلى 416px للضلع الأطول بجودة JPEG 78 لتقليل الحجم.
5. حوّلنا التوسيم من صيغة Open Images (`XMin, XMax, YMin, YMax`) إلى صيغة YOLO (`class x_center y_center width height`).

سكربت التحويل كاملاً في `tools/prepare_week7_dataset.py`.
