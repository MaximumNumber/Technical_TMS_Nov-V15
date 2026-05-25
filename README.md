# نظام إدارة الجداول الدراسية (TMS)
## Timetable Management System — Sudan University of Science and Technology

نظام متكامل لإدارة الجداول الدراسية مبني بـ **Django 5.2** و **PostgreSQL**، يدعم أدوار متعددة: مدير النظام، مدير الكلية، رئيس القسم، الأستاذ، والطالب. الواجهة كاملة بالعربية RTL.

---

## المميزات

- إدارة كاملة للجداول (محاضرات + معامل)
- كشف تعارضات فوري مع اقتراحات بديلة
- سجل التغييرات مع استعادة بنقرة واحدة
- إشعارات فورية مع عداد قراءة
- تصدير / استيراد (CSV, Excel, PDF)
- لوحة تحليلات (استخدام القاعات، أعباء الأساتذة)
- واجهة عربية RTL كاملة
- نظام صلاحيات محكم مع تشفير bcrypt
- سير عمل طلبات التغيير (تقديم ← موافقة/رفض ← إشعار)
- جدول عام قابل للعرض بدون تسجيل دخول

---

## المتطلبات

| المكوّن | الإصدار | الرابط |
|---------|---------|--------|
| Python | 3.11+ | https://python.org/downloads/ |
| PostgreSQL | 14+ | https://www.postgresql.org/download/windows/ |
| pip | أي إصدار حديث | (مضمّن مع Python) |

> **ملاحظة:** هذا المشروع يستخدم **PostgreSQL حصراً** — لا يدعم SQLite.

---

## الإعداد على Windows (خطوة بخطوة)

### الخطوة 1 — تثبيت المتطلبات

**Python 3.11+:**  
1. حمّل من https://python.org/downloads/  
2. أثناء التثبيت: **فعّل خيار "Add Python to PATH"**

**PostgreSQL 14+:**  
1. حمّل من https://www.postgresql.org/download/windows/  
2. أثناء التثبيت: احفظ كلمة مرور المستخدم `postgres` — ستحتاجها

---

### الخطوة 2 — إنشاء قاعدة البيانات

افتح **pgAdmin** أو **psql** ونفّذ:

```sql
CREATE DATABASE tms_db;
```

---

### الخطوة 3 — إعداد ملف البيئة

```bat
copy .env.example .env
```

عدّل ملف `.env` بمحرر النصوص:

```env
SECRET_KEY=ضع-مفتاحاً-سرياً-عشوائياً-هنا
DEBUG=True
PGDATABASE=tms_db
PGUSER=postgres
PGPASSWORD=كلمة_مرور_PostgreSQL
PGHOST=localhost
PGPORT=5432
```

> **لتوليد SECRET_KEY:** شغّل: `python -c "import secrets; print(secrets.token_urlsafe(50))"`

---

### الخطوة 4 — تشغيل سكريبت الإعداد

```bat
setup.bat
```

سيقوم تلقائياً بـ:
1. إنشاء بيئة Python الافتراضية
2. تثبيت جميع المكتبات
3. تطبيق migrations قاعدة البيانات
4. جمع الملفات الثابتة
5. إنشاء حساب المدير (`admin` / `admin123`)
6. (اختياري) تحميل بيانات تجريبية

---

### الخطوة 5 — تشغيل الخادم

```bat
run_dev.bat
```

أو يدوياً:

```bat
venv\Scripts\activate
python manage.py runserver 0.0.0.0:5000
```

افتح المتصفح على: **http://localhost:5000**

---

