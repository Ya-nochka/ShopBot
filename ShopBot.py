from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Обработка команды start
def start(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text(
        f"Добро пожаловать, {first_name}. Меня зовут Олежка. Я буду твоим персональным помощником!")


# Обработка команды help
def help(update, context):
    update.message.reply_text('Подсказки в разработке...')


# Возврат ошибки пользователю
def error(update, context):
    update.message.reply_text('Произошла ошибка бота :(')


# Обработка текстовых сообщений
def echo(update, context):
    text = 'Получено: ' + update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


# Телеграм бот
def main():
    TOKEN = "5095243696:AAFRdkSXJsV5Ly_CwnhH5dKmpC-34dxXCLw"

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()


