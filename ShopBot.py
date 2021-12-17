from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from translate import Translator
import mysql.connector
from mysql.connector import Error

def connect():
    try:
        connection = mysql.connector.connect(host='37.140.192.81',
                                             database='u1256183_shop-helper',
                                             user='u1256183_yana',
                                             password='tD8lL6sQ2yjN8h')
        if not connection.is_connected():
            print('Ошибка подключения')

        else:
            print('Успешное подключение к базе данных')

    except Error as e:
        print(e)

    finally:
        connection.close()


# Get/create tg user
def get_or_create(chat_id, name):
    try:
        connection = mysql.connector.connect(host='37.140.192.81',
                                             database='u1256183_shop-helper',
                                             user='u1256183_yana',
                                             password='tD8lL6sQ2yjN8h')
        if not connection.is_connected():
            print('Ошибка подключения')

        else:
            print('Успешное подключение к базе данных')

            with connection.cursor() as cursor:
                select_all_rows = f"SELECT * FROM telegram_users WHERE external_id = {chat_id};"
                cursor.execute(select_all_rows)
                rows = cursor.fetchall()
            print(rows)
            if not rows:
                print("Nothing found")
                with connection.cursor() as cursor:
                    insert_query = "INSERT INTO telegram_users (external_id, name, notifications)" + f" VALUES ({chat_id}, '{name}', 1);"
                    print(insert_query)
                    cursor.execute(insert_query)
                    connection.commit()

    except Error as e:
        print(e)

    finally:
        connection.close()


# Обработка команды start
def start(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text(
        f"Добро пожаловать, {first_name}. Меня зовут Олежка. Я буду твоим персональным помощником!")
    get_or_create(update.message.chat_id, first_name)


# Обработка команды help
def help(update, context):
    update.message.reply_text('Подсказки в разработке...')


# Возврат ошибки пользователю
def error(update, context):
    update.message.reply_text('Произошла ошибка бота :(')


# Обработка текстовых сообщений
def echo(update, context):
    translator = Translator(to_lang="ru")
    translation = translator.translate(update.message.text)
    text = 'Перевожу: ' + translation
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


# Телеграм бот
def main():
    debug_bt = True
    if debug_bt:
        connect()

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

