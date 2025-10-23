# ربات پاسخگو با RAG و LLM رایگان

سرویس ربات پاسخگو که با استفاده از RAG (Retrieval-Augmented Generation) و Google Gemini API به سوالات کاربران در مورد محصولات به زبان فارسی پاسخ می‌دهد. این پروژه شبیه‌ساز دایرکت اینستاگرام است.

## ویژگی‌ها

 **API با FastAPI** - سریع، مدرن و امن  
 **RAG System** - جستجوی هوشمند در دیتابیس SQLite  
 **Google Gemini API** - استفاده از LLM رایگان  
 **پاسخ فارسی** - تمام پاسخ‌ها به زبان فارسی  
 **Rate Limiting** - محدودیت نرخ درخواست برای امنیت  
 **Input Validation** - اعتبارسنجی ورودی‌ها  
 **100+ محصول تستی** - دیتابیس آماده برای تست  

## معماری سیستم

```
┌─────────────┐
│   Client    │
│  (کاربر)    │
└──────┬──────┘
       │ HTTP POST /simulate_dm
       ▼
┌─────────────────────────────┐
│      FastAPI Endpoint       │
│  (اعتبارسنجی و Rate Limit)  │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────┐      ┌──────────────┐
│   RAG Service   │─────▶│   Database   │
│ (بازیابی اطلاعات)│      │   (SQLite)   │
└─────────┬───────┘      └──────────────┘
          │
          │ محصولات مرتبط
          ▼
┌─────────────────┐
│   LLM Service   │
│  (Gemini API)   │
└─────────┬───────┘
          │
          │ پاسخ هوشمند
          ▼
┌─────────────────┐
│   JSON Response │
│  (پاسخ فارسی)   │
└─────────────────┘
```

## پیش‌نیازها

- Python 3.8 یا بالاتر
- pip (مدیریت پکیج‌های پایتون)
- کلید API رایگان Google Gemini

## نصب و راه‌اندازی

### 1. کلون کردن یا دانلود پروژه

```bash
cd Salona_instagram_bot_task
```

### 2. ساخت محیط مجازی (Virtual Environment)

```bash
# ایجاد محیط مجازی
python -m venv venv

# فعال‌سازی محیط مجازی
# در macOS/Linux:
source venv/bin/activate

# در Windows:
venv\Scripts\activate
```

### 3. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```



### 4. اجرای سرویس

```bash
python main.py
```

یا با uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

سرویس روی آدرس `http://localhost:8000` در دسترس خواهد بود.

## استفاده از API

### Endpoint اصلی: `/simulate_dm`

**متد:** POST  
**آدرس:** `http://localhost:8000/simulate_dm`  
**Content-Type:** `application/json`

### مثال درخواست با curl

```bash
curl -X POST http://localhost:8000/simulate_dm \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "user123",
    "message_id": "m-001",
    "text": "قیمت گوشی آیفون چقدره؟"
  }'
```

### مثال پاسخ

```json
{
  "reply": "تعداد 3 محصول مرتبط پیدا شد:\n- گوشی اپل iPhone 14 Pro: 55،000،000 تومان\n- گوشی اپل iPhone 13: 42،000،000 تومان\n- گوشی اپل iPhone SE 2022: 18،000،000 تومان"
}
```

### سایر نمونه‌های درخواست

#### جستجوی لپ‌تاپ

```bash
curl -X POST http://localhost:8000/simulate_dm \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "u1",
    "message_id": "m2",
    "text": "لپ‌تاپ مک بوک"
  }'
```

#### جستجوی هدفون

```bash
curl -X POST http://localhost:8000/simulate_dm \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "u1",
    "message_id": "m3",
    "text": "هدفون با حذف نویز"
  }'
```

#### سوال در مورد مشخصات

```bash
curl -X POST http://localhost:8000/simulate_dm \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "u1",
    "message_id": "m4",
    "text": "گوشی سامسونگ S23 چه مشخصاتی داره؟"
  }'
```

## Endpoints دیگر

### 1. صفحه اصلی

```bash
curl http://localhost:8000/
```

### 2. Health Check

```bash
curl http://localhost:8000/health
```

### 3. آمار دیتابیس

```bash
curl http://localhost:8000/stats
```

