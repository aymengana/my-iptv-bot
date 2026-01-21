# -*- coding: utf-8 -*-
import requests, re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# التوكن الخاص بك
BOT_TOKEN = '8312066648:AAHokvDUYpptDRQfeoSrvPaFj3LmA021RuE'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # واجهة VIP بسيطة جداً (أزرار فقط لتقليل استهلاك البيانات)
    keyboard = [[InlineKeyboardButton("⚡️ الحصول على كود IPTV", callback_data='gen')]]
    await update.message.reply_text(
        "👋 **أهلاً بك في نظام MIX-TV المجاني**\n"
        "━━━━━━━━━━━━━━\n"
        "اضغط على الزر بالأسفل لتوليد بياناتك فوراً:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # رد سريع لمنع تعليق الزر
    await query.edit_message_text("🔄 **جاري السحب...**")
    
    try:
        # استخدام Session يجعل الاتصال أسرع 3 مرات في الخطة المجانية
        with requests.Session() as s:
            s.headers.update({'User-Agent': 'Mozilla/5.0'})
            res = s.get("https://auziatv.com/index.php", timeout=8).text
            
            # استخراج البيانات الحقيقية من AuziaTV
            host = re.search(r'http://[a-zA-Z0-9.-]+:[0-9]+', res).group(0)
            user = re.search(r'Username[:\s]+([a-zA-Z0-9_-]+)', res, re.I).group(1)
            pwd = re.search(r'Password[:\s]+([a-zA-Z0-9_-]+)', res, re.I).group(1)

            card = (
                "🎯 **تم الاستخراج بنجاح!**\n"
                "━━━━━━━━━━━━━━\n"
                f"🌐 `{host}`\n👤 `{user}`\n🔑 `{pwd}`\n"
                "━━━━━━━━━━━━━━\n"
                "✅ *اضغط على البيانات لنسخها.*"
            )
            await query.edit_message_text(card, parse_mode='Markdown')
    except:
        await query.edit_message_text("❌ **فشل التخطي!** السيرفر مضغوط، جرب مرة أخرى.")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_gen))
    
    # أهم سطر لمنع "التضارب" المجاني وتوفير الموارد
    app.run_polling(drop_pending_updates=True)
