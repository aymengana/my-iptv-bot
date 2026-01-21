# -*- coding: utf-8 -*-
import os, threading, requests, re
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- سيرفر Port لإرضاء Render ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Iptv24_Bot is Active!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- إعدادات البوت ---
BOT_TOKEN = '8312066648:AAEWpmkMX6WG-wZt9pLQkKPhbRCULoMfQXk'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تم إبقاء زر واحد فقط كما طلبت
    keyboard = [[InlineKeyboardButton("⚡️ توليد حساب IPTV مجاني", callback_data='gen')]]
    
    welcome_text = (
        "👋 أهلاً بك في Iptv24_Bot\n"
        "━━━━━━━━━━━━━━\n"
        "اضغط على الزر أدناه للحصول على بياناتك فوراً:"
    )
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # تحديث النص أثناء الجلب لمنع تكرار الرسائل
    await query.edit_message_text(text="🔄 جاري استخراج البيانات... يرجى الانتظار.")
    
    try:
        res = requests.get("https://auziatv.com/index.php", timeout=12).text
        host = re.search(r'http://[a-zA-Z0-9.-]+:[0-9]+', res).group(0)
        user = re.search(r'Username[:\s]+([a-zA-Z0-9_-]+)', res, re.I).group(1)
        pwd = re.search(r'Password[:\s]+([a-zA-Z0-9_-]+)', res, re.I).group(1)

        result_card = (
            "🚀 بيانات حسابك جاهزة الآن:\n\n"
            f"🌐 SERVER: {host}\n"
            f"👤 USER: {user}\n"
            f"🔑 PASS: {pwd}\n\n"
            "✅ انسخ البيانات واستمتع بالمشاهدة."
        )
        # إضافة زر للعودة إذا أراد المستخدم توليد كود آخر
        back_btn = [[InlineKeyboardButton("🔙 العودة لتوليد كود آخر", callback_data='back')]]
        await query.edit_message_text(text=result_card, reply_markup=InlineKeyboardMarkup(back_btn))
    except:
        await query.edit_message_text(text="❌ عذراً، فشل الاتصال بالسيرفر. حاول مرة أخرى.")

async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("⚡️ توليد حساب IPTV مجاني", callback_data='gen')]]
    await query.edit_message_text(text="👋 اضغط على الزر بالأسفل لتوليد كود جديد:", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_gen, pattern='gen'))
    app.add_handler(CallbackQueryHandler(handle_back, pattern='back'))
    
    # تنظيف التحديثات العالقة لمنع تضارب النسخ
    app.run_polling(drop_pending_updates=True)
