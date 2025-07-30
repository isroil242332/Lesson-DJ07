import requests
import telebot
from telebot import types

# Конфигурация
BOT_TOKEN = 'ВАШ_TELEGRAM_BOT_TOKEN'
API_URL = 'http://localhost:8000/api/'  # Замените на URL вашего Django сервера


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    user = message.from_user
    data = {
        'user_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    try:
        response = requests.post(f'{API_URL}register/', json=data)
        if response.status_code == 201 or response.status_code == 200:
            bot.reply_to(message, "✅ Вы успешно зарегистрированы!")
        else:
            bot.reply_to(message, "⚠️ Вы уже зарегистрировались!")
    except requests.exceptions.RequestException:
        bot.reply_to(message, "🚨 Ошибка сервера. Пожалуйста, попробуйте позже.")


@bot.message_handler(commands=['myinfo'])
def handle_myinfo(message):
    user_id = message.from_user.id

    try:
        response = requests.get(f'{API_URL}user/{user_id}/')
        if response.status_code == 200:
            user_data = response.json()
            info_text = (
                f"ℹ️ Ваша информация:\n"
                f"ID: {user_data['user_id']}\n"
                f"Имя пользователя: {user_data['username']}\n"
                f"Имя: {user_data['first_name']}\n"
                f"Фамилия: {user_data['last_name']}\n"
                f"Дата регистрации: {user_data['created_at']}"
            )
            bot.reply_to(message, info_text)
        else:
            bot.reply_to(message, "❌ Вы не зарегистрированы. Пожалуйста, используйте /start сначала.")
    except requests.exceptions.RequestException:
        bot.reply_to(message, "🚨 Ошибка сервера. Пожалуйста, попробуйте позже.")


if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()