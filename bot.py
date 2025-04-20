from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ApplicationBuilder, ContextTypes

# دسته‌بندی مشاغل
jobs_categories = {
    "engineering": ["مهندس نرم‌افزار", "مهندس برق", "مهندس مکانیک"],
    "art": ["نقاش", "گرافیست", "طراح مد"],
    "medicine": ["پزشک", "پرستار", "دندانپزشک"]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("مهندسی", callback_data="engineering")],
        [InlineKeyboardButton("هنر", callback_data="art")],
        [InlineKeyboardButton("پزشکی", callback_data="medicine")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("لطفاً یک دسته از مشاغل را انتخاب کنید:", reply_markup=reply_markup)

async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    category = query.data
    jobs = jobs_categories.get(category, [])
    if jobs:
        keyboard = [[InlineKeyboardButton(job, callback_data=f"job_{job}")] for job in jobs]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"مشاغل موجود در دسته انتخابی:", reply_markup=reply_markup)
    else:
        await query.answer("دسته‌بندی پیدا نشد.")

async def handle_job_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    job = query.data.replace("job_", "")
    await query.answer()
    await query.edit_message_text(f"شما شغل «{job}» را انتخاب کردید.")

# ساخت ربات
app = ApplicationBuilder().token("7875123067:AAHEIZ5GfvbdbHieDy5xUqQeGGeLNWfFeZs").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_category_selection, pattern="^(engineering|art|medicine)$"))
app.add_handler(CallbackQueryHandler(handle_job_selection, pattern="^job_"))

app.run_polling()
