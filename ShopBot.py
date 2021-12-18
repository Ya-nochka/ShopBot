from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from translate import Translator
import mysql.connector
from mysql.connector import Error
from secrets import TOKEN, host, database, user, password
import re



def get_or_create(chat_id, name):

    """
        Получить / создать пользователя tg
        Бот подключается к базе данных,
        от результата подключения зависит вывод:
        'Ошибка подключения' - соединение не установлено,
        'Успешное подключение к базе данных' - соединение установлено
        Далее регистрируется ID клиента, использовавшего бот
    """

    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
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


def add_link_to_db(chat_id, link):

    """
        Добавить ссылку для пользователя tg
        Необходимо соединение с MySQL
        Если его нет, программа выдаёт: 'Ошибка подключения'
        Если соединение есть: 'Успешное подключение к базе данных'
        После этого выводится ID пользователя телеграм бота
    """

    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        if not connection.is_connected():
            print('Ошибка подключения')

        else:
            print('Успешное подключение к базе данных')

            with connection.cursor() as cursor:
                insert_query = "INSERT INTO users_links (user_id, link, disable)" + f" VALUES ({chat_id}, '{link}', 0);"
                print(insert_query)
                cursor.execute(insert_query)
                connection.commit()

    except Error as e:
        print(e)

    finally:
        connection.close()





def start(update, context):

    """
        Обработка команды start
        Когда бот принимает на вход '/start', ему необходимо поприветсвовать клиента следующим сообщением:
        'Добро пожаловать, (имя пользователя).
        Меня зовут Олежка. Я буду твоим персональным помощником!'
    """

    first_name = update.message.chat.first_name
    update.message.reply_text(
        f"Добро пожаловать, {first_name}. Меня зовут Олежка. Я буду твоим персональным помощником!")
    get_or_create(update.message.chat_id, first_name)


def help(update, context):

    """
        Обработка команды help
        Когда бот принимает на вход '/help', он выводит список возможных команд,
        с пояснением вызова каждой.
        Из них : start, display, delete
    """

    update.message.reply_text('start - Запуск бота\ndisplay - отображение всех ссылок\ndelete <id записи> - удаление ссылки (можно узнать набрав команду /display - первое значение)')


def display(update, context):

    """
           Обработка команды display
           Когда бот принимает на вход '/display', он подключается к базе данных
           от результата подключения зависит вывод:
           'Ошибка подключения' - соединение не установлено,
           'Успешное подключение к базе данных' - соединение установлено
           выводит список ссылок, сохранившихся
           в базе данных, а также ID пользователя, их добавивших
           Если их нет, бот возвращает: "Не нахожу ссылок"
       """

    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        if not connection.is_connected():
            print('Ошибка подключения')

        else:
            print('Успешное подключение к базе данных')
    except Error as e:
        print(e)

    try:
        with connection.cursor() as cursor:
            select_all_rows = f"SELECT * FROM users_links WHERE user_id = {update.effective_chat.id};"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            for row in rows:
                print(str(row))
                l = str(row)
                update.message.reply_text(l)
    except:
        update.message.reply_text('Не нахожу ссылок')





def delete(update, context):

    """
        Обработка команды delete
        :argument int
        Обработка команды delete
        Когда бот принимает на вход '/delete', он подключается к базе данных
        от результата подключения зависит вывод:
        'Ошибка подключения' - соединение не установлено,
        'Успешное подключение к базе данных' - соединение установлено
        Далее идёт удаление определённой(следует из введённого аргумента)
        или всех (по желанию клиента) ранее найденных ссылок из базы данных

    """

    this_id = int(' '.join(context.args))
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        if not connection.is_connected():
            print('Ошибка подключения')

        else:
            print('Успешное подключение к базе данных')
    except Error as e:
        print(e)
    # try:
    with connection.cursor() as cursor:
        delete_data = "DELETE FROM users_links WHERE id = " + f"{this_id};"
        cursor.execute(delete_data)
        connection.commit()
        update.message.reply_text('Успешно удалено')


def error(update, context):

    """
        Возврат ошибки пользователю
        При введение пользователем команд, не встроенных в программу,
        бот возвращает: 'Произошла ошибка бота :('
    """

    update.message.reply_text('Произошла ошибка бота :(')



def echo(update, context):

    """
        Обработка текстовых сообщений
        l принимает кол-во ссылок
        если == 1, бот успешно добавляет в базу данных и возвращает: "Добавил в базу данных"
        елси ссылок введено больше, возвращает: "Отправляй ссылки по очереди)"
        При вводе какого-либо текстового сообщения, телеграмм бот переводит его на русский язык
    """

    link = update.message.text
    l = re.findall("(?P<url>https?://[^\s]+)", link)
    if len(l) == 1:
        add_link_to_db(update.effective_chat.id, l[0])
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Добавил в базу данных")
    elif len(l) > 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Отправляй ссылки по очереди)")
    else:
        translator = Translator(to_lang="ru")
        translation = translator.translate(update.message.text)
        text = 'Перевожу: ' + translation
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text)


def main():

    """
        Телеграм бот
        Функция регистрирует в госреестре обработчиков все возможные команды
    """

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("display", display))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("delete", delete))

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
