import telebot
from config import config


env = config.load_config('.env')

bot = telebot.TeleBot(env.tg_bot.bot_token)


@bot.message_handler(commands=['start'])
def start_message(message: telebot.types.Message):
    deep_link = message.text[7:]
    answer = f'Привет {message.chat.first_name}, ты написал /start,'

    message_to_admin = f'Привет, tg пользователь {message.chat.username}, '\
                       f'имя {message.chat.first_name} написал /start,\n'\
                       f'Его телеграм id {message.chat.id}\n'\
                       f'Его deep_link is {deep_link}'
    bot.send_message(message.chat.id, answer)
    bot.send_message(env.tg_bot.admin_ids[0], message_to_admin)
    print(message)
    return None


bot.polling()