## ساختار پروژه

```
salona_test/
├── main.py                 # FastAPI app و endpoints
├── config.py              # تنظیمات پروژه
├── database.py            # مدیریت دیتابیس SQLite
├── rag_service.py         # سرویس RAG (بازیابی اطلاعات)
├── llm_service.py         # سرویس اتصال به Gemini API
├── requirements.txt       # وابستگی‌های پایتون
├── .env                   # متغیرهای محیطی (ایجاد کنید)
├── .gitignore            # فایل‌های ignore شده
├── README.md             # مستندات (این فایل)
├── db/
│   └── app_data.sqlite   # دیتابیس SQLite (خودکار ایجاد می‌شود)
└── tests/
    └── test_api.py       # تست‌های واحد
```

## دیتابیس

### ساختار جدول `products`

| ستون        | نوع     | توضیحات              |
|-------------|---------|---------------------|
| id          | INTEGER | کلید اصلی (Primary Key) |
| name        | TEXT    | نام محصول           |
| description | TEXT    | توضیحات محصول        |
| price       | REAL    | قیمت (تومان)         |

### داده‌های تستی

دیتابیس شامل بیش از **100 محصول** در دسته‌بندی‌های مختلف است:

-  گوشی‌های موبایل (Samsung, Apple, Xiaomi, Google)
-  لپ‌تاپ (Dell, MacBook, HP, Lenovo, Asus)
-  تبلت (iPad, Samsung Galaxy Tab)
-  ساعت هوشمند (Apple Watch, Samsung, Garmin)
-  هدفون و ایرپاد (AirPods, Sony, Bose, JBL)
-  دوربین (Canon, Sony, Nikon)
-  کنسول بازی (PlayStation, Xbox, Nintendo)
-  اسپیکر (JBL, Sony, Bose)
-  مانیتور (Dell, LG, Samsung, ASUS)
-  لوازم جانبی (کیبورد، ماوس، شارژر، کابل)

دیتابیس به صورت خودکار در اولین اجرا ایجاد و پر می‌شود.

## امنیت

پروژه شامل اقدامات امنیتی زیر است:

### 1. **Rate Limiting**
- محدودیت 10 درخواست در دقیقه برای هر IP
- جلوگیری از حملات DDoS

### 2. **Input Validation**
- اعتبارسنجی طول پیام (حداکثر 1000 کاراکتر)
- بررسی شناسه‌ها برای جلوگیری از Injection Attacks
- استفاده از Pydantic برای validation

### 3. **SQL Injection Prevention**
- استفاده از Parameterized Queries
- Context Manager برای مدیریت امن اتصالات

### 4. **Error Handling**
- مدیریت مناسب خطاها
- عدم افشای اطلاعات حساس در پیام‌های خطا

### 5. **Environment Variables**
- کلیدهای API در فایل .env 
- عدم هاردکد کردن اطلاعات حساس

### 6. **Logging**
- ثبت لاگ‌های امنیتی
- ردیابی درخواست‌های مشکوک


**راه‌حل:** مطمئن شوید محیط مجازی فعال است و تمام وابستگی‌ها نصب شده‌اند:

```bash
source venv/bin/activate  # فعال‌سازی محیط مجازی
pip install -r requirements.txt
```


```bash
# تغییر پورت
python main.py --port 8001
```

## توسعه و گسترش

### افزودن محصولات جدید به دیتابیس

```python
from database import Database

db = Database()
with db.get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
        ("نام محصول", "توضیحات", 1000000)
    )
```

### تغییر مدل LLM

برای استفاده از مدل‌های دیگر، فایل `llm_service.py` را ویرایش کنید:

```python
self.model = genai.GenerativeModel(
    model_name="gemini-pro",  # یا مدل دیگر
    # ...
)
```

### اضافه کردن Embedding-based Search

برای بهبود RAG، می‌توانید از embedding-based search استفاده کنید:

```python
# نصب کتابخانه
pip install sentence-transformers

# استفاده در rag_service.py
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
```


---

**نکته مهم:** این پروژه از API رایگان Gemini استفاده می‌کند که محدودیت‌های استفاده دارد. برای استفاده در پروداکشن، پلن مناسب را انتخاب کنید.

