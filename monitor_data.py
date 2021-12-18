import mysql.connector
from mysql.connector import Error
from secrets import TOKEN, host, database, user, password

"""
    Отображает все записи таблицы telegram_users
"""

if __name__ == '__main__':
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
            select_all_rows = "SELECT * FROM telegram_users"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
    except:
        pass