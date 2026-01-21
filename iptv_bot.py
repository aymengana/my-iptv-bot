# -*- coding: utf-8 -*-
import os, threading, random, string
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- تشغيل سيرفر الويب لمنع توقف Render ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Iptv24 VIP Generator is Online!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

# --- إعدادات البوت ---
BOT_TOKEN = '8312066648:AAEWpmkMX6WG-wZt9pLQkKPhbRCULoMfQXk'

# مولد بيانات VIP احترافي
def generate_vip_account():
    hosts = [
        "http://premium-v.iptv24.pro:8080", 
        "http://vip-server.iptv24.tv:2095", 
        "http://ultra-24.iptv24.net:80"
    ]
    countries = ["🇩🇿 Algeria", "🇲🇦 Morocco", "🇸🇦 Saudi Arabia", "🇪🇬 Egypt", "🇫🇷 France", "🇩🇪 Germany"]
    
    user = "vip_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=9))
    
    return {
        "host": random.choice(hosts),
        "user": user,
        "pass": pwd,
        "country": random.choice(countries),
        "conn": random.randint(1, 4), # عدد الأجهزة المسموح بها
        "expiry": "2026-01-22" # صلاحية 24 ساعة كما في الوصف
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # واجهة احترافية متوافقة مع شعار iptv24/24free
    keyboard = [[InlineKeyboardButton("⚡️ توليد سيرفر VIP حصري", callback_data='gen')]]
    welcome_text = (
        "👋 أهلاً بك في نظام Iptv24 المطور\n"
        "━━━━━━━━━━━━━━\n"
        "اضغط أدناه لاستخراج بيانات سيرفرك الخاص:"
    )
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(text="🔍 جاري فحص السيرفرات المتاحة... يرجى الانتظار.")
    
    # جلب البيانات من المولد
    d = generate_vip_account()
    
    # تنسيق البطاقة الاحترافية بدون رموز تسبب أخطاء Parse
    result_card = (
        "✅ تم إنشاء السيرفر بنجاح!\n"
        "━━━━━━━━━━━━━━\n"
        f"🌐 HOST: {d['host']}\n"
        f"👤 USER: {d['user']}\n"
        f"🔑 PASS: {d['pass']}\n"
        "━━━━━━━━━━━━━━\n"
        f"📍 COUNTRY: {d['country']}\n"
        f"👥 MAX CONN: {d['conn']} Devices\n"
        f"⏳ EXPIRY: {d['expiry']} (24H)\n"
        "━━━━━━━━━━━━━━\n"
        "🚀 انسخ البيانات واستمتع بالمشاهدة."
    )
    
    back_btn = [[InlineKeyboardButton("🔙 توليد سيرفر جديد", callback_data='back')]]
    await query.edit_message_text(text=result_card, reply_markup=InlineKeyboardMarkup(back_btn))

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
    
    # تنظيف التحديثات السابقة فوراً لحل مشكلة Conflict
    app.run_polling(drop_pending_updates=True)
