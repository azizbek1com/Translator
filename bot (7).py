import logging
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# === TOKENLAR ===
TELEGRAM_TOKEN = "BU_YERGA_YANGI_TELEGRAM_TOKENNI_QOʻYING"
ANTHROPIC_API_KEY = "BU_YERGA_ANTHROPIC_API_KEYNI_QOʻYING"

# === LOGGING ===
logging.basicConfig(level=logging.INFO)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# === START ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! 👋\n\n"
        "Men tarjimon botman:\n"
        "🇺🇿 O'zbekcha yozsangiz → Turkchaga tarjima qilaman\n"
        "🇹🇷 Turkcha yozsangiz → O'zbekchaga tarjima qilaman\n\n"
        "Boshlang! ✍️"
    )

# === TARJIMA ===
async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    if not user_text:
        return

    await update.message.chat.send_action("typing")

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=(
                "Sen o'zbek va turk tillarida professional tarjimonsan. "
                "Foydalanuvchi matn yuboradi — tilini aniqla (o'zbek yoki turk), "
                "so'ng boshqa tilga tabiiy va ravon tarjima qil. "
                "Faqat tarjima matnini yoz, boshqa hech narsa yozma."
            ),
            messages=[{"role": "user", "content": user_text}]
        )
        translation = response.content[0].text.strip()
        await update.message.reply_text(translation)

    except Exception as e:
        logging.error(f"Xato: {e}")
        await update.message.reply_text("Xatolik yuz berdi, qayta urinib ko'ring.")

# === ISHGA TUSHIRISH ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))
    print("Bot ishlamoqda...")
    app.run_polling()
