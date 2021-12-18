import unittest
from debug import connect
from telethon import TelegramClient, sync, events
from telethon.tl.functions.channels import GetMessagesRequest
import time


"""
    Your API ID, hash and session string here
"""
api_id = int('16333584')
api_hash = "c4644b465027ca9e4ced09d1f60f34f2"
client = TelegramClient('session_name', api_id, api_hash)

client.start()


class DBconnectionTest(unittest.TestCase):
    def connection(self):
        self.assertEqual(connect(), 1)

    def testStart(self):
        try:
            client.send_message('@OlegVladimirovich_bot', '/start')
            time.sleep(2)
            messages = client.get_messages('@OlegVladimirovich_bot')
            for message in client.get_messages('@OlegVladimirovich_bot', limit=1):
                m = message.message
            text = 'Добро пожаловать'
            if text in m:
                self.assertEqual(1, 1)
            else:
                self.assertEqual(0, 1)
        except:
            self.assertFalse(True)

    def testHelp(self):
        try:
            client.send_message('@OlegVladimirovich_bot', '/help')
            time.sleep(2)
            messages = client.get_messages('@OlegVladimirovich_bot')
            for message in client.get_messages('@OlegVladimirovich_bot', limit=1):
                m = message.message
            text = 'start - Запуск бота\ndisplay - отображение всех ссылок\ndelete <id записи> - удаление ссылки (можно узнать набрав команду /display - первое значение)'
            if text in m:
                self.assertEqual(1, 1)
            else:
                self.assertEqual(0, 1)
        except:
            self.assertFalse(True)


if __name__ == "__main__":
    unittest.main()
