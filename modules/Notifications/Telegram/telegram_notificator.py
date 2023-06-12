import json
import logging
import requests

logger = logging.getLogger('project')

class TelegramNotify():
    """ Send telegram message """
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


class TelegramNotifyTrain(TelegramNotify):
    """ Send telegram message to alert user that a train is available. """

    message_format = ""
    symbol_less_5_places_left = ""
    symbol_6_to_10_places_left = ""
    symbol_11_to_20_places_left = ""
    symbol_more_20_places_left = ""

    def __init__(self):
        super().__init__()

    @classmethod
    def update_message_format(cls, config : dict):
        cls.message_format = config['message_format']
        cls.symbol_less_5_places_left = config['symbol_less_5_places_left']
        cls.symbol_6_to_10_places_left = config['symbol_6_to_10_places_left']
        cls.symbol_11_to_20_places_left = config['symbol_11_to_20_places_left']
        cls.symbol_more_20_places_left = config['symbol_more_20_places_left']
        logger.debug(f'Updating TelegramNotifyTrain configuration with format {cls.message_format}')

    @classmethod
    def send_train_alert(cls, name, date, departure_time, origin, destination, free_places, requestID, updatedAt):
        # generate content
        msg = cls.message_format
        msg = msg.replace("TRAIN_NAME", name)
        msg = msg.replace("TRAIN_DATE", date)
        msg = msg.replace("TRAIN_DEPARTURE_TIME", departure_time)
        msg = msg.replace("TRAIN_ORIGIN", origin)
        msg = msg.replace("TRAIN_DESTINATION", destination)
        msg = msg.replace("TRAIN_FREE_PLACES_LEFT", str(free_places))
        msg = msg.replace("REQUEST_NUMBER", str(requestID))
        msg = msg.replace("UPDATE_DATETIME", updatedAt)

        if free_places <= 5:
            msg = msg.replace("SYMBOL", cls.symbol_less_5_places_left)
        if 5 < free_places <= 10:
            msg = msg.replace("SYMBOL", cls.symbol_6_to_10_places_left)
        if 10 < free_places <= 20:
            msg = msg.replace("SYMBOL", cls.symbol_11_to_20_places_left)
        if free_places > 20:
            msg = msg.replace("SYMBOL", cls.symbol_more_20_places_left)
        
        # send notification
        cls.send_telegram_message(msg)