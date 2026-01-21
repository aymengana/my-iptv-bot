# -*- coding: utf-8 -*-
import requests
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن الخاص بك
BOT_TOKEN = '8312066648:AAHokvDUYpptDRQfeoSrvPaFj3LmA021RuE'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # واجهة نظيفة جداً بأزرار
    keyboard = [[InlineKeyboardButton("⚡️ تفعيل الحساب آلياً", callback_data='activate')],
                [InlineKeyboardButton("🔗 رابط الكود اليدوي", url="https://auziatv.com/index.php")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 **أهلاً بك في بوت Mix TV الجديد**\n\n"
        "يرجى اختيار الخدمة المطلوبة من الأزرار أدناه 👇",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_activation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # هذه الدالة ستعمل عند كتابة "تفعيل" أو الضغط على الزر
    status_msg = await update.message.reply_text("🔄 **جاري المعالجة الذكية...**")
    
    try:
        # محاولة التخطي والاستخراج الصامت
        response = requests.get("https://auziatv.com/index.php", timeout=15).text
        
        # استخراج البيانات الحقيقية
        host = re.search(r'http://[a-zA-Z0-9.-]+:[0-9]+', response).group(0)
        user = re.search(r'Username[:\s]+([a-zA-Z0-9_-]+)', response, re.I).group(1)
        pwd = re.search(r'Password[:\s]+([a-zA-Z0-9_-]+)', response, re.I).group(1)

        # عرض البيانات في بطاقة VIP نظيفة جداً
        card = (
            "💎 **بيانات اشتراكك جاهزة**\n"
            "╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼\n"
            f"🌐 **HOST:** `{host}`\n"
            f"👤 **USER:** `{user}`\n"
            f"🔑 **PASS:** `{pwd}`\n"
            "╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼\n"
            "✨ *اضغط على أي قيمة لنسخها فوراً.*"
        )
        await status_msg.edit_text(card, parse_mode='Markdown')
    except:
        await status_msg.edit_text("❌ **عذراً!** الحماية حالياً مرتفعة، يرجى استخدام الرابط اليدوي.")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex('^تفعيل$'), handle_activation))
    app.run_polling(drop_pending_updates=True) # لإنهاء تضارب Logs
