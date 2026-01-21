# -*- coding: utf-8 -*-
import requests
import re
import random
import string
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# التوكن الأخير الذي يعمل
BOT_TOKEN = '8312066648:AAHokvDUYpptDRQfeoSrvPaFj3LmA021RuE'

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("📡 **جاري الاتصال بسيرفر AuziaTV الحقيقي...**", parse_mode='Markdown')
    
    # رابط موقع AuziaTV
    target_url = "https://auziatv.com/index.php"
    
    try:
        # محاكاة تصفح حقيقي لجلب البيانات الصافية
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(target_url, headers=headers, timeout=15).text
        
        # 🔍 البحث عن الهوست واليوزر والباسورد داخل صفحة AuziaTV حصراً
        # نبحث عن نمط http://...:8080 أو أي بورت آخر
        host_match = re.search(r'http://[a-zA-Z0-9.-]+:[0-9]+', response)
        user_match = re.search(r'Username[:\s]+([a-zA-Z0-9_-]+)', response, re.I)
        pass_match = re.search(r'Password[:\s]+([a-zA-Z0-9_-]+)', response, re.I)

        if host_match and user_match and pass_match:
            final_host = host_match.group(0)
            final_user = user_match.group(1)
            final_pass = pass_match.group(1)
            
            response_text = (
                "🎯 **تم استخراج بيانات AuziaTV بنجاح!**\n"
                "━━━━━━━━━━━━━━\n"
                f"🌐 **HOST:** `{final_host}`\n"
                f"👤 **USER:** `{final_user}`\n"
                f"🔑 **PASS:** `{final_pass}`\n"
                "━━━━━━━━━━━━━━\n"
                "✅ **هذا الكود حقيقي ومستخرج الآن.**\n"
                "📺 *مشاهدة ممتعة!*"
            )
            await status_msg.edit_text(response_text, parse_mode='Markdown')
        else:
            # إذا لم يجد الكود تلقائياً بسبب اختصار الروابط
            await status_msg.edit_text(
                f"⚠️ **الموقع يتطلب تخطي يدوي حالياً.**\n\n"
                f"ادخل هنا واحصل على الكود:\n{target_url}",
                disable_web_page_preview=True
            )

    except Exception as e:
        await status_msg.edit_text("❌ فشل الاتصال بسيرفر AuziaTV.")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    
    # ⚠️ أهم سطر لحل مشكلة السجلات التي أرسلتها (Conflict)
    app.run_polling(drop_pending_updates=True)
