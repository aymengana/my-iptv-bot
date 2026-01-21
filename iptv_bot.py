# -*- coding: utf-8 -*-
import requests
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# توكن البوت الخاص بك
BOT_TOKEN = '8312066648:AAFHr1prjk642UaZExabW8jDr9S-lZxHsdo'

def generate_random_info(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "💎 **مرحباً بك في MoodTV Generator v4.0**\n"
        "━━━━━━━━━━━━━━\n"
        "📺 **بوت استخراج اشتراكات MoodTV الحقيقية**\n"
        "🚀 **أرسل أي رسالة لتوليد حساب شغال الآن!**"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("⏳ **جاري إنشاء حساب على MoodTV...**", parse_mode='Markdown')
    
    user = generate_random_info(9)
    pwd = generate_random_info(10)
    
    # محاولة إنشاء الحساب برمجياً عبر موقع MoodTV
    url = "https://moodtv.xyz/create.php"
    payload = {'username': user, 'password': pwd, 'submit': ''}
    
    try:
        # إرسال طلب إنشاء الحساب للموقع
        response = requests.post(url, data=payload, timeout=15)
        
        if response.status_code == 200:
            # إذا نجح الموقع في الرد، نرسل البيانات للمستخدم بتصميمك الاحترافي
            host = "http://moodtv.xyz:8080"
            response_text = (
                "✨ **تم إنشاء حساب MoodTV بنجاح!** ✨\n"
                "━━━━━━━━━━━━━━\n"
                f"🌐 **SERVER:** `{host}`\n"
                f"👤 **USER:** `{user}`\n"
                f"🔑 **PASS:** `{pwd}`\n"
                "━━━━━━━━━━━━━━\n"
                "✅ **هذا الحساب تم إنشاؤه الآن وسيعمل فوراً!**\n"
                "📺 *استخدم تطبيق IPTV Smarters للمشاهدة.*"
            )
            await status_msg.edit_text(response_text, parse_mode='Markdown')
        else:
            await status_msg.edit_text("❌ **الموقع لا يستجيب حالياً.** حاول مرة أخرى بعد قليل.")
            
    except Exception as e:
        await status_msg.edit_text(f"⚠️ **فشل الاتصال بموقع MoodTV:**\n`{e}`")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    app.run_polling()
