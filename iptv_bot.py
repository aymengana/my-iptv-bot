# -*- coding: utf-8 -*-
import requests, re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# التوكن الجديد الذي أرسلته
BOT_TOKEN = '8312066648:AAEWpmkMX6WG-wZt9pLQkKPhbRCULoMfQXk'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # واجهة تطبيق نظيفة جداً بأزرار شفافة
    keyboard = [[InlineKeyboardButton("⚡️ توليد حساب MIX-TV آلياً", callback_data='gen')]]
    
    await update.message.reply_text(
        "💎 **نظام التفعيل الذكي لـ Mix TV**\n"
        "╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼\n"
        "مرحباً بك. اضغط على الزر أدناه للحصول على بياناتك فوراً.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # تحديث نفس الرسالة يمنع التلوث البصري تماماً
    await query.edit_message_text("🔄 **جاري اختصار الروابط وسحب البيانات...**")
    
    try:
        # عملية سحب بيانات AuziaTV الحقيقية
        with requests.Session() as s:
            res = s.get("https://auziatv.com/index.php", timeout=12).text
            host = re.search(r'http://[a-zA-Z0-9.-]+:[0-9]+', res).group(0)
            user = re.search(r'Username[:\s]+([a-zA-Z0-9_-]+)', res, re.I).group(1)
            pwd = re.search(r'Password[:\s]+([a-zA-Z0-9_-]+)', res, re.I).group(1)

            # بطاقة VIP منظمة وسهلة النسخ
            card = (
                "🎯 **تم تجهيز الحساب بنجاح**\n"
                "╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼\n"
                f"🌐 **HOST:** `{host}`\n"
                f"👤 **USER:** `{user}`\n"
                f"🔑 **PASS:** `{pwd}`\n"
                "╼╼╼╼╼╼╼╼╼╼╼╼╼╼╼\n"
                "✅ *انقر على أي قيمة لنسخها فوراً.*"
            )
            await query.edit_message_text(card, parse_mode='Markdown')
    except:
        await query.edit_message_text("❌ **فشل التخطي!** السيرفر محمي حالياً، يرجى استخدام الرابط اليدوي أو المحاولة لاحقاً.")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_gen))
    
    # أهم سطر لمنع "التضارب" المجاني وتوفير الموارد
    app.run_polling(drop_pending_updates=True)