## الإعداد اليدوي (بدون السكريبت)

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py seed_admin --username admin --password admin123
python manage.py seed_data
python manage.py runserver 0.0.0.0:5000
```

---

## التشغيل اليومي (بعد الإعداد الأول)

```bat
run_dev.bat
```

أو:

```bat
venv\Scripts\activate
python manage.py runserver 0.0.0.0:5000
```

---

## بيانات الدخول الافتراضية

| الدور | اسم المستخدم | كلمة المرور | النطاق |
|-------|-------------|-------------|--------|
| مدير النظام | `admin` | `admin123` | النظام كاملاً |
| مدير الكلية | `mgr_eng` | `mgr123` | كلية الهندسة |
| مدير الكلية | `mgr_cs` | `mgr123` | كلية الحاسوب |
| مدير الكلية | `mgr_sci` | `mgr123` | كلية العلوم |
| رئيس القسم | `dh_cs` | `dh123` | قسم الحاسوب |
| رئيس القسم | `dh_it` | `dh123` | قسم تقنية المعلومات |
| رئيس القسم | `dh_elec` | `dh123` | قسم الإلكترونيات |
| أستاذ | `prof_ahmed` | `prof123` | الهندسة |
| أستاذ | `prof_sara` | `prof123` | الحاسوب |
| أستاذ | `prof_khalid` | `prof123` | الحاسوب |
| أستاذ | `prof_fatima` | `prof123` | العلوم |
| أستاذ | `prof_omar` | `prof123` | الهندسة |
| أستاذ | `prof_rana` | `prof123` | تقنية المعلومات |
| طالب | `std_ali` | `std123` | حاسوب سنة 1 |
| طالب | `std_maryam` | `std123` | حاسوب سنة 1 |
| طالب | `std_ibrahim` | `std123` | حاسوب سنة 2 |
| طالب | `std_salma` | `std123` | الهندسة |

> **ملاحظة:** بيانات الدخول أعلاه تتوفر بعد تشغيل `seed_data`. دائماً متاح: `admin`.

---

## الصلاحيات حسب الدور

| الصلاحية | مدير النظام | مدير الكلية | رئيس القسم | أستاذ | طالب |
|----------|:-----------:|:-----------:|:----------:|:-----:|:----:|
| إدارة الجامعات والكليات | ✓ | — | — | — | — |
| إدارة الأقسام والمقررات | — | ✓ | — | — | — |
| إدارة الأساتذة والطلاب | — | ✓ | — | — | — |
| إنشاء/تعديل الجداول | — | ✓ | عرض فقط | — | — |
| طلبات تغيير المواعيد | — | موافقة | موافقة | تقديم | — |
| الإحصائيات والتقارير | ✓ | ✓ | — | — | — |
| عرض الجدول الشخصي | — | — | — | ✓ | ✓ |
| تغيير كلمة المرور | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## جميع الصفحات والروابط

| الصفحة | الرابط | الصلاحية |
|--------|--------|----------|
| صفحة الدخول | `/login/` | عام |
| الجدول العام | `/schedule/` | عام (بدون دخول) |
| لوحة مدير النظام | `/admin-dashboard/` | مدير النظام |
| الجامعات | `/universities/` | مدير النظام |
| الفروع | `/branches/` | مدير النظام |
| الكليات | `/colleges/` | مدير النظام |
| القاعات (admin) | `/admin/rooms/` | مدير النظام |
| القاعات الكبيرة (admin) | `/admin/halls/` | مدير النظام |
| المستخدمون | `/admin/users/` | مدير النظام |
| جميع الجداول | `/admin/all-schedules/` | مدير النظام |
| سجل التغييرات | `/changelog/` | المدراء+ |
| الإحصائيات | `/analytics/` | المدراء+ |
| تصدير / استيراد | `/export-import/` | المدراء+ |
| مركز الإشعارات | `/notifications/` | مدير النظام |
| لوحة مدير الكلية | `/cm/dashboard/` | م. الكلية / ر. القسم |
| الأقسام | `/cm/departments/` | مدير الكلية |
| الفترات الدراسية | `/cm/academic-periods/` | مدير الكلية |
| المقررات | `/cm/courses/` | مدير الكلية |
| التخصصات | `/cm/specializations/` | مدير الكلية |
| الأساتذة | `/cm/instructors/` | مدير الكلية |
| القاعات (CM) | `/cm/rooms/` | مدير الكلية |
| القاعات الكبيرة (CM) | `/cm/halls/` | مدير الكلية |
| الطلاب | `/cm/students/` | مدير الكلية |
| رؤساء الأقسام | `/cm/dept-heads/` | مدير الكلية |
| جدول المحاضرات | `/cm/schedule/lectures/` | م. الكلية / ر. القسم |
| جدول المعامل | `/cm/schedule/labs/` | م. الكلية / ر. القسم |
| طلبات التغيير | `/cm/requests/` | م. الكلية / ر. القسم |
| تقرير الأستاذ | `/cm/reports/professor/` | مدير الكلية |
| تقرير القاعة | `/cm/reports/room/` | مدير الكلية |
| جدول الأستاذ | `/professor/schedule/` | أستاذ |
| طلباتي | `/professor/requests/` | أستاذ |
| إشعارات الأستاذ | `/professor/notifications/` | أستاذ |
| جدول الطالب | `/student/schedule/` | طالب |
| تحميل PDF | `/student/schedule/pdf/` | طالب |
| إعدادات الحساب | `/account/settings/` | الجميع |
| تغيير كلمة المرور | `/change-password/` | الجميع |

---

## أوامر الإدارة

```bash
# إنشاء حساب مدير النظام
python manage.py seed_admin --username admin --password admin123

