# -*- coding: utf-8 -*-
import os
import time
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# إعداداتك
BOT_TOKEN = '8312066648:AAFHr1prjk642UaZExabW8jDr9S-lZxHsdo'
NITRO_API_KEY = '6508fa23bf8d664bb923eb5744af09860255ff93'

def get_raw_iptv_link(user, pwd):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # إضافة User-Agent حقيقي لتجنب حظر السيرفرات
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    driver = None
    try:
        # استخدام التثبيت التلقائي المناسب لبيئة Render
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get("https://moodtv.xyz/create.php")
        
        wait = WebDriverWait(driver, 30)
        # البحث عن خانة اليوزر بمرونة أكبر
        user_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        
        user_field.send_keys(user)
        driver.find_element(By.NAME, "password").send_keys(pwd)
        
        # حل الكابتشا
        captcha_text = driver.find_element(By.ID, "captcha_label").text
        result = eval(captcha_text.replace('=', '').strip())
        
        driver.find_element(By.NAME, "captcha").send_keys(str(result))
        
        # محاولة الضغط على الزر بطريقة تضمن التنفيذ
        submit_btn = driver.find_element(By.NAME, "submit")
        driver.execute_script("arguments[0].click();", submit_btn)
        
        # انتظار كافٍ لتحميل الصفحة التالية
        time.sleep(15)
        
        final_url = driver.current_url
        if "create.php" not in final_url:
            return final_url
        return None
    except Exception as e:
        print(f"Detail error: {e}")
        return None
    finally:
        if driver:
            driver.quit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 البوت جاهز! أرسل البيانات هكذا: `user:pass`")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if ":" in text:
        user, pwd = text.split(":", 1)
        m = await update.message.reply_text("⏳ جاري إنشاء الرابط... قد يستغرق الأمر 20 ثانية")
        
        link = get_raw_iptv_link(user.strip(), pwd.strip())
        
        if link:
            # اختصار الرابط
            api_url = f"https://nitro-link.com/api?api={NITRO_API_KEY}&url={link}&format=text"
            final_link = requests.get(api_url).text.strip()
            await m.edit_text(f"✅ تم الإنشاء بنجاح!\n🔗 رابطك: {final_link}")
        else:
            await m.edit_text("❌ لم ينجح الأمر. تأكد أن اليوزر جديد تماماً ولم يُستخدم من قبل.")
    else:
        await update.message.reply_text("⚠️ أرسل البيانات بصيغة `user:pass`")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    app.run_polling()
