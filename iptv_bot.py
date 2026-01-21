# -*- coding: utf-8 -*-
import os, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- 1. سيرفر الويب لضمان استقرار الخدمة ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Iptv24 System is Fully Active!"

def run_flask():
    # استخدام المنفذ 10000 المتوافق مع سجلاتك بنجاح
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

# --- 2. الإعدادات (التوكن الجديد والبيانات) ---
BOT_TOKEN = '8312066648:AAGK2oDn870CtWxpJNxFlgGP8r5gRTYCio8'
MY_LINK = "https://linkjust.com/YP7Q" 
ACTIVATION_CODE = "88220033" 
user_logs = {}

# --- 3. وظائف البوت بتصميم "الإرشاد البصري" ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # زر جلب الكود بتنسيق صحيح
    keyboard = [[InlineKeyboardButton("🔗 اضغط هنا لجلب كود التفعيل", url=MY_LINK)]]
    
    # رسالة توضيحية موجهة بصرياً نحو مكان الكتابة
    welcome_text = (
        "👋 **أهلاً بك في نظام Iptv24 الذكي**\n"
        "━━━━━━━━━━━━━━\n"
        "للحصول على بيانات السيرفر المجاني:\n\n"
        "1️⃣ اضغط على الزر أدناه لجلب كود اليوم.\n"
        "2️⃣ انسخ الكود الرقمي ثم **اكتبه في المربع بالأسفل** (مكان كتابة الرسائل) وأرسله 👇\n\n"
        "📍 **اكتب الرقم هنا في الأسفل:**\n"
        "↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓"
    )
    await update.message.reply_text(
        welcome_text, 
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_activation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text
    
    # منع التكرار لضمان عدالة التوزيع
    if user_id in user_logs:
        await update.message.reply_text("❌ لقد حصلت على حسابك اليوم بالفعل! عد غداً.")
        return

    if user_text == ACTIVATION_CODE:
        user_logs[user_id] = True
        # عرض البيانات بنظام النسخ بلمسة واحدة
        success_msg = (
            "✅ **تم التحقق بنجاح! إليك سيرفرك:**\n"
            "━━━━━━━━━━━━━━\n"
            "🌐 **HOST:** `http://top.cloud-ip.cc:2052` \n"
            "👤 **USER:** `a128` \n"
            "🔑 **PASS:** `a` \n"
            "━━━━━━━━━━━━━━\n"
            "🚀 **استمتع بالمشاهدة مع Iptv24.**"
        )
        await update.message.reply_text(success_msg, parse_mode='Markdown')
    else:
        # رسالة خطأ ترشد المستخدم للمكان الصحيح مجدداً
        await update.message.reply_text("⚠️ **الرقم غير صحيح!** اكتب الكود الرقمي هنا في الأسفل 👇")

# --- 4. التشغيل النهائي المحمي من التوقف ---
if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_activation))
    
    # حل مشكلة الـ Conflict بتجاهل التحديثات القديمة
    app.run_polling(drop_pending_updates=True)
