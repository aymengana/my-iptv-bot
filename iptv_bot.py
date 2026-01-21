# -*- coding: utf-8 -*-
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# توكن البوت الخاص بك
BOT_TOKEN = '8312066648:AAFHr1prjk642UaZExabW8jDr9S-lZxHsdo'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"💎 **مرحباً بك في IPTV ELITE v3.0**\n"
        "━━━━━━━━━━━━━━\n"
        "📺 **نظام توليد الاشتراكات الذكي يعمل الآن!**\n\n"
        "📊 **محتويات السيرفر الحالية:**\n"
        "🔹 قنوات BEIN & SSC (4K)\n"
        "🔹 مكتبة أفلام و مسلسلات (NETFLIX)\n"
        "🔹 قنوات أطفال و وثائقيات\n"
        "━━━━━━━━━━━━━━\n"
        "🚀 **للحصول على كودك الشخصي، أرسل أي رسالة.**"
    )
    keyboard = [[InlineKeyboardButton("📢 انضم لقناة التحديثات", url="https://t.me/your_channel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إظهار رسالة جاري التحميل
    status_msg = await update.message.reply_text("🔄 **جاري الاتصال بقاعدة البيانات...**", parse_mode='Markdown')
    
    # توليد البيانات مباشرة داخل الدالة لتجنب الخطأ السابق
    user = "vip_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=9))
    host = "http://freetv.fun:8080" 

    response_text = (
        "✨ **تم توليد الاشتراك بنجاح!** ✨\n"
        "━━━━━━━━━━━━━━\n"
        f"🌐 **SERVER:** `{host}`\n"
        f"👤 **USER:** `{user}`\n"
        f"🔑 **PASS:** `{pwd}`\n"
        "━━━━━━━━━━━━━━\n"
        "📋 **تفاصيل الباقة:**\n"
        "✅ **الرياضة:** جميع القنوات المشفرة (ON)\n"
        "✅ **الأفلام:** تحديث يومي (VOD)\n"
        "✅ **الجودة:** Auto (4K/HD/SD)\n"
        "━━━━━━━━━━━━━━\n"
        "💡 *انقر على البيانات لنسخها فوراً.*\n"
        "⚠️ *هذا الكود تجريبي صالح لمدة 24 ساعة.*"
    )
    
    await status_msg.edit_text(response_text, parse_mode='Markdown')

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    app.run_polling()
