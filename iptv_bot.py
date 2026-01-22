# -*- coding: utf-8 -*-
import os, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- 1. سيرفر الويب لضمان استقرار Render ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Iptv24: Testing 1 Account..."

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

# --- 2. الإعدادات ---
BOT_TOKEN = '8312066648:AAHI0ncJpcHyU3-1aIMlQlO0DPbexgSDisI'
MY_LINK = "https://linkjust.com/YP7Q" 
ACTIVATION_CODE = "88220033" 

# --- 3. قائمة الحسابات (حساب وهمي واحد للتجربة) ---
# غداً ستقوم باستبدال هذا السطر بالـ 100 حساب
iptv_accounts = [
    {"user": "TEST_USER_99", "pass": "TEST_PASS_123"}
]

user_logs = {}

# --- 4. وظائف البوت الذكية ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # فحص إذا كانت الحسابات انتهت
    if len(iptv_accounts) == 0:
        await update.message.reply_text(
            "⚠️ **نعتذر، نفدت جميع الحسابات!**\nجاري توليد سيرفرات جديدة الآن...", 
            parse_mode='Markdown'
        )
        return

    keyboard = [[InlineKeyboardButton("🔗 اضغط هنا لجلب كود التفعيل", url=MY_LINK)]]
    welcome_text = (
        "👋 **أهلاً بك في تجربة نظام Iptv24**\n"
        "━━━━━━━━━━━━━━\n"
        f"📊 **الحسابات المتوفرة للتجربة:** {len(iptv_accounts)}\n\n"
        "1️⃣ احصل على الكود من الرابط.\n"
        "2️⃣ أرسله هنا في الأسفل 👇"
    )
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def handle_activation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id in user_logs:
        await update.message.reply_text("❌ لقد حصلت على حسابك التجريبي بالفعل!")
        return

    if update.message.text == ACTIVATION_CODE:
        if len(iptv_accounts) > 0:
            # سحب الحساب الوحيد وحذفه فوراً
            account = iptv_accounts.pop(0) 
            user_logs[user_id] = True
            
            success_msg = (
                "✅ **تم التحقق! إليك سيرفرك الوهمي:**\n"
                "━━━━━━━━━━━━━━\n"
                "🌐 **HOST:** `http://top.cloud-ip.cc:2052` \n"
                f"👤 **USER:** `{account['user']}` \n"
                f"🔑 **PASS:** `{account['pass']}` \n"
                "━━━━━━━━━━━━━━\n"
                "💡 **لاحظ:** الآن إذا حاولت مرة أخرى ستجد أن الحساب قد حُذف."
            )
            await update.message.reply_text(success_msg, parse_mode='Markdown')
        else:
            await update.message.reply_text("😔 نفدت الحسابات! انتظر التحديث.")
    else:
        await update.message.reply_text("⚠️ الكود خاطئ! اكتبه في الأسفل 👇")

# --- 5. التشغيل النهائي ---
if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_activation))
    app.run_polling(drop_pending_updates=True)
