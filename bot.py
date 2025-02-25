import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
EXCHANGE_API_KEY = os.getenv('EXCHANGE_API_KEY')

# Инициализация приложения Telegram
application = Application.builder().token(TELEGRAM_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 Привет! Используй /rates для получения курса USD к основным валютам")

def fetch_rates():
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/USD"
    response = requests.get(url)
    data = response.json()
    
    if data.get('result') == 'success':
        return {
            'EUR': data['conversion_rates']['EUR'],
            'GBP': data['conversion_rates']['GBP'],
            'JPY': data['conversion_rates']['JPY'],
            'RUB': data['conversion_rates']['RUB']
        }
    raise Exception("API Error")

async def rates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        rates = fetch_rates()
        message = (
            "📈 Текущий курс USD:\n\n"
            f"🇪🇺 EUR: {rates['EUR']:.2f}\n"
            f"🇬🇧 GBP: {rates['GBP']:.2f}\n"
            f"🇯🇵 JPY: {rates['JPY']:.2f}\n"
            f"🇷🇺 RUB: {rates['RUB']:.2f}"
        )
        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text("⚠️ Сервис временно недоступен")

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
async def webhook():
    await application.update_queue.put(
        Update.de_json(request.json, application.bot)
    return 'ok'

def main():
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("rates", rates))
    
    # Для PythonAnywhere
    application.run_webhook(
        listen="0.0.0.0",
        port=8080,
        webhook_url=f"https://ВАШ_ЛОГИН.pythonanywhere.com/{TELEGRAM_TOKEN}",
        secret_token='WEBHOOK_SECRET'
    )

if __name__ == "__main__":
    main()
