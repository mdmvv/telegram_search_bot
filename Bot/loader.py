from configparser import ConfigParser
import logging
from aiogram import Bot
from aiogram import Dispatcher


config = ConfigParser()
config.read('config.ini')
api_token = config.get('Telegram', 'api_token')


logging.basicConfig(level=logging.INFO)


bot = Bot(token=api_token)
dp = Dispatcher(bot)
