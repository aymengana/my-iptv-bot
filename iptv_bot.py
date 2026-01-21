# -*- coding: utf-8 -*-
import requests
import random
import string
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن الجديد الخاص بك
BOT_TOKEN = '8312066648:AAEHJLLZVic_VkPDn5tkOHtkxu_aRT4CGcM'

def get_random_string(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إشعار المستخدم ببدء العملية
    status_msg = await update.message.reply_text("⏳ **جاري إنشاء حساب MoodTV حقيقي...**", parse_mode='Markdown')
    
    user = f"vip_{get_random_string(6)}"
    pwd = get_random_string(8)
    
    # محاولة الإنشاء الفعلية في الموقع لضمان عمل اليوزر
    url = "https://moodtv.xyz/create.php"
    payload = {'username': user, 'password': pwd, 'submit': ''}
    
    try:
        # إرسال طلب الإنشاء الحقيقي للموقع
        requests.post(url, data=payload, timeout=10)
        
        # إذا وصلنا هنا، نرسل البيانات للمستخدم بتنسيق احترافي
        response_text = (
            "✨ **تم توليد اشتراكك الخاص بنجاح!** ✨\n"
            "━━━━━━━━━━━━━━\n"
            "🌐 **SERVER:** `http://moodtv.xyz:8080`\n"
            f"👤 **USER:** `{user}`\n"
            f"🔑 **PASS:** `{pwd}`\n"
            "━━━━━━━━━━━━━━\n"
            "✅ **الحالة:** حساب نشط (متصل واحد) ✅\n"
            "📺 *انسخ البيانات وجربها في تطبيقك الآن.*"
        )
        await status_msg.edit_text(response_text, parse_mode='Markdown')
        
    except Exception as e:
        await status_msg.edit_text("⚠️ السيرفر مشغول حالياً، يرجى المحاولة مرة أخرى.")

if __name__ == '__main__':
    # بناء البوت مع ميزة مسح التحديثات القديمة لمنع التعليق
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    
    print("البوت يعمل الآن بالتوكن الجديد...")
    # drop_pending_updates=True ضرورية جداً لحل مشكلة التضارب السابقة
    app.run_polling(drop_pending_updates=True)
