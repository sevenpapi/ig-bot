import colorama
from CONSTANTS import bot_username, bot_password
from core.bot_engine import Bot

colorama.init()

bot = Bot(bot_username, bot_password)
bot.initialize()
bot.quit()

colorama.deinit()
