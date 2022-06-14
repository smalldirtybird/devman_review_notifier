# [Devman](https://dvmn.org/modules/) review notifier

Receive notification directly to the telegram channel.
 
## How to prepare:
1. Make sure Python installed on your PC - you can get it from [official website](https://www.python.org/).
   

2. Install libraries with pip:
    ```
    pip3 install -r requirements.txt
    ```
   
3. Get your personal token for access to Devman API on [Devman API page](https://dvmn.org/api/docs/). 
   Create .env file in directory with main.py file(use Notepad++) and add the string
    ```
    DEVMAN_API_TOKEN ='your_devman_api_token'
    ```
    to it instead of value in quotes. Here and further quotes must be removed.

  
4. Create a Telegram bot which will post pictures to your own channel - just send message `/newbot` to [@BotFather](https://telegram.me/BotFather) and follow instructions.
    After bot will be created, get token from @BotFather and add to .env file:
    ```
    TELEGRAM_BOT_TOKEN ='your_telegram_bot_token'
    ```
    Put your token instead of value in quotes.

   
5. Get your Telegram id - just send message `/start` to `@userinfobot` and copy value of id from answer.
    Add the string
    ```
    TELEGRAM_CHAT_ID=@'YourTelegramID'
    ```
    to .env file (`@` symbol is required).
   
## How to use:
Run `main.py` with console. Use `cd` command if you need to change directory:
```
D:\>cd D:\learning\python\Chat_bots\devman_review_notifier
D:\learning\python\Chat_bots\devman_review_notifier>python main.py
```
In case of errors, the bot will send their text in the message.

## Available options
You can change delay time in case of connection error.
Get instructions options with `-h` argument:
```
D:\learning\python\Chat_bots\devman_review_notifier>python main.py -h
usage: main.py [-h] [-d DELAY]

Получайте сообщение о проверке задания в Телеграм.

optional arguments:
  -h, --help            show this help message and exit
  -d DELAY, --delay DELAY
                        Время паузы перед отправкой нового запроса в случае отсутствия соединения с сетью.

```
