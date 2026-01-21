# -*- coding: utf-8 -*-
import os, threading, random, string
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- تشغيل سيرفر الويب لمنع توقف الخدمة على Render ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Iptv24 Premium Generator is Online!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- إعدادات البوت الأساسية ---
BOT_TOKEN = '8312066648:AAEWpmkMX6WG-wZt9pLQkKPhbRCULoMfQXk'

# دالة ذكية لتوليد بيانات سيرفر احترافية
def generate_premium_data():
    hosts = ["http://v-vip.iptv24.com:8080", "http://ultra.iptv24.net:2095", "http://server-pro.iptv24.tv:80"]
    countries = ["🇩🇿 Algeria", "🇲🇦 Morocco", "🇸🇦 Saudi Arabia", "🇪🇬 Egypt", "🇫🇷 France", "🇪🇸 Spain"]
    
    # توليد يوزر وباسورد عشوائيين
    user = "vip_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    return {
        "host": random.choice(hosts),
        "user": user,
        "pass": pwd,
        "country": random.choice(countries),
        "conn": random.randint(1, 4),
        "expiry": "2026-01-22" # صلاحية لـ 24 ساعة كما في وصف البوت
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # واجهة بسيطة ومركزة
    keyboard = [[InlineKeyboardButton("⚡️ توليد سيرفر VIP حصري", callback_data='gen')]]
    welcome_text = (
        "👋 أهلاً بك في نظام Iptv24 المطور\n"
        "━━━━━━━━━━━━━━\n"
        "اضغط أدناه لاستخراج بيانات سيرفرك الخاص:"
    )
    # استخدام النص العادي لتجنب أخطاء parse entities
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # تحديث الرسالة الحالية لزيادة الواقعية
    await query.edit_message_text(text="🔍 جاري البحث عن أفضل سيرفر متاح...")
    
    # محاكاة توليد البيانات
    d = generate_premium_data()
    
    # تنسيق البطاقة الاحترافية (بدون رموز معقدة لتفادي الأخطاء)
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
    
    # تنظيف التحديثات العالقة لمنع تضارب النسخ
    app.run_polling(drop_pending_updates=True)
