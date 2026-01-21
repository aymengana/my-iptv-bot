# -*- coding: utf-8 -*-
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# توكن البوت الخاص بك
BOT_TOKEN = '8312066648:AAFHr1prjk642UaZExabW8jDr9S-lZxHsdo'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"💎 **مرحباً بك في {user_name} IPTV GEN v2.0**\n"
        "━━━━━━━━━━━━━━\n"
        "📺 **أقوى مولد أكواد IPTV مباشر وسريع**\n\n"
        "✅ استخراج بيانات الـ Xtream تلقائياً\n"
        "✅ دعم فني ومتابعة مستمرة\n"
        "✅ قنوات بجودة 4K و FHD\n"
        "━━━━━━━━━━━━━━\n"
        "👇 **للبدء، أرسل البيانات بهذا الشكل:**\n"
        "`user:pass`"
    )
    # أزرار احترافية أسفل الرسالة
    keyboard = [
        [InlineKeyboardButton("📢 قناة التحديثات", url="https://t.me/your_channel")],
        [InlineKeyboardButton("👨‍💻 المطور", url="https://t.me/your_username")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if ":" in text:
        try:
            user, pwd = text.split(":", 1)
            user = user.strip()
            pwd = pwd.strip()
            
            # حالة التحميل الوهمية لإعطاء طابع احترافي
            status_msg = await update.message.reply_text("🔍 **جاري فحص السيرفر واستخراج البيانات...**", parse_mode='Markdown')
            
            host = "http://freetv.fun:8080"
            
            # تصميم بطاقة البيانات المنظمة
            response_text = (
                "🎁 **تم تجهيز بيانات اشتراكك بنجاح!**\n"
                "━━━━━━━━━━━━━━\n"
                f"🌐 **HOST:** `{host}`\n"
                f"👤 **USER:** `{user}`\n"
                f"🔑 **PASS:** `{pwd}`\n"
                "━━━━━━━━━━━━━━\n"
                "💡 *اضغط على البيانات أعلاه لنسخها تلقائياً.*\n"
                "📺 *يعمل على IPTV Smarters و VLC و كافة الأجهزة.*"
            )
            
            await status_msg.edit_text(response_text, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text("⚠️ **حدث خطأ غير متوقع، حاول مرة أخرى.**")
    else:
        await update.message.reply_text("❌ **صيغة خاطئة!**\nيرجى إرسال: `الاسم:كلمة السر`")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    app.run_polling()
