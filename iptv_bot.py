# -*- coding: utf-8 -*-
import os, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- 1. سيرفر الويب لضمان استقرار الخدمة في Render ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Iptv24 System is Online!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

# --- 2. الإعدادات ---
BOT_TOKEN = '8312066648:AAGK2oDn870CtWxpJNxFlgGP8r5gRTYCio8'
MY_LINK = "https://linkjust.com/YP7Q" 
ACTIVATION_CODE = "88220033" 
user_logs = {}

# --- 3. وظائف البوت بتصميم جديد ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تصميم الأزرار بشكل احترافي
    keyboard = [[InlineKeyboardButton("🔗 اضغط هنا لجلب كود التفعيل", url=MY_LINK)]]
    
    # رسالة ترحيبية بتصميم المربعات الاحترافي
    welcome_text = (
        "👋 **أهلاً بك في نظام Iptv24 الذكي**\n"
        "━━━━━━━━━━━━━━\n"
        "للحصول على بيانات سيرفرك المجاني لمدة 24 ساعة، يرجى اتباع الخطوات:\n\n"
        "1️⃣ **أولاً:** اذهب للرابط أدناه واختصره لجلب الكود.\n"
        "2️⃣ **ثانياً:** ضع الكود في المربع أدناه وأرسله 👇\n\n"
        "╔════════════════╗\n"
        "   📥 **قـم بإدخـال الـكـود هـنـا**\n"
        "╚════════════════╝\n"
        "━━━━━━━━━━━━━━"
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
        await update.message.reply_text("❌ عذراً! لقد حصلت على حسابك اليوم بالفعل.")
        return

    if user_text == ACTIVATION_CODE:
        user_logs[user_id] = True
        # تصميم بطاقة البيانات بنسخ بلمسة واحدة
        success_msg = (
            "✅ **تم التحقق! إليك بيانات سيرفرك الحصري:**\n"
            "━━━━━━━━━━━━━━\n"
            "🌐 **HOST:** `http://top.cloud-ip.cc:2052` \n"
            "👤 **USER:** `a128` \n"
            "🔑 **PASS:** `a` \n"
            "━━━━━━━━━━━━━━\n"
            "🚀 **انسخ البيانات واستمتع بالمشاهدة الآن.**"
        )
        await update.message.reply_text(success_msg, parse_mode='Markdown')
    else:
        # رسالة خطأ احترافية
        error_msg = (
            "⚠️ **عذراً، الكود الذي أدخلته غير صحيح!**\n"
            "تأكد من جلب الكود الرقمي من الرابط المذكور أعلاه."
        )
        await update.message.reply_text(error_msg, parse_mode='Markdown')

# --- 4. التشغيل النهائي ---
if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_activation))
    
    # تنظيف التحديثات العالقة لمنع الـ Conflict
    app.run_polling(drop_pending_updates=True)
