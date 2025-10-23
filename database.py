"""
SQLite database management
"""
import sqlite3
from pathlib import Path
from typing import List, Dict, Any
import logging
from contextlib import contextmanager

from config import DB_PATH, DB_DIR

logger = logging.getLogger(__name__)


class Database:
    """Database management class"""
    
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._ensure_db_directory()
        self._init_db()
    
    def _ensure_db_directory(self):
        """Ensure database directory exists"""
        DB_DIR.mkdir(parents=True, exist_ok=True)
    
    @contextmanager
    def get_connection(self):
        """Context manager for secure database connection management"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database transaction error: {e}")
            raise
        finally:
            conn.close()
    
    def _init_db(self):
        """Create products table if it doesn't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL
                )
            """)
            
            # Check if data exists
            cursor.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]
            
            if count == 0:
                logger.info("Database is empty. Adding sample data...")
                self._populate_sample_data()
    
    def _populate_sample_data(self):
        """Add 100+ sample products to database"""
        sample_products = [
            # گوشی‌های موبایل
            ("گوشی سامسونگ Galaxy S23", "گوشی پرچمدار سامسونگ با پردازنده Snapdragon 8 Gen 2، صفحه نمایش 6.1 اینچ، دوربین 50 مگاپیکسل", 35000000),
            ("گوشی اپل iPhone 14 Pro", "آیفون پرچمدار با تراشه A16 Bionic، صفحه نمایش ProMotion 6.1 اینچ، دوربین 48 مگاپیکسل", 55000000),
            ("گوشی شیائومی Redmi Note 12", "گوشی میان‌رده با پردازنده Snapdragon 685، صفحه نمایش 6.67 اینچ AMOLED، دوربین 50 مگاپیکسل", 8500000),
            ("گوشی سامسونگ Galaxy A54", "گوشی میان‌رده با پردازنده Exynos 1380، صفحه نمایش 6.4 اینچ Super AMOLED", 14500000),
            ("گوشی اپل iPhone 13", "آیفون با تراشه A15 Bionic، صفحه نمایش 6.1 اینچ، دوربین دوگانه 12 مگاپیکسل", 42000000),
            ("گوشی شیائومی Poco X5 Pro", "گوشی گیمینگ با پردازنده Snapdragon 778G، صفحه نمایش 120Hz", 9500000),
            ("گوشی سامسونگ Galaxy Z Fold 5", "گوشی تاشو پرچمدار با صفحه نمایش 7.6 اینچ داخلی و 6.2 اینچ خارجی", 75000000),
            ("گوشی اپل iPhone SE 2022", "آیفون مقرون به صرفه با تراشه A15 Bionic و Touch ID", 18000000),
            ("گوشی شیائومی Mi 13 Pro", "گوشی پرچمدار با دوربین Leica، پردازنده Snapdragon 8 Gen 2", 38000000),
            ("گوشی گوگل Pixel 7", "گوشی با تراشه Google Tensor G2 و دوربین محاسباتی پیشرفته", 28000000),
            
            # لپ‌تاپ‌ها
            ("لپ‌تاپ Dell XPS 13", "لپ‌تاپ نازک و سبک با پردازنده Intel Core i7 نسل 12، رم 16GB، SSD 512GB", 45000000),
            ("لپ‌تاپ MacBook Air M2", "لپ‌تاپ اپل با تراشه M2، صفحه نمایش Liquid Retina 13.6 اینچ", 52000000),
            ("لپ‌تاپ HP Pavilion 15", "لپ‌تاپ همه‌کاره با پردازنده AMD Ryzen 5، رم 8GB، SSD 256GB", 18000000),
            ("لپ‌تاپ Lenovo ThinkPad X1", "لپ‌تاپ بیزینس با پردازنده Intel Core i7، رم 16GB، صفحه نمایش 14 اینچ", 48000000),
            ("لپ‌تاپ Asus ROG Strix G15", "لپ‌تاپ گیمینگ با پردازنده AMD Ryzen 9، کارت گرافیک RTX 3070", 65000000),
            ("لپ‌تاپ MacBook Pro 14", "لپ‌تاپ پرچمدار اپل با تراشه M2 Pro، صفحه نمایش Liquid Retina XDR", 95000000),
            ("لپ‌تاپ Acer Aspire 5", "لپ‌تاپ مقرون به صرفه با پردازنده Intel Core i5 نسل 11، رم 8GB", 15000000),
            ("لپ‌تاپ MSI Creator Z16", "لپ‌تاپ کریتور با صفحه نمایش لمسی، پردازنده Intel Core i9", 85000000),
            ("لپ‌تاپ Microsoft Surface Laptop 5", "لپ‌تاپ با طراحی منحصر به فرد و صفحه نمایش لمسی", 42000000),
            ("لپ‌تاپ Razer Blade 15", "لپ‌تاپ گیمینگ نازک با کارت گرافیک RTX 4070", 95000000),
            
            # تبلت‌ها
            ("تبلت iPad Air 2022", "تبلت اپل با تراشه M1، صفحه نمایش 10.9 اینچ Liquid Retina", 28000000),
            ("تبلت Samsung Galaxy Tab S9", "تبلت اندروید پرچمدار با صفحه نمایش 11 اینچ AMOLED", 32000000),
            ("تبلت iPad Pro 12.9", "تبلت حرفه‌ای اپل با تراشه M2، صفحه نمایش Liquid Retina XDR", 58000000),
            ("تبلت Samsung Galaxy Tab A8", "تبلت مقرون به صرفه با صفحه نمایش 10.5 اینچ", 8500000),
            ("تبلت Lenovo Tab P11 Pro", "تبلت اندروید با صفحه نمایش 11.5 اینچ OLED", 15000000),
            
            # ساعت هوشمند
            ("ساعت هوشمند Apple Watch Series 8", "ساعت هوشمند با سنسورهای سلامتی پیشرفته، صفحه نمایش Always-On", 18000000),
            ("ساعت هوشمند Samsung Galaxy Watch 6", "ساعت هوشمند اندروید با ردیابی سلامتی و GPS", 12000000),
            ("ساعت هوشمند Garmin Fenix 7", "ساعت هوشمند ورزشی با GPS و نقشه توپوگرافی", 25000000),
            ("ساعت هوشمند Xiaomi Mi Band 8", "مچ‌بند هوشمند مقرون به صرفه با ردیابی فعالیت", 1200000),
            ("ساعت هوشمند Huawei Watch GT 3", "ساعت هوشمند با عمر باتری طولانی و طراحی کلاسیک", 8500000),
            
            # هدفون و ایرپاد
            ("ایرپاد Apple AirPods Pro 2", "ایرپاد با حذف نویز فعال، صدای فضایی، باتری تا 6 ساعت", 12000000),
            ("هدفون Sony WH-1000XM5", "هدفون بی‌سیم با بهترین حذف نویز، صدای Hi-Res", 15000000),
            ("ایرپاد Samsung Galaxy Buds 2 Pro", "ایرپاد پرچمدار با حذف نویز هوشمند، صدای 360 درجه", 6500000),
            ("هدفون Bose QuietComfort 45", "هدفون با حذف نویز برتر و راحتی بالا", 14000000),
            ("ایرپاد JBL Wave 200TWS", "ایرپاد مقرون به صرفه با کیفیت صدای خوب", 2200000),
            ("هدفون Audio-Technica ATH-M50x", "هدفون استودیویی حرفه‌ای با صدای دقیق", 6500000),
            
            # دوربین
            ("دوربین Canon EOS R6 Mark II", "دوربین بدون آینه فول فریم با سنسور 24 مگاپیکسل", 125000000),
            ("دوربین Sony Alpha A7 IV", "دوربین حرفه‌ای با سنسور 33 مگاپیکسل، فیلمبرداری 4K", 135000000),
            ("دوربین Nikon Z6 II", "دوربین بدون آینه با سنسور 24.5 مگاپیکسل", 95000000),
            ("دوربین Fujifilm X-T5", "دوربین APS-C با سنسور 40 مگاپیکسل", 78000000),
            ("دوربین GoPro Hero 11", "دوربین اکشن با قابلیت فیلمبرداری 5.3K", 18000000),
            ("دوربین DJI Osmo Action 3", "دوربین اکشن با صفحه نمایش دوگانه", 15000000),
            
            # کنسول بازی
            ("کنسول Sony PlayStation 5", "کنسول نسل نهمی با SSD فوق سریع و کنترلر DualSense", 28000000),
            ("کنسول Microsoft Xbox Series X", "کنسول قدرتمند با پشتیبانی 4K و 120fps", 25000000),
            ("کنسول Nintendo Switch OLED", "کنسول هیبریدی با صفحه نمایش 7 اینچ OLED", 15000000),
            ("کنسول Steam Deck", "کنسول دستی PC گیمینگ", 22000000),
            
            # اسپیکر
            ("اسپیکر JBL Charge 5", "اسپیکر بلوتوث ضد آب با باتری 20 ساعته", 5500000),
            ("اسپیکر Sony SRS-XB43", "اسپیکر قدرتمند با بیس عمیق و نورپردازی LED", 7500000),
            ("اسپیکر Bose SoundLink Revolve+", "اسپیکر 360 درجه با صدای استریو", 12000000),
            ("اسپیکر Marshall Emberton II", "اسپیکر با طراحی کلاسیک و صدای قدرتمند", 6800000),
            ("اسپیکر Amazon Echo Dot 5", "اسپیکر هوشمند با دستیار صوتی Alexa", 2500000),
            
            # مانیتور
            ("مانیتور Dell UltraSharp U2723DE", "مانیتور 27 اینچ 4K با پنل IPS و USB-C", 22000000),
            ("مانیتور LG UltraGear 27GN950", "مانیتور گیمینگ 27 اینچ 4K با 144Hz", 28000000),
            ("مانیتور Samsung Odyssey G7", "مانیتور گیمینگ منحنی 32 اینچ با 240Hz", 32000000),
            ("مانیتور ASUS ProArt PA278QV", "مانیتور حرفه‌ای 27 اینچ برای طراحی", 18000000),
            ("مانیتور BenQ PD2700U", "مانیتور 27 اینچ 4K برای طراحان", 16000000),
            
            # کیبورد و ماوس
            ("کیبورد مکانیکال Keychron K2", "کیبورد مکانیکال بی‌سیم با سوئیچ‌های Gateron", 4500000),
            ("کیبورد Logitech MX Keys", "کیبورد بی‌سیم پرمیوم با نورپردازی هوشمند", 5200000),
            ("ماوس Logitech MX Master 3S", "ماوس ارگونومیک بی‌سیم با دقت بالا", 4200000),
            ("ماوس Razer DeathAdder V3", "ماوس گیمینگ با سنسور 30000 DPI", 3500000),
            ("کیبورد Corsair K70 RGB", "کیبورد مکانیکال گیمینگ با نورپردازی RGB", 6500000),
            
            # شارژر و پاوربانک
            ("شارژر Anker PowerPort III", "شارژر سریع 65 وات با 3 پورت USB", 1800000),
            ("پاوربانک Xiaomi 20000mAh", "پاوربانک با ظرفیت بالا و شارژ سریع 33W", 1500000),
            ("پاوربانک Anker PowerCore 26800", "پاوربانک قدرتمند با 3 پورت خروجی", 2800000),
            ("شارژر Apple MagSafe", "شارژر بی‌سیم 15 وات برای آیفون", 2200000),
            ("شارژر Samsung 45W Super Fast", "شارژر سریع سامسونگ با کابل USB-C", 1200000),
            
            # روتر و شبکه
            ("روتر TP-Link Archer AX73", "روتر WiFi 6 با سرعت تا 5400 Mbps", 4500000),
            ("روتر ASUS RT-AX86U", "روتر گیمینگ WiFi 6 با پورت 2.5G", 8500000),
            ("روتر Xiaomi AX3000", "روتر مقرون به صرفه با WiFi 6", 1500000),
            ("مش وایفای Google Nest WiFi", "سیستم مش وایفای با پوشش گسترده", 12000000),
            
            # هارد و SSD
            ("هارد اکسترنال WD My Passport 2TB", "هارد اکسترنال قابل حمل با USB 3.2", 3500000),
            ("SSD اکسترنال Samsung T7 1TB", "SSD خارجی سریع با سرعت تا 1050 MB/s", 5200000),
            ("هارد اکسترنال Seagate Expansion 4TB", "هارد اکسترنال با ظرفیت بالا", 4800000),
            ("SSD داخلی Samsung 980 PRO 1TB", "SSD NVMe با سرعت بالا", 4500000),
            
            # کابل و لوازم جانبی
            ("کابل HDMI Belkin Ultra High Speed", "کابل HDMI 2.1 با پشتیبانی 8K", 850000),
            ("کابل USB-C Anker Powerline III", "کابل USB-C با طول عمر بالا", 650000),
            ("هاب USB-C Anker 7-in-1", "هاب چندکاره با HDMI، USB، و SD Card", 2200000),
            ("پایه لپ‌تاپ Rain Design mStand", "پایه آلومینیومی ارگونومیک", 2500000),
            
            # چاپگر و اسکنر
            ("چاپگر HP LaserJet Pro M404dn", "چاپگر لیزری سیاه و سفید", 12000000),
            ("چاپگر Canon PIXMA G6020", "چاپگر جوهرافشان رنگی با مخزن", 9500000),
            ("چاپگر Epson EcoTank L3250", "چاپگر سه‌کاره با مخزن جوهر", 7500000),
            ("اسکنر Fujitsu ScanSnap iX1600", "اسکنر اسناد با سرعت بالا", 18000000),
            
            # وب‌کم و میکروفون
            ("وب‌کم Logitech C920 HD Pro", "وب‌کم 1080p با میکروفون استریو", 3200000),
            ("وب‌کم Razer Kiyo Pro", "وب‌کم حرفه‌ای با سنسور بزرگ", 5500000),
            ("میکروفون Blue Yeti", "میکروفون USB حرفه‌ای برای استریم و پادکست", 6500000),
            ("میکروفون HyperX QuadCast S", "میکروفون استریم با نورپردازی RGB", 7200000),
            
            # لوازم جانبی موبایل
            ("قاب محافظ Spigen Ultra Hybrid", "قاب شفاف محافظ برای گوشی‌های مختلف", 450000),
            ("گلس محافظ صفحه Belkin ScreenForce", "گلس تمپرد با ضربه‌گیر", 350000),
            ("پایه نگهدارنده موبایل Anker MagGo", "پایه مگنتی برای آیفون", 1200000),
            ("رینگ لایت Neewer 18 اینچ", "رینگ لایت برای عکاسی و ویدیو", 2800000),
            
            # گجت‌های هوشمند
            ("دستیار صوتی Amazon Echo Show 10", "نمایشگر هوشمند با چرخش خودکار", 12000000),
            ("لامپ هوشمند Philips Hue", "لامپ LED هوشمند با 16 میلیون رنگ", 2200000),
            ("پریز هوشمند TP-Link Kasa", "پریز هوشمند با کنترل از راه دور", 850000),
            ("ترموستات هوشمند Nest Learning", "ترموستات یادگیرنده با صرفه‌جویی انرژی", 8500000),
            
            # دوچرخه برقی و اسکوتر
            ("اسکوتر برقی Xiaomi Mi Electric Scooter 3", "اسکوتر برقی با برد 30 کیلومتر", 15000000),
            ("دوچرخه برقی Fiido D11", "دوچرخه برقی تاشو با باتری لیتیومی", 22000000),
            
            # عینک هوشمند
            ("عینک هوشمند Meta Ray-Ban", "عینک هوشمند با دوربین و اسپیکر", 18000000),
            
            # ربات جاروبرقی
            ("ربات جاروبرقی Roborock S7", "ربات جاروبرقی با قابلیت دستمال زدن", 18000000),
            ("ربات جاروبرقی Xiaomi Mi Robot Vacuum", "ربات جاروبرقی با ناوبری لیزری", 8500000),
        ]
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(
                "INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
                sample_products
            )
            logger.info(f"{len(sample_products)} products successfully added to database.")
    
    def search_products(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search products based on keywords with intelligent scoring"""
        query_cleaned = query.strip().lower()
        
        stop_words = {
            'قیمت', 'چقدر', 'چقدره', 'چند', 'چنده', 'کدوم', 'کدام', 
            'میخوام', 'میخواهم', 'بگو', 'بگید', 'لطفا', 'لطفاً',
            'چیه', 'چیست', 'هست', 'است', 'دارید', 'داره', 'دارد',
            'برای', 'تو', 'در', 'با', 'از', 'به', 'را', 'رو'
        }
        
        category_words = {
            'گوشی', 'موبایل', 'تلفن',
            'لپتاپ', 'لپ‌تاپ', 'نوتبوک',
            'تبلت', 
            'ساعت', 'هدفون', 'ایرپاد',
            'دوربین', 'کنسول', 'اسپیکر',
            'مانیتور', 'کیبورد', 'ماوس',
            'شارژر', 'پاوربانک', 'روتر',
            'هارد', 'چاپگر', 'اسکنر',
        }
        
        brand_identifiers = {
            'آیفون': ['آیفون', 'iphone', 'ایفون'],
            'اپل': ['اپل', 'apple'],
            'مک': ['مک', 'mac', 'macbook', 'مکبوک', 'بوک'],
            'سامسونگ': ['سامسونگ', 'samsung'],
            'گلکسی': ['گلکسی', 'galaxy'],
            'شیائومی': ['شیائومی', 'xiaomi', 'شائومی'],
            'می': ['می'],
            'ردمی': ['ردمی', 'redmi'],
            'دل': ['dell', 'دل'],
            'اچ پی': ['hp', 'اچ‌پی'],
            'لنوو': ['lenovo', 'لنوو'],
            'ایسوس': ['asus', 'ایسوس'],
            'ایسر': ['acer', 'ایسر'],
            'ام اس آی': ['msi', 'ام‌اس‌آی'],
            'مایکروسافت': ['microsoft', 'surface', 'مایکروسافت'],
            'گوگل': ['google', 'pixel', 'گوگل'],
            'سونی': ['sony', 'سونی'],
            'نیکون': ['nikon', 'نیکون'],
            'کانن': ['canon', 'کانن'],
        }
        
        raw_keywords = [word for word in query_cleaned.split() if len(word) > 1 and word not in stop_words]
        
        brand_keywords = []
        category_keywords = []
        other_keywords = []
        
        for keyword in raw_keywords:
            is_brand = False
            for brand_name, variants in brand_identifiers.items():
                if keyword in variants:
                    brand_keywords.extend(variants)
                    is_brand = True
                    break
            
            if not is_brand:
                if keyword in category_words:
                    category_keywords.append(keyword)
                else:
                    other_keywords.append(keyword)
        
        brand_keywords = list(set(brand_keywords))
        category_keywords = list(set(category_keywords))
        other_keywords = list(set(other_keywords))
        
        unique_keywords = brand_keywords + other_keywords + category_keywords
        
        if not unique_keywords:
            return []
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description, price FROM products")
            all_products = cursor.fetchall()
            
            def is_word_match(keyword, text):
                """Check if keyword appears as a complete word in text"""
                import re
                pattern = r'(?:^|\s|[^\w\u0600-\u06FF])' + re.escape(keyword) + r'(?:$|\s|[^\w\u0600-\u06FF])'
                return re.search(pattern, text) is not None
            
            scored_products = []
            for product in all_products:
                name_lower = product["name"].lower()
                desc_lower = (product["description"] or "").lower()
                
                score = 0
                matched_brand_keywords = 0
                matched_other_keywords = 0
                matched_category_keywords = 0
                
                for keyword in brand_keywords:
                    if is_word_match(keyword, name_lower):
                        score += 50
                        matched_brand_keywords += 1
                    elif is_word_match(keyword, desc_lower):
                        score += 20
                        matched_brand_keywords += 1
                
                for keyword in other_keywords:
                    if is_word_match(keyword, name_lower):
                        score += 15
                        matched_other_keywords += 1
                    elif is_word_match(keyword, desc_lower):
                        score += 5
                        matched_other_keywords += 1
                
                for keyword in category_keywords:
                    if is_word_match(keyword, name_lower):
                        score += 5
                        matched_category_keywords += 1
                    elif is_word_match(keyword, desc_lower):
                        score += 2
                        matched_category_keywords += 1
                
                if brand_keywords and matched_brand_keywords == 0:
                    continue
                
                if brand_keywords and category_keywords:
                    if matched_brand_keywords == 0 or matched_category_keywords == 0:
                        continue
                
                total_matched = matched_brand_keywords + matched_other_keywords + matched_category_keywords
                if total_matched > 1:
                    score += total_matched * 10
                
                if matched_brand_keywords > 0 and matched_category_keywords > 0:
                    score += 30
                
                if score > 0:
                    scored_products.append({
                        "product": product,
                        "score": score,
                        "matched_brand": matched_brand_keywords,
                        "matched_other": matched_other_keywords,
                        "matched_category": matched_category_keywords
                    })
            
            scored_products.sort(key=lambda x: x["score"], reverse=True)
            top_products = scored_products[:limit]
            
            results = []
            for item in top_products:
                product = item["product"]
                results.append({
                    "id": product["id"],
                    "name": product["name"],
                    "description": product["description"],
                    "price": product["price"]
                })
            
            return results
    
    def get_all_products(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all products"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description, price FROM products LIMIT ?", (limit,))
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                results.append({
                    "id": row["id"],
                    "name": row["name"],
                    "description": row["description"],
                    "price": row["price"]
                })
            
            return results

