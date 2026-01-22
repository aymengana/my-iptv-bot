# -*- coding: utf-8 -*-
import os, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- 1. سيرفر الويب لضمان استقرار الخدمة على Render ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Iptv24 System is Online!"

def run_flask():
    # استخدام المنفذ 10000 كما هو محدد في سجلات Render الخاصة بك
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

# --- 2. الإعدادات (التوكن الجديد والبيانات) ---
# تم وضع التوكن الجديد الذي أرسلته هنا لضمان التفعيل
BOT_TOKEN = '8312066648:AAHI0ncJpcHyU3-1aIMlQlO0DPbexgSDisI'
MY_LINK = "https://linkjust.com/YP7Q" 
ACTIVATION_CODE = "88220033" 
user_logs = {}

# --- 3. وظائف البوت بتصميم "الإرشاد البصري" ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # زر جلب الكود بتنسيق سليم
    keyboard = [[InlineKeyboardButton("🔗 اضغط هنا لجلب كود التفعيل", url=MY_LINK)]]
    
    # رسالة توضيحية موجهة بصرياً نحو مكان الكتابة بالأسفل
    welcome_text = (
        "👋 **أهلاً بك في نظام Iptv24 الذكي**\n"
        "━━━━━━━━━━━━━━\n"
        "للحصول على بيانات السيرفر المجاني:\n\n"
        "1️⃣ اضغط على الزر أدناه لجلب كود اليوم.\n"
        "2️⃣ بعد الحصول على الكود، **اكتبه في المربع بالأسفل** (خانة الرسائل) ثم أرسله 👇\n\n"
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
    
    if user_id in user_logs:
        await update.message.reply_text("❌ لقد حصلت على حسابك اليوم بالفعل!")
        return

    if user_text == ACTIVATION_CODE:
        user_logs[user_id] = True
        success_msg = (
            "✅ **تم التحقق بنجاح! إليك سيرفرك:**\n"
            "━━━━━━━━━━━━━━\n"
            "🌐 **HOST:** `http://top.cloud-ip.cc:2052` \n"
            "👤 **USER:** `a128` \n"
            "🔑 **PASS:** `a` \n"
            "━━━━━━━━━━━━━━\n"
            "🚀 **انسخ البيانات واستمتع بالمشاهدة.**"
        )
        await update.message.reply_text(success_msg, parse_mode='Markdown')
    else:
        # توجيه المستخدم للمكان الصحيح مجدداً في حال الخطأ
        await update.message.reply_text("⚠️ **الرقم غير صحيح!** اكتب الكود الرقمي في الأسفل 👇")

# --- 4. التشغيل النهائي المحمي من التوقف ---
if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_activation))
    
    # حل مشكلة الـ Conflict بتجاهل التحديثات القديمة وطرد الجلسات المتداخلة
    app.run_polling(drop_pending_updates=True)
