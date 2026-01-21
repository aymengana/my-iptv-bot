# -*- coding: utf-8 -*-
import os, threading, random, string
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- سيرفر Port لإبقاء البوت نشطاً على Render ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Iptv24_Bot Premium is Active!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- إعدادات البوت ---
BOT_TOKEN = '8312066648:AAEWpmkMX6WG-wZt9pLQkKPhbRCULoMfQXk'

# دالة لتوليد بيانات احترافية وهمية
def generate_fake_iptv():
    hosts = ["http://v-vip.iptv24.com:8080", "http://premium.iptv24.net:2095", "http://server1.iptv24.tv:80"]
    countries = ["🇩🇿 Algeria", "🇸🇦 Saudi Arabia", "🇪🇬 Egypt", "🇲🇦 Morocco", "🇫🇷 France", "🇩🇪 Germany"]
    
    user = "vip_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    return {
        "host": random.choice(hosts),
        "user": user,
        "pass": pwd,
        "country": random.choice(countries),
        "connections": random.randint(1, 5),
        "expiry": "2026-01-22"  # صلاحية لـ 24 ساعة كما في وصفك
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # واجهة احترافية بزر واحد
    keyboard = [[InlineKeyboardButton("⚡️ توليد سيرفر VIP حصري", callback_data='gen')]]
    
    welcome_text = (
        "👋 **أهلاً بك في نظام Iptv24_Bot المطور**\n"
        "━━━━━━━━━━━━━━\n"
        "أنت الآن متصل بنظام توليد السيرفرات الخاصة.\n"
        "اضغط أدناه لاستخراج بياناتك:"
    )
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def handle_gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # رسالة انتظار احترافية لمنع التلوث البصري
    await query.edit_message_text(text="🔍 **جاري البحث عن سيرفر متاح...**")
    
    # محاكاة وقت المعالجة لزيادة الواقعية
    data = generate_fake_iptv()
    
    result_card = (
        "✅ **تم إنشاء السيرفر بنجاح!**\n"
        "━━━━━━━━━━━━━━\n"
        f"🌐 **HOST:** `{data['host']}`\n"
        f"👤 **USER:** `{data['user']}`\n"
        f"🔑 **PASS:** `{data['pass']}`\n"
        "━━━━━━━━━━━━━━\n"
        f"📍 **COUNTRY:** {data['country']}\n"
        f"👥 **MAX CONN:** {data['connections']} Devices\n"
        f"⏳ **EXPIRY:** {data['expiry']} (24H)\n"
        "━━━━━━━━━━━━━━\n"
        "🚀 *انسخ البيانات واستخدمها في مشغلك المفضل.*"
    )
    
    back_btn = [[InlineKeyboardButton("🔙 توليد سيرفر جديد", callback_data='back')]]
    await query.edit_message_text(text=result_card, reply_markup=InlineKeyboardMarkup(back_btn), parse_mode='Markdown')

async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("⚡️ توليد سيرفر VIP حصري", callback_data='gen')]]
    await query.edit_message_text(text="👋 اضغط للبدء من جديد:", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_gen, pattern='gen'))
    app.add_handler(CallbackQueryHandler(handle_back, pattern='back'))
    
    # حل مشكلة التحديثات العالقة في سجلات Render
    app.run_polling(drop_pending_updates=True)
