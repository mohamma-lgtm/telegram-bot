import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("البوت شغال 24/7 🔥")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()        await query.edit_message_text("اكتب مشكلتك الآن وأرسلها:")
        context.user_data["step"] = "problem"

    elif query.data == "data":
        await query.edit_message_text("الرجاء إرسال: الاسم، الكنية، رقم التواصل")
        context.user_data["step"] = "data"

    elif query.data == "send":
        usdt_address = "TXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # حط عنوان USDT تبعك هون
        await query.edit_message_text(f"لإجراء عملية التواصل الرجاء إرسال 20 USDT إلى:\n`{usdt_address}`\n\nبعد الدفع ارسل صورة التحويل", parse_mode="Markdown")
        context.user_data["step"] = "waiting_payment" # علامة انو ناطر صورة

    elif query.data == "send_request":
        problem_text = context.user_data.get("problem", "لم يتم رفع مشكلة")
        data_text = context.user_data.get("data", "لم يتم رفع بيانات")

        keyboard = [
            [InlineKeyboardButton("موافق", callback_data=f"approve_{user_id}")],
            [InlineKeyboardButton("رفض", callback_data=f"reject_{user_id}")]
        ]
        await context.bot.send_message(
            ADMIN_ID,
            f"📩 طلب جديد جاهز للموافقة\nمن: {query.from_user.full_name}\nID: `{user_id}`\n\n**المشكلة:**\n{problem_text}\n\n**البيانات:**\n{data_text}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        await query.edit_message_text("✅ تم ارسال طلبك للإدارة بنجاح، بانتظار الموافقة")

    elif query.data.startswith("approve_"):
        client_id = int(query.data.split("_")[1])
        await context.bot.send_message(client_id, "✅ تمت الموافقة على طلبك\nسيتواصل معك الأدمن قريباً")
        await query.edit_message_text("تمت الموافقة وابلاغ العميل")

    elif query.data.startswith("reject_"):
        client_id = int(query.data.split("_")[1])
        await context.bot.send_message(client_id, "❌ تم رفض طلبك. يرجى تعديل البيانات والمشكلة")
        await query.edit_message_text("تم رفض الطلب")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    step = context.user_data.get("step")

    if step == "problem":
        context.user_data["problem"] = text
        await update.message.reply_text("تم حفظ المشكلة ✅\nالآن اضغط 'رفع البيانات'")
        context.user_data["step"] = None

    elif step == "data":
        context.user_data["data"] = text
        await update.message.reply_text("تم حفظ البيانات ✅\nالآن اضغط 'ارسال الطلب'")
        context.user_data["step"] = None

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("step")
    user = update.effective_user

    if step == "waiting_payment":
        # ببعت الصورة للادمن مع تعليق
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=f"💰 وصل دفع جديد\nمن: {user.full_name}\nID: `{user.id}`",
            parse_mode="Markdown"
        )
        await update.message.reply_text("✅ تم استلام صورة التحويل\nسيتم مراجعتها من قبل الإدارة")
        context.user_data["step"] = None
    else:
        await update.message.reply_text("⚠️ ارسل الصورة بعد الضغط على زر 'ارسال العمولة'")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo)) # اضفنا هاد السطر
    print("البوت شغال...")
    app.run_polling()

if __name__ == "__main__":
    main()
