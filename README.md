# ShopBot

### Данный бот в Telegram позволяет

####Для запуска необходимо выполнить несколько команд:
 
1) Клонируем репозиторий к себе
``` bash
git clone <ссылка на репозиторий>
```
2) Переходим в репозиторий
``` bash
cd ShopBot
```
3) Устанавливаем все необходимые зависимости
``` bash
python3 -m pip install -r requirements.txt
```
4) Необходимо в `secrets.py` изменить токен и указать реквизиты базы данных вашей
``` python
TOKEN = '<ваш токен>'
host = '<ссылка на базу данных>'
database = '<название базы данных>'
user = '<имя пользователя бд>'
password = '<пароль от user>'
```
5) Запускаем бота
``` bash
python3 bot.py
```
## Запуск тестов
``` bash
python3 bot_test.py
```


&copy; Все права защищены. 


