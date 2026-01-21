# -*- coding: utf-8 -*-
import requests
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = '8312066648:AAFHr1prjk642UaZExabW8jDr9S-lZxHsdo'

# دالة لتخطي الرابط المختصر (مثال باستخدام API خارجي)
def bypass_link(short_url):
    try:
        # ملاحظة: سنستخدم API لتخطي الروابط (يجب التأكد من دعم الموقع المختصر)
        bypass_api = f"https://api.bypass.vip/bypass?url={short_url}"
        response = requests.get(bypass_api, timeout=15).json()
        return response.get("destination") # يعيد الرابط النهائي
    except:
        return None

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("⏳ **جاري فك تشفير الرابط واستخراج الكود...**", parse_mode='Markdown')
    
    # رابط الموقع الذي يعطي الأكواد (رابطك المختصر)
    short_url = "https://your-short-link.com/xyz" 
    
    final_url = bypass_link(short_url)
    
    if final_url:
        try:
            # الدخول للرابط النهائي وجلب محتواه
            res = requests.get(final_url, timeout=10).text
            
            # استخراج اليوزر والباسورد باستخدام Regex (البحث عن أنماط نصية)
            user = re.search(r'username=(.*?)&', res).group(1)
            pwd = re.search(r'password=(.*?)&', res).group(1)
            host = "http://moodtv.xyz:8080" # الهوست الثابت للموقع
            
            response_text = (
                "✨ **تم توليد كود فريد بنجاح!** ✨\n"
                "━━━━━━━━━━━━━━\n"
                f"🌐 **SERVER:** `{host}`\n"
                f"👤 **USER:** `{user}`\n"
                f"🔑 **PASS:** `{pwd}`\n"
                "━━━━━━━━━━━━━━\n"
                "✅ **هذا الكود خاص بك فقط ويعمل الآن.**"
            )
            await status_msg.edit_text(response_text, parse_mode='Markdown')
        except:
            await status_msg.edit_text("❌ فشل استخراج البيانات من الرابط النهائي.")
    else:
        await status_msg.edit_text("⚠️ فشل تخطي الرابط المختصر تلقائياً.")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("أرسل أي رسالة للحصول على كودك!")))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    app.run_polling()
