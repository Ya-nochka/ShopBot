import mysql.connector
from mysql.connector import Error
from secrets import TOKEN, host, database, user, password


def connect():
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        if not connection.is_connected():
            return 0

        else:
            return 1
    except Error as e:
        return 0