from config_data import config
from pprint import pprint

conf = config.load_config('.env')
TOKEN = conf.tg_bot.bot_token
pprint(TOKEN)
