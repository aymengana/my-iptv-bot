# -*- coding: utf-8 -*-
import requests
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن الخاص بك
BOT_TOKEN = '8312066648:AAHokvDUYpptDRQfeoSrvPaFj3LmA021RuE'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تصميم ترحيبي جذاب باستخدام البلوكات النصية
    welcome_text = (
        "🤖 **أهلاً بك في نظام التفعيل الذكي**\n"
        "━━━━━━━━━━━━━━\n"
        "📍 **للحصول على رابط الكود:**\n"
        "اضغط على: /code\n\n"
        "⚡️ **لجلب البيانات مباشرة:**\n"
        "اكتب كلمة: `تفعيل`\n"
        "━━━━━━━━━━━━━━\n"
        "💎 *نظامنا يوفر لك أكواداً فريدة (Single Connection).*"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تصميم احترافي للرابط
    link_text = (
        "🔗 **بوابة استخراج الأكواد**\n"
        "━━━━━━━━━━━━━━\n"
        "تفضل بزيارة الموقع الرسمي للحصول على كودك:\n"
        "👉 https://auziatv.com/index.php\n\n"
        "⚠️ *بعد تخطي الرابط، انسخ البيانات وضعها في تطبيقك.*"
    )
    await update.message.reply_text(link_text, parse_mode='Markdown', disable_web_page_preview=True)

async def auto_activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # رسالة انتظار احترافية
    status_msg = await update.message.reply_text("🔄 **جاري فحص السيرفرات واستخراج البيانات...**")
    
    url = "https://auziatv.com/index.php"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, timeout=15).text
        
        # استخراج البيانات الحقيقية من AuziaTV
        host_match = re.search(r'http://[a-zA-Z0-9.-]+:[0-9]+', response)
        user_match = re.search(r'Username[:\s]+([a-zA-Z0-9_-]+)', response, re.I)
        pass_match = re.search(r'Password[:\s]+([a-zA-Z0-9_-]+)', response, re.I)

        if host_match and user_match and pass_match:
            # بطاقة البيانات الاحترافية (تشبه التي في صورتك)
            res_text = (
                "🎯 **تم استخراج البيانات بنجاح!**\n"
                "━━━━━━━━━━━━━━\n"
                f"🌐 **HOST:** `{host_match.group(0)}`\n"
                f"👤 **USER:** `{user_match.group(1)}`\n"
                f"🔑 **PASS:** `{pass_match.group(1)}`\n"
                "━━━━━━━━━━━━━━\n"
                "✅ **هذا الحساب تم إنشاؤه وتخطيه آلياً.**\n"
                "📺 *يعمل الآن على تطبيق IPTV Smarters.*"
            )
            await status_msg.edit_text(res_text, parse_mode='Markdown')
        else:
            await status_msg.edit_text(
                "⚠️ **تنبيه حماية:**\n"
                "━━━━━━━━━━━━━━\n"
                "السيرفر يطلب تخطي يدوي حالياً لضمان أنك لست روبوت.\n"
                "استخدم الأمر /code للحصول على الرابط."
            )
    except:
        await status_msg.edit_text("❌ **خطأ:** السيرفر لا يستجيب حالياً.")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("code", get_link))
    app.add_handler(MessageHandler(filters.Regex('^تفعيل$'), auto_activate))
    
    # حل مشكلة التضارب نهائياً
    app.run_polling(drop_pending_updates=True)
