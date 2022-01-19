import logging
import os
from textwrap import dedent

import requests
import telegram
from dotenv import load_dotenv


def get_devman_reviews(token, timestamp_to_request):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {token}'
        }
    params = {
        'timestamp': timestamp_to_request
        }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def send_telegram_message(token, chat_id, text):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=text)


if __name__ == '__main__':
    logging.basicConfig(
        filename='logs.log',
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s')
    load_dotenv()
    devman_api_token = os.environ['DEVMAN_API_TOKEN']
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
    last_attempt_timestamp = None
    while True:
        try:
            review = get_devman_reviews(
                devman_api_token, last_attempt_timestamp)
            if review['status'] == 'timeout':
                last_attempt_timestamp = review['timestamp_to_request']
            else:
                review_details = review['new_attempts'][0]
                lesson_title = review_details['lesson_title']
                lesson_url = review_details['lesson_url']
                review_is_negative = review_details['is_negative']
                message_template = f'У Вас проверили работу: '
                if not review_is_negative:
                    message = f"""\
                            {message_template} "{lesson_title}".
                            Преподавателю всё понравилось, можно приступать
                            к следующему уроку!
                            """
                else:
                    message = f"""\
                            {message_template} "{lesson_title}".
                            К сожалению, в работе нашлись ошибки, подробности
                            по ссылке: {lesson_url}
                            """
                send_telegram_message(
                    telegram_bot_token, telegram_chat_id, dedent(message))
        except (requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError) as error:
            logging.exception(error)
