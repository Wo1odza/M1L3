import telebot
from config import token

bot = telebot.TeleBot(token)

# Функция для бана пользователя
def ban_user(message, user_id, chat_id):
    try:
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status in ('administrator', 'creator'):
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка при бане: {e}")

@bot.message_handler(commands=['ban'])
def ban_user_command(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        ban_user(message, user_id, chat_id)
    else:
        bot.reply_to(message, "Команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")


@bot.message_handler(func=lambda message: True)
def process_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if "https://" in message.text:
      # Здесь нужно добавить логирование и сохранение информации о пользователе и сообщении для последующей работы с базой данных
      #  Пример:
      #  save_user_info(user_id, message.text, chat_id)  # Предполагается, что эта функция сохраняет данные.
      bot.reply_to(message, "Ссылка в сообщении. Пользователь заблокирован.")
      ban_user(message, user_id, chat_id)



@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")



bot.infinity_polling()
