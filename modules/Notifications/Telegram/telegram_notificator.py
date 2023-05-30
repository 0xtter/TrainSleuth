import json
import logging
import requests

logger = logging.getLogger('project')

class TelegramNotify():
    API_KEY = None
    user_id = None

    def __init__(self):
        pass

    @classmethod
    def update_configuration(cls,config : dict):
        cls.API_KEY = config['API_KEY']
        cls.user_id = config['user_id_to_notify']
        logger.debug(f'updating configuration with API_KEY = {cls.API_KEY} and user_id = {cls.user_id}')
    
    @classmethod
    def send_telegram_message(cls, message : str):
        if cls.API_KEY == None or cls.user_id == None:
            return
        logger.debug(f'sending message "{message}" to user id : {cls.user_id}')
        response = requests.get(f'https://api.telegram.org/bot{cls.API_KEY}/sendMessage?chat_id={cls.user_id}&text={message}')
        logger.debug(f'response : {response.json()}')