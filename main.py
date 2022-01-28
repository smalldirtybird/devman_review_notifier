import argparse
import logging
import os
from textwrap import dedent
from time import sleep

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


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Получайте сообщение о проверке задания в Телеграм.')
    parser.add_argument('-d', '--delay', default=60,
                        help="""
                        Время паузы перед отправкой нового запроса
                        в случае отсутствия соединения с сетью.
                        """
                        )
    args = parser.parse_args()
    return args.delay


if __name__ == '__main__':
    delay = get_arguments()
    logging.basicConfig(
        filename='logs.log',
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s')
    load_dotenv()
    devman_api_token = os.environ['DEVMAN_API_TOKEN']
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
    bot = telegram.Bot(token=telegram_bot_token)
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
                bot.send_message(chat_id=telegram_chat_id,
                                 text=dedent(message))
        except requests.exceptions.ReadTimeout as et_error:
            logging.exception(et_error)
        except requests.exceptions.ConnectionError as c_error:
            logging.exception(c_error)
            sleep(delay)
