# أدوات تصميم منشورات زينب

- `build/base.css`: أنماط الهوية (IBM Plex Arabic، الألوان، الترويسة والتذييل).
- `build/fonts/`: خط IBM Plex Sans Arabic (رخصة OFL).
- `build/example-carousel.html`: مثال كاروسيل بالنسق التحريري والخلفيات المنقوشة.
- `build/example-stories.html`: مثال ستوري 1080×1920.

التشغيل (يتطلب Playwright Chromium و Pillow):

    cd tools
    python3 -I render_any.py <file.html داخل build/> <مجلد الإخراج> <بادئة>

ضع ملف HTML الجديد داخل `build/` واربطه بـ `base.css`. كل شريحة `<section class="slide">` (أو `slide tall` للستوري).
