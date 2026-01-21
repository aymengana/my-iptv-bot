# -*- coding: utf-8 -*-
import os, threading, random
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- 1. سيرفر الويب لضمان استقرار Render ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Iptv24 System is Active!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

# --- 2. الإعدادات ---
BOT_TOKEN = '8312066648:AAFNatDZOZY9utlQNBWK1Jj_5MVvDe0UySw'

# الكود الذي تضعه في اختصار الروابط (أرقام فقط)
ACTIVATION_CODE = "88220033" 

# سجل الحماية لمنع التكرار
user_logs = {}

# --- 3. وظائف البوت ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # رسالة احترافية متناسقة مع شعارك
    welcome_text = (
        "👋 مرحباً بك في Iptv24\n"
        "━━━━━━━━━━━━━━\n"
        "للحصول على بيانات السيرفر:\n"
        "أرسل كود التفعيل (أرقام فقط) هنا 📥\n"
        "━━━━━━━━━━━━━━"
    )
    await update.message.reply_text(welcome_text)

async def handle_activation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text
    
    # حماية من التكرار
    if user_id in user_logs:
        await update.message.reply_text("❌ لقد حصلت على حسابك بالفعل اليوم!")
        return

    # التحقق من الكود الرقمي
    if user_text == ACTIVATION_CODE:
        user_logs[user_id] = True
        
        # بيانات السيرفر الخاص بك
        success_msg = (
            "✅ تم التحقق بنجاح!\n"
            "━━━━━━━━━━━━━━\n"
            "🌐 HOST: `http://top.cloud-ip.cc:2052` \n"
            "👤 USER: `a128` \n"
            "🔑 PASS: `a` \n"
            "━━━━━━━━━━━━━━\n"
            "🚀 انسخ البيانات واستمتع بالمشاهدة."
        )
        await update.message.reply_text(success_msg, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ الكود الرقمي غير صحيح!")

# --- 4. التشغيل النهائي ---
if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_activation))
    
    # حل مشكلة Conflict وتنظيف الجلسات القديمة
    app.run_polling(drop_pending_updates=True)
