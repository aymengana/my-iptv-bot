# -*- coding: utf-8 -*-
import requests, re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# التوكن الخاص بـ Iptv24_Bot
BOT_TOKEN = '8312066648:AAEWpmkMX6WG-wZt9pLQkKPhbRCULoMfQXk'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # واجهة Iptv24_Bot الاحترافية بنظام الأزرار
    keyboard = [
        [InlineKeyboardButton("⚡️ استخراج كود IPTV مجاني", callback_data='gen')],
        [
            InlineKeyboardButton("📖 دليل التشغيل", callback_data='help'),
            InlineKeyboardButton("🌐 موقع الأكواد", url="https://auziatv.com/index.php")
        ],
        [InlineKeyboardButton("📢 قناة التحديثات", url="https://t.me/Iptv24_News")]
    ]
    
    await update.message.reply_text(
        "👋 **أهلاً بك في Iptv24_Bot الرسمي**\n"
        "━━━━━━━━━━━━━━\n"
        "أسرع نظام لتوليد بيانات IPTV آلياً وبدون إعلانات مزعجة.\n\n"
        "يرجى الضغط على الزر أدناه للبدء 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'gen':
        # تحديث الرسالة لمنع تراكم النصوص في المحادثة
        await query.edit_message_text("🔄 **جاري اختصار الروابط وسحب البيانات...**")
        try:
            with requests.Session() as s:
                s.headers.update({'User-Agent': 'Mozilla/5.0'})
                res = s.get("https://auziatv.com/index.php", timeout=12).text
                
                # استخراج البيانات الصافية
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
                    "✅ *اضغط على أي قيمة أعلاه لنسخها فوراً.*"
                )
                # إضافة زر للعودة بعد استلام الكود
                back_btn = [[InlineKeyboardButton("🔙 العودة للقائمة", callback_data='back')]]
                await query.edit_message_text(card, reply_markup=InlineKeyboardMarkup(back_btn), parse_mode='Markdown')
        except:
            await query.edit_message_text("❌ **عذراً!** الموقع محمي حالياً، يرجى المحاولة بعد قليل.")

    elif query.data == 'help':
        help_text = (
            "📖 **كيف تستفيد من Iptv24_Bot؟**\n\n"
            "1. اضغط على 'استخراج كود'.\n"
            "2. سيقوم البوت بتخطي الروابط نيابة عنك.\n"
            "3. انسخ البيانات وضعها في تطبيق IPTV Smarters.\n"
            "📺 مشاهدة ممتعة!"
        )
        back_btn = [[InlineKeyboardButton("🔙 العودة للقائمة", callback_data='back')]]
        await query.edit_message_text(help_text, reply_markup=InlineKeyboardMarkup(back_btn), parse_mode='Markdown')

    elif query.data == 'back':
        # العودة للواجهة الرئيسية بدون رسائل مكررة
        keyboard = [[InlineKeyboardButton("⚡️ استخراج كود IPTV مجاني", callback_data='gen')],
                    [InlineKeyboardButton("📖 دليل التشغيل", callback_data='help'),
                     InlineKeyboardButton("🌐 موقع الأكواد", url="https://auziatv.com/index.php")]]
        await query.edit_message_text("👋 **أهلاً بك في Iptv24_Bot الرسمي**\n━━━━━━━━━━━━━━\nيرجى الاختيار:", 
                                     reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    
    # ضمان عدم تضارب الرسائل أو التعليق (Conflict Fix)
    app.run_polling(drop_pending_updates=True)
