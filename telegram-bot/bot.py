import os
import requests
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, ConversationHandler,
                          Application, CommandHandler, MessageHandler,
                          filters, ContextTypes,
                          )
from telegram.ext import CallbackQueryHandler


load_dotenv()

LOGIN, PASSWORD = range(2)

user_data = {}
user_tokens = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Запиши сюда свои гроши", callback_data="start_exchange")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("С праздником сучки, добро пожаловать на борт, капитан Залупа",
                                    reply_markup=reply_markup)


async def get_currency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get("http://127.0.0.1:8000/exchanger")
        if response.status_code == 200:
            result = response.text

            await update.message.reply_text(result)
        else:
            await update.message.reply_text("Ошибка сервера")
    except requests.exceptions.RequestException as e:
        print(f"{e}")
        await update.message.reply_text("Ошибка при подключении к серверу")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "start_exchange":
        context.user_data["step"] = "value"
        await query.edit_message_text("Введите сумму для обмена (валуе):")


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if "step" not in context.user_data:
        await update.message.reply_text("Нажмите кнопку для начала.")
        return

    step = context.user_data['step']

    if step == "value":
        try:
            value = float(update.message.text)
            context.user_data["value"] = value
            context.user_data['step'] = "your_currency"
            await update.message.reply_text("Введите вашу валюту (Например, RUB):")
        except ValueError:
            await update.message.reply_text("Введи норм данные капитан")

    elif step == "your_currency":

        your_currency = update.message.text.strip().upper()
        context.user_data["your_currency"] = your_currency
        context.user_data["step"] = "ex_currency"
        await update.message.reply_text("Введите целевую валюту (Например, USD):")

    elif step == "ex_currency":

        ex_currency = update.message.text.strip().upper()
        context.user_data["ex_currency"] = ex_currency

        value = context.user_data["value"]
        your_currency = context.user_data["your_currency"]
        ex_currency = context.user_data["ex_currency"]

        try:
            response = requests.post(
                f"http://127.0.0.1:8000/ex/{value}",
                json={"your_currency": your_currency, "ex_currency": ex_currency},
                timeout=5
            )
            if response.status_code == 200:
                result = response.json()
                await update.message.reply_text(f"{result['result']} данные добавлены в БД")
            else:
                await update.message.reply_text("Server Error")
        except requests.exceptions.RequestException as e:
            await update.message.reply_text(f"Connection error: {e}")

        context.user_data.clear()


async def login_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("На святое позарился, ну посмотрим на тебя, кто ты. Введи логин")
    return LOGIN


async def get_login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["login"] = update.message.text
    await update.message.reply_text("Введи свой пароль")
    return PASSWORD


async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text
    login = context.user_data.get("login")

    try:
        # Запрос на получение токена
        response = requests.post("http://127.0.0.1:8000/auth/token",
            data={"username": login, "password": password},
        )
        response.raise_for_status()
        token = response.json().get("access_token")
        user_tokens[update.message.chat_id] = token
        await update.message.reply_text("Ты прошел отбор, добро пожаловать на борт."
                                        " Теперь вы можете использовать команду /all.")
    except requests.HTTPError:
        await update.message.reply_text("Неверный логин или пароль")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Авторизация отминет")
    return ConversationHandler.END


# Команда /all: запрос защищенного ресурса
async def get_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = user_tokens.get(update.message.chat_id)
    if not token:
        await update.message.reply_text("Куда полез, сначал авторизируйся")
        return

    try:
        # Запрос к защищенному маршруту
        response = requests.get(
            "http://127.0.0.1:8000/auth/all",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        data = response.json()
        await update.message.reply_text(f"Данные {data}")
    except requests.HTTPError:
        await update.message.reply_text("Не удалось получить данные. Возможно, токен недействителен.")


def main() -> None:

    telegram_token = os.getenv("TELEGRAM_TOKEN")
    app = Application.builder().token(telegram_token).build()

    # ConversationHandler для авторизации
    login_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("login", login_start)],
        states={
            LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_login)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(login_conv_handler)
    app.add_handler(CommandHandler("all", get_all))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("exchanger", get_currency))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
