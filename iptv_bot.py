# -*- coding: utf-8 -*-
import requests, re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# التوكن الخاص بك
BOT_TOKEN = '8312066648:AAEWpmkMX6WG-wZt9pLQkKPhbRCULoMfQXk'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تصميم الأزرار (البُطونات) تحت اسم البوت الجديد
    keyboard = [
        [InlineKeyboardButton("⚡️ توليد كود IPTV جديد", callback_data='gen')],
        [
            InlineKeyboardButton("📖 طريقة الاستخدام", callback_data='help'),
            InlineKeyboardButton("🌐 موقعنا الرسمي", url="https://auziatv.com/index.php")
        ],
        [InlineKeyboardButton("📢 قناة التحديثات", url="https://t.me/YourNewChannel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # رسالة الترحيب بالاسم الجديد
    await update.message.reply_text(
        "👋 **مرحباً بك في بوتك الاحترافي**\n"
        "━━━━━━━━━━━━━━\n"
        "أهلاً بك في الواجهة الجديدة. يرجى اختيار ما تريد القيام به:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'gen':
        # تحديث نفس الرسالة يمنع تكرار النصوص
        await query.edit_message_text("🔄 **جاري استخراج البيانات من أجلك...**")
        try:
            with requests.Session() as s:
                res = s.get("https://auziatv.com/index.php", timeout=10).text
                host = re.search(r'http://[a-zA-Z0-9.-]+:[0-9]+', res).group(0)
                user = re.search(r'Username[:\s]+([a-zA-Z0-9_-]+)', res, re.I).group(1)
                pwd = re.search(r'Password[:\s]+([a-zA-Z0-9_-]+)', res, re.I).group(1)

                card = (
                    "🎯 **بيانات حسابك جاهزة الآن:**\n"
                    "━━━━━━━━━━━━━━\n"
                    f"🌐 **HOST:** `{host}`\n"
                    f"👤 **USER:** `{user}`\n"
                    f"🔑 **PASS:** `{pwd}`\n"
                    "━━━━━━━━━━━━━━\n"
                    "✅ *اضغط على البيانات أعلاه لنسخها فوراً.*"
                )
                await query.edit_message_text(card, parse_mode='Markdown')
        except:
            await query.edit_message_text("❌ حدث خطأ في الموقع الأصلي، يرجى المحاولة لاحقاً.")

    elif query.data == 'help':
        # رسالة المساعدة داخل البوت
        help_text = (
            "📖 **دليل الاستخدام السريع:**\n"
            "1️⃣ اضغط على زر 'توليد كود'.\n"
            "2️⃣ انسخ البيانات التي ستظهر لك.\n"
            "3️⃣ ضعها في تطبيق IPTV المفضل لديك.\n"
            "✨ مشاهدة ممتعة!"
        )
        back_button = [[InlineKeyboardButton("🔙 العودة للقائمة", callback_data='back')]]
        await query.edit_message_text(help_text, reply_markup=InlineKeyboardMarkup(back_button))

    elif query.data == 'back':
        # العودة للقائمة الرئيسية بنفس الرسالة
        await start_back(query)

async def start_back(query):
    keyboard = [
        [InlineKeyboardButton("⚡️ توليد كود IPTV جديد", callback_data='gen')],
        [InlineKeyboardButton("📖 طريقة الاستخدام", callback_data='help'),
         InlineKeyboardButton("🌐 موقعنا الرسمي", url="https://auziatv.com/index.php")]
    ]
    await query.edit_message_text(
        "👋 **مرحباً بك في بوتك الاحترافي**\n━━━━━━━━━━━━━━\nيرجى الاختيار:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    
    # حل مشكلة الـ Conflict التي ظهرت في سجلاتك
    app.run_polling(drop_pending_updates=True)
