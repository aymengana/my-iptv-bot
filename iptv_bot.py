# -*- coding: utf-8 -*-
import requests
import random
import string
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = '8312066648:AAFHr1prjk642UaZExabW8jDr9S-lZxHsdo'

def get_random_string(length):
    # توليد نص عشوائي لضمان عدم تكرار اليوزر
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("⏳ **جاري إنشاء اشتراك فريد لك...**", parse_mode='Markdown')
    
    # 1. تجهيز بيانات الحساب الجديد
    username = f"mood_{get_random_string(6)}"
    password = get_random_string(8)
    
    # 2. إرسال الطلب لموقع MoodTV (محاكاة المتصفح)
    url = "https://moodtv.xyz/create.php"
    payload = {
        'username': username,
        'password': password,
        'submit': '' # محاكاة الضغط على زر الإنشاء
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://moodtv.xyz/create.php'
    }

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=15)
        
        # التأكد من أن الموقع استجاب بنجاح
        if response.status_code == 200:
            host = "http://moodtv.xyz:8080"
            
            response_text = (
                "✨ **تم توليد اشتراكك الخاص!** ✨\n"
                "━━━━━━━━━━━━━━\n"
                f"🌐 **SERVER:** `{host}`\n"
                f"👤 **USER:** `{username}`\n"
                f"🔑 **PASS:** `{password}`\n"
                "━━━━━━━━━━━━━━\n"
                "✅ **هذا الكود يدعم متصل واحد فقط.**\n"
                "📺 *يعمل على IPTV Smarters و VLC.*"
            )
            await status_msg.edit_text(response_text, parse_mode='Markdown')
        else:
            await status_msg.edit_text("❌ السيرفر لا يستجيب حالياً، جرب مرة أخرى.")
            
    except Exception as e:
        await status_msg.edit_text(f"⚠️ حدث خطأ أثناء الاتصال بالموقع:\n`{str(e)}`")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("🚀 أرسل أي رسالة لإنشاء كودك الشخصي!")))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    app.run_polling()
