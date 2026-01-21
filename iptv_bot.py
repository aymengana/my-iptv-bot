# -*- coding: utf-8 -*-
import requests
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# التوكن الجديد الخاص بك (تأكد أنه هو المستخدم حالياً)
BOT_TOKEN = '8312066648:AAEHJLLZVic_VkPDn5tkOHtkxu_aRT4CGcM'

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("📡 **جاري الاتصال بسيرفر AuziaTV واستخراج بياناتك...**", parse_mode='Markdown')
    
    # رابط الموقع الجديد
    url = "https://auziatv.com/index.php"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    try:
        # محاولة جلب محتوى الصفحة
        response = requests.get(url, headers=headers, timeout=15).text
        
        # 🔍 البحث عن البيانات بنمط (Regex) دقيق لموقع Auzia
        # سنبحث عن كلمات مثل Server, Username, Password
        host_search = re.search(r'(http://[^\s<>"]+:[0-9]+)', response)
        user_search = re.search(r'Username[:\s]+([a-zA-Z0-9_-]+)', response, re.I)
        pass_search = re.search(r'Password[:\s]+([a-zA-Z0-9_-]+)', response, re.I)

        if host_search and user_search and pass_search:
            h = host_search.group(1)
            u = user_search.group(1)
            p = pass_search.group(1)
            
            response_text = (
                "🚀 **تم استخراج حساب AuziaTV بنجاح!**\n"
                "━━━━━━━━━━━━━━\n"
                f"🌐 **HOST:** `{h}`\n"
                f"👤 **USER:** `{u}`\n"
                f"🔑 **PASS:** `{p}`\n"
                "━━━━━━━━━━━━━━\n"
                "✅ **هذا الكود يعمل الآن وبشكل فريد.**\n"
                "📺 *مشاهدة ممتعة على IPTV Smarters.*"
            )
            await status_msg.edit_text(response_text, parse_mode='Markdown')
        else:
            # إذا كانت البيانات مخفية خلف اختصار روابط، نعطي المستخدم الرابط المباشر
            error_text = (
                "⚠️ **تنبيه:** الموقع يتطلب تخطي رابط مختصر للحصول على الكود.\n\n"
                f"👉 [اضغط هنا للحصول على كودك من AuziaTV]({url})\n\n"
                "قم بتخطي الرابط ثم انسخ البيانات وضعها في تطبيقك."
            )
            await status_msg.edit_text(error_text, parse_mode='Markdown', disable_web_page_preview=True)
            
    except Exception as e:
        await status_msg.edit_text("❌ حدث خطأ في الاتصال بموقع AuziaTV.")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    # تنظيف التحديثات القديمة لمنع تكرار الرسائل
    app.run_polling(drop_pending_updates=True)
