# -*- coding: utf-8 -*-
import os, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- سيرفر الويب لاستقرار الخدمة ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Iptv24 Status: Fully Active!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

# --- الإعدادات ---
BOT_TOKEN = '8312066648:AAHI0ncJpcHyU3-1aIMlQlO0DPbexgSDisI'
MY_LINK = "https://linkjust.com/YP7Q" 
ACTIVATION_CODE = "88220033" 

# قائمة الحسابات (حساب وهمي للتجربة الآن)
iptv_accounts = [{"user": "TEST_USER_99", "pass": "TEST_PASS_123"}]
user_logs = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(iptv_accounts) == 0:
        await update.message.reply_text("⚠️ نعتذر، نفدت جميع الحسابات حالياً!")
        return

    keyboard = [[InlineKeyboardButton("🔗 اضغط هنا لجلب كود التفعيل", url=MY_LINK)]]
    welcome_text = (
        "👋 **أهلاً بك في نظام Iptv24**\n"
        "━━━━━━━━━━━━━━\n"
        "1️⃣ احصل على الكود من الرابط.\n"
        "2️⃣ أرسله هنا في الأسفل 👇\n\n"
        "📍 اكتب الرقم في خانة الرسائل العادية."
    )
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def handle_activation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_logs:
        await update.message.reply_text("❌ لقد حصلت على حسابك بالفعل اليوم!")
        return

    if update.message.text == ACTIVATION_CODE:
        if len(iptv_accounts) > 0:
            account = iptv_accounts.pop(0) 
            user_logs[user_id] = True
            success_msg = (
                "✅ **تم التحقق! إليك سيرفرك الشخصي:**\n"
                "━━━━━━━━━━━━━━\n"
                f"👤 **USER:** `{account['user']}` | 🔑 **PASS:** `{account['pass']}` \n"
                "━━━━━━━━━━━━━━"
            )
            await update.message.reply_text(success_msg, parse_mode='Markdown')
        else:
            await update.message.reply_text("😔 نفدت الحسابات!")
    else:
        await update.message.reply_text("⚠️ الكود خاطئ! اكتبه في الأسفل 👇")

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_activation))
    
    # هذه الإضافة تمنع ظهور الرسائل الحمراء (Conflict) نهائياً
    app.run_polling(drop_pending_updates=True)