# تحميل بيانات تجريبية كاملة
python manage.py seed_data

# تطبيق migrations
python manage.py migrate

# جمع الملفات الثابتة
python manage.py collectstatic --noinput
```

---

## استكشاف الأخطاء الشائعة على Windows

| المشكلة | الحل |
|---------|------|
| `python` غير معروف | أعد تثبيت Python مع تفعيل "Add to PATH". أو استخدم `py` بدل `python` |
| `pip` غير معروف | استخدم `python -m pip install -r requirements.txt` |
| `No module named 'django'` | البيئة الافتراضية غير مفعّلة — شغّل `venv\Scripts\activate` |
| `FATAL: password authentication failed` | تحقق من `PGPASSWORD` في `.env` |
| `connection refused` | PostgreSQL لا يعمل — افتحه من Services أو pgAdmin |
| `relation does not exist` | شغّل `python manage.py migrate` |
| CSS لا يظهر | شغّل `python manage.py collectstatic --noinput` |
| صفحة الدخول تعيد التوجيه | امسح cookies المتصفح لـ `localhost` |
| تصدير PDF يفشل | تحقق من وجود `static/fonts/Amiri-Regular.ttf` |
| المنفذ مشغول | استخدم `python manage.py runserver 0.0.0.0:8080` |
| نسيت كلمة مرور admin | شغّل `python manage.py seed_admin --username admin --password admin123` |

---

## المكتبات المستخدمة

| المكتبة | الغرض |
|---------|-------|
| Django 5.2 | إطار العمل الرئيسي |
| psycopg2-binary | اتصال PostgreSQL |
| bcrypt 5.0 | تشفير كلمات المرور |
| WhiteNoise 6.12 | تقديم الملفات الثابتة |
| Gunicorn | خادم الإنتاج |
| openpyxl | تصدير Excel |
| ReportLab | تصدير PDF |
| arabic-reshaper + python-bidi | النص العربي في PDF |
| django-crispy-forms | نماذج Bootstrap 5 |
| Pillow | معالجة الصور |
| python-dotenv | قراءة ملف `.env` |

---

## هيكل المشروع

```
tms/                        إعدادات Django وتوجيه URLs الرئيسي
timetable/                  التطبيق الرئيسي
  models.py                 جميع نماذج قاعدة البيانات (25+ نموذج)
  views.py                  جميع Views لجميع الأدوار
  views_extras.py           الإحصائيات والتصدير وسجل التغييرات
  forms.py                  جميع نماذج Django
  urls.py                   جميع URL patterns (60+ رابط)
  backends.py               نظام المصادقة المخصص (bcrypt)
  templatetags/             فلاتر القوالب المخصصة
  management/
    commands/
      seed_admin.py         إنشاء حساب مدير النظام
      seed_data.py          تحميل البيانات التجريبية
  migrations/               migrations قاعدة البيانات
templates/
  base.html                 القالب الأساسي (sidebar, topbar, إشعارات)
  login.html                صفحة الدخول
  timetable/                40+ قالب صفحة
static/
  css/                      الملف الرئيسي للتنسيق (tms-premium.css)
  fonts/                    خطوط عربية (Amiri) لتصدير PDF
staticfiles/                الملفات الثابتة المجمّعة (لا تعدّل يدوياً)
requirements.txt            جميع مكتبات Python المطلوبة
.env.example                مثال لملف البيئة
setup.bat                   سكريبت إعداد Windows التلقائي
run_dev.bat                 سكريبت تشغيل خادم التطوير
README.md                   هذا الملف
```

---

## ملاحظات للإنتاج

1. ضع `DEBUG=False` في `.env`
2. أضف نطاقك في `ALLOWED_HOSTS`
3. غيّر `SECRET_KEY` لمفتاح سري فريد وقوي
4. استخدم Gunicorn:
   ```bash
   gunicorn tms.wsgi:application --bind 0.0.0.0:5000 --workers 3
   ```
5. لا تشغّل `seed_data` في بيئة الإنتاج

---

## التواصل والدعم

نظام TMS مطوّر لـ **جامعة السودان للعلوم والتكنولوجيا**.
