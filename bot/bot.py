import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from .trader import analyze_signal, place_order

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я GPT трейдер бот. Используй /signal для сигнала.")

async def signal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol, direction, amount = analyze_signal()
    keyboard = [
        [InlineKeyboardButton("✅ Подтвердить", callback_data="confirm"),
         InlineKeyboardButton("❌ Пропустить", callback_data="skip")]
    ]
    text = f"Сигнал: {direction} {symbol}, сумма {amount}"
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "confirm":
        result = place_order()
        await query.edit_message_text(f"Ордер помещён: {result}")
    else:
        await query.edit_message_text("Сделка пропущена.")

def start_bot():
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
