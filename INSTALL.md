# راهنمای نصب و راه‌اندازی

## نصب سریع

### مرحله 1: نصب وابستگی‌ها

```bash
# ایجاد محیط مجازی
python3 -m venv venv

# فعال‌سازی محیط مجازی
source venv/bin/activate  # macOS/Linux
# یا
venv\Scripts\activate  # Windows

# نصب پکیج‌ها
pip install -r requirements.txt
```

### مرحله 2: تنظیم API Key

1. به آدرس [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey) بروید
2. با اکانت Google خود وارد شوید
3. روی "Create API Key" کلیک کنید
4. API Key را کپی کنید

### مرحله 3: ایجاد فایل .env

فایل `.env` در ریشه پروژه ایجاد کنید:

```bash
GEMINI_API_KEY=your_api_key_here
API_HOST=0.0.0.0
API_PORT=8000
```

**توجه:** `your_api_key_here` را با کلید API واقعی خود جایگزین کنید.

### مرحله 4: راه‌اندازی دیتابیس

```bash
python init_db.py
```

این دستور:
- دیتابیس SQLite را ایجاد می‌کند
- 99+ محصول نمونه اضافه می‌کند
- جستجو را تست می‌کند

### مرحله 5: اجرای سرویس

```bash
# روش 1: استفاده از اسکریپت start
./start.sh

# روش 2: اجرای مستقیم
python main.py

# روش 3: با uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

سرویس در آدرس `http://localhost:8000` در دسترس خواهد بود.

## تست کردن

### تست دستی

```bash
python test_manual.py
```

### تست API (سرویس باید در حال اجرا باشد)

در یک ترمینال دیگر:

```bash
./test_api.sh
```

یا با curl:

```bash
curl -X POST http://localhost:8000/simulate_dm \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "test_user",
    "message_id": "msg_001",
    "text": "قیمت گوشی آیفون چقدره؟"
  }'
```

### تست با pytest

```bash
pytest tests/
```

## عیب‌یابی

### خطا: "ModuleNotFoundError"

**راه‌حل:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### خطا: "GEMINI_API_KEY not set"

**راه‌حل:**
1. مطمئن شوید فایل `.env` وجود دارد
2. بررسی کنید که کلید API درست است
3. سرویس را مجددا راه‌اندازی کنید

### خطا: "Address already in use"

**راه‌حل:**
```bash
# پیدا کردن پروسه
lsof -i :8000

# kill کردن پروسه
kill -9 PID

# یا تغییر پورت
API_PORT=8001 python main.py
```

### خطا: "Database is locked"

**راه‌حل:**
```bash
# بستن تمام اتصالات
rm db/app_data.sqlite
python init_db.py
```

## دسترسی به مستندات API

بعد از راه‌اندازی سرویس:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## توقف سرویس

برای توقف سرویس: `Ctrl+C`

## بروزرسانی

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

