# -*- coding: utf-8 -*-
import os, threading, requests, re
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- تشغيل سيرفر Port لحل مشكلة Render المجاني ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- إعدادات البوت ---
BOT_TOKEN = '8312066648:AAEWpmkMX6WG-wZt9pLQkKPhbRCULoMfQXk'
# استبدل الرابط أدناه برابط الصورة الحقيقية بعد رفعها
PHOTO_URL = 'https://telegra.ph/file/your_image_link.jpg' 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡️ استخراج كود IPTV", callback_data='gen')],
        [InlineKeyboardButton("📢 قناة التحديثات", url="https://t.me/Iptv24_Bot")]
    ]
    # تم تبسيط النص لتجنب أخطاء التنسيق (Parse Entities)
    welcome_text = (
        "👋 أهلاً بك في Iptv24_Bot\n"
        "━━━━━━━━━━━━━━\n"
        "أسرع نظام لتوليد الحسابات مجاناً.\n"
        "اضغط على الزر أدناه للبدء:"
    )
    try:
        await update.message.reply_photo(photo=PHOTO_URL, caption=welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))
    except:
        await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # تحديث النص مع التأكد من عدم وجود رموز Markdown خاطئة
    await query.edit_message_caption(caption="🔄 جاري جلب البيانات من السيرفر...")
    
    try:
        res = requests.get("https://auziatv.com/index.php", timeout=10).text
        host = re.search(r'http://[a-zA-Z0-9.-]+:[0-9]+', res).group(0)
        user = re.search(r'Username[:\s]+([a-zA-Z0-9_-]+)', res, re.I).group(1)
        pwd = re.search(r'Password[:\s]+([a-zA-Z0-9_-]+)', res, re.I).group(1)

        result_card = (
            "🚀 بيانات حسابك جاهزة:\n\n"
            f"🌐 SERVER: {host}\n"
            f"👤 USER: {user}\n"
            f"🔑 PASS: {pwd}\n\n"
            "✅ انسخ البيانات واستمتع بالمشاهدة."
        )
        await query.edit_message_caption(caption=result_card)
    except:
        await query.edit_message_caption(caption="❌ فشل السحب آلياً، يرجى المحاولة لاحقاً.")

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_gen))
    # تنظيف التحديثات العالقة لمنع تضارب النسخ
    app.run_polling(drop_pending_updates=True)
