# -*- coding: utf-8 -*-
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعداداتك الثابتة
BOT_TOKEN = '8312066648:AAFHr1prjk642UaZExabW8jDr9S-lZxHsdo'
NITRO_API_KEY = '6508fa23bf8d664bb923eb5744af09860255ff93'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 البوت جاهز تماماً! أرسل البيانات هكذا `user:pass` للحصول على رابطك.")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if ":" in text:
        user, pwd = text.split(":", 1)
        m = await update.message.reply_text("⏳ جاري إنشاء واختصار الرابط...")
        
        # الرابط المباشر للسيرفر (سريع ومضمون)
        raw_link = f"http://freetv.fun:8080/get.php?username={user.strip()}&password={pwd.strip()}&type=m3u_plus&output=ts"
        
        try:
            # الاختصار عبر Nitro-link
            api_url = f"https://nitro-link.com/api?api={NITRO_API_KEY}&url={raw_link}&format=text"
            final_link = requests.get(api_url).text.strip()
            
            if "http" in final_link:
                await m.edit_text(f"✅ تم الإنشاء بنجاح!\n🔗 رابطك المختصر: {final_link}")
            else:
                await m.edit_text("❌ مشكلة في API الخاص بالاختصار، تأكد من صحته في الموقع.")
        except Exception as e:
            await m.edit_text(f"❌ حدث خطأ: {e}")
    else:
        await update.message.reply_text("⚠️ أرسل البيانات بصيغة `user:pass`")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    app.run_polling()
