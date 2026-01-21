# -*- coding: utf-8 -*-
import requests
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# التوكن الخاص بك
BOT_TOKEN = '8312066648:AAHokvDUYpptDRQfeoSrvPaFj3LmA021RuE'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # واجهة نظيفة جداً كأنها تطبيق
    keyboard = [
        [InlineKeyboardButton("⚡️ توليد حساب جديد", callback_data='gen')],
        [InlineKeyboardButton("🔗 رابط الموقع الرسمي", url="https://auziatv.com/index.php")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "💎 **أهلاً بك في MIX-TV PREMIUM**\n"
        "╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼\n"
        "الرجاء الضغط على الزر أدناه لبدء التفعيل الآلي.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'gen':
        await query.edit_message_text("🔄 **جاري اختصار الروابط وسحب البيانات...**")
        
        try:
            # محاكاة التخطي الصامت للموقع
            res = requests.get("https://auziatv.com/index.php", timeout=15).text
            host = re.search(r'http://[a-zA-Z0-9.-]+:[0-9]+', res).group(0)
            user = re.search(r'Username[:\s]+([a-zA-Z0-9_-]+)', res, re.I).group(1)
            pwd = re.search(r'Password[:\s]+([a-zA-Z0-9_-]+)', res, re.I).group(1)

            # بطاقة البيانات الأنيقة
            card = (
                "🚀 **تم استخراج الحساب بنجاح**\n"
                "╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼\n"
                f"🌐 **HOST:** `{host}`\n"
                f"👤 **USER:** `{user}`\n"
                f"🔑 **PASS:** `{pwd}`\n"
                "╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼\n"
                "✅ *انقر على أي قيمة لنسخها فوراً.*"
            )
            await query.edit_message_text(card, parse_mode='Markdown')
        except:
            await query.edit_message_text("❌ **فشل التخطي الآلي حالياً.**\nيرجى استخدام الرابط اليدوي من القائمة.")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # قتل أي جلسات قديمة لمنع التضارب
    app.run_polling(drop_pending_updates=True)
