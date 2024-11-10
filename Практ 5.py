import telebot


TOKEN = '7440147569:AAGBj94rDeAkffKa-IWkIqGsGrk7LmyECaU'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    print("Бот запущено!")
    bot.polling(none_stop=True)
