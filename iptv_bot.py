# -*- coding: utf-8 -*-
import requests, re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# التوكن الخاص بك
BOT_TOKEN = '8312066648:AAEWpmkMX6WG-wZt9pLQkKPhbRCULoMfQXk'

# رابط الصورة التي اخترتها (ضع الرابط المباشر للصورة هنا)
PHOTO_URL = 'https://telegra.ph/file/your_image_link.jpg' 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تصميم الأزرار الاحترافية
    keyboard = [
        [InlineKeyboardButton("⚡️ استخراج كود IPTV", callback_data='gen')],
        [
            InlineKeyboardButton("📖 دليل التشغيل", callback_data='help'),
            InlineKeyboardButton("🌐 موقع الأكواد", url="https://auziatv.com/index.php")
        ],
        [InlineKeyboardButton("📢 قناة التحديثات", url="https://t.me/Iptv24_News")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # إرسال الصورة مع رسالة ترحيبية بالهوية الجديدة
    welcome_text = (
        "👋 **أهلاً بك في Iptv24_Bot الرسمي**\n"
        "━━━━━━━━━━━━━━\n"
        "أسرع نظام لتوليد بيانات IPTV آلياً وباحترافية عالية.\n"
        "اضغط على الزر أدناه للحصول على حسابك 👇"
    )
    
    # محاولة إرسال الصورة، وإذا فشل يرسل نصاً فقط
    try:
        await update.message.reply_photo(photo=PHOTO_URL, caption=welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    except:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'gen':
        # تحديث النص يمنع التلوث البصري
        await query.edit_message_caption(caption="🔄 **جاري تخطي الروابط وسحب البيانات...**", parse_mode='Markdown')
        try:
            with requests.Session() as s:
                res = s.get("https://auziatv.com/index.php", timeout=12).text
                host = re.search(r'http://[a-zA-Z0-9.-]+:[0-9]+', res).group(0)
                user = re.search(r'Username[:\s]+([a-zA-Z0-9_-]+)', res, re.I).group(1)
                pwd = re.search(r'Password[:\s]+([a-zA-Z0-9_-]+)', res, re.I).group(1)

                card = (
                    "🚀 **بيانات حسابك في Iptv24_Bot:**\n"
                    "━━━━━━━━━━━━━━\n"
                    f"🌐 **HOST:** `{host}`\n"
                    f"👤 **USER:** `{user}`\n"
                    f"🔑 **PASS:** `{pwd}`\n"
                    "━━━━━━━━━━━━━━\n"
                    "✅ *اضغط على القيم لنسخها فوراً.*"
                )
                back_btn = [[InlineKeyboardButton("🔙 العودة للقائمة", callback_data='back')]]
                await query.edit_message_caption(caption=card, reply_markup=InlineKeyboardMarkup(back_btn), parse_mode='Markdown')
        except:
            await query.edit_message_caption(caption="❌ **خطأ!** الموقع محمي حالياً، حاول مجدداً.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back')]]))

    elif query.data == 'help':
        help_text = (
            "📖 **دليل Iptv24_Bot:**\n"
            "1️⃣ اضغط استخراج كود.\n"
            "2️⃣ سيقوم البوت بالتخطي الآلي.\n"
            "3️⃣ انسخ البيانات واستمتع بالمشاهدة!"
        )
        back_btn = [[InlineKeyboardButton("🔙 العودة للقائمة", callback_data='back')]]
        await query.edit_message_caption(caption=help_text, reply_markup=InlineKeyboardMarkup(back_btn), parse_mode='Markdown')

    elif query.data == 'back':
        # العودة للقائمة الرئيسية
        keyboard = [[InlineKeyboardButton("⚡️ استخراج كود IPTV", callback_data='gen')],
                    [InlineKeyboardButton("📖 دليل التشغيل", callback_data='help')]]
        await query.edit_message_caption(caption="👋 **قائمة Iptv24_Bot الرئيسية:**", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    
    # حل مشكلة التضارب (Conflict) نهائياً
    app.run_polling(drop_pending_updates=True)
