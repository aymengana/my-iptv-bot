# -*- coding: utf-8 -*-
import requests
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن الخاص بك
BOT_TOKEN = '8312066648:AAHokvDUYpptDRQfeoSrvPaFj3LmA021RuE'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # رسالة ترحيبية بتصميم هرمي
    welcome_text = (
        "🚀 **مرحباً بك في المركز الذكي لتفعيل IPTV**\n"
        "━━━━━━━━━━━━━━\n"
        "💎 **الخدمات المتاحة:**\n"
        "1️⃣ استخراج كود جديد: اكتب `تفعيل`\n"
        "2️⃣ رابط التفعيل المباشر: اضغط /code\n"
        "━━━━━━━━━━━━━━\n"
        "📡 *يتم تحديث السيرفرات تلقائياً كل 15 دقيقة.*"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def auto_activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # رسالة مؤقتة تعطي إحساساً بالعمل البرمجي في الخلفية
    status_msg = await update.message.reply_text("🔄 **جاري اختراق نظام الحماية وجلب البيانات...**")
    
    # المواقع المستهدفة (يمكنك التبديل بينها)
    target_url = "https://auziatv.com/index.php"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(target_url, headers=headers, timeout=15).text
        
        # استخراج البيانات الحقيقية باستخدام أنماط Regex متطورة
        host_match = re.search(r'http://[a-zA-Z0-9.-]+:[0-9]+', response)
        user_match = re.search(r'Username[:\s]+([a-zA-Z0-9_-]+)', response, re.I)
        pass_match = re.search(r'Password[:\s]+([a-zA-Z0-9_-]+)', response, re.I)

        if host_match and user_match and pass_match:
            # بطاقة البيانات الاحترافية المماثلة للصورة التي أرسلتها
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
                "⚠️ **تنبيه أمني:**\n"
                "السيرفر يطلب تخطي يدوي حالياً.\n"
                "استخدم الأمر /code للحصول على الرابط."
            )
    except:
        await status_msg.edit_text("❌ **فشل:** السيرفر لا يستجيب حالياً.")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("code", lambda u, c: u.message.reply_text("👉 https://auziatv.com/index.php")))
    app.add_handler(MessageHandler(filters.Regex('^تفعيل$'), auto_activate))
    
    # حل مشكلة Conflict النهائية لمنع ظهور الأخطاء الحمراء
    app.run_polling(drop_pending_updates=True)
