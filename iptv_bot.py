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
    
    # تحديد مسار الكروم للسيرفر (هام جداً لـ Render)
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://moodtv.xyz/create.php")
        
        wait = WebDriverWait(driver, 30)
        user_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        
        user_field.send_keys(user)
        driver.find_element(By.NAME, "password").send_keys(pwd)
        
        captcha_text = driver.find_element(By.ID, "captcha_label").text
        result = eval(captcha_text.replace('=', '').strip())
        
        driver.find_element(By.NAME, "captcha").send_keys(str(result))
        driver.find_element(By.NAME, "submit").click()
        
        time.sleep(10)
        final_url = driver.current_url
        return final_url if "create.php" not in final_url else None
    except:
        return None
    finally:
        if driver: driver.quit()

async def start(update, context):
    await update.message.reply_text("🚀 أرسل اليوزر والباسورد (user:pass)")

async def handle_msg(update, context):
    if ":" in update.message.text:
        user, pwd = update.message.text.split(":", 1)
        m = await update.message.reply_text("⏳ جاري العمل...")
        link = get_raw_iptv_link(user.strip(), pwd.strip())
        if link:
            res = requests.get(f"https://nitro-link.com/api?api={NITRO_API_KEY}&url={link}&format=text")
            await m.edit_text(f"✅ تم بنجاح:\n{res.text}")
        else:
            await m.edit_text("❌ حدث خطأ، جرب بيانات أخرى.")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    app.run_polling()