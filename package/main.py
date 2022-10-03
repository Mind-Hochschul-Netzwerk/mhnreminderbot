# Imports
from dataclasses import dataclass
import logging
import schedule
import datetime 
import time
from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
from . import config


LOGLEVEL = logging.DEBUG
# May add loglevel specification over command line or config file later

try:
    logging.basicConfig(
        level=LOGLEVEL,
        filename=config.logging_config["file"],
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt="%Y-%m-%dT%H:%M:%S%z"
    )
except Exception as exception:
    logging.warning(exception)
    raise exception

try:
    logging.debug("Startup")
    logging.debug("Initialize Log")
except Exception as exception:
    logging.warning(exception)
    raise exception

#Constants
do_now = False

# Telegeram
updater = Updater(token=config.tg_config['token'], use_context=True)
dispatcher = updater.dispatcher

# Commands
def start(update, context):
    try:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, I am the Bot that reminds the IT Team of its regular Telco.")
    except Exception as exception:
        raise exception

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


# Every Day Job
def reminder():
    """Check for new comics and send them afterwards"""
    try:
        for i in config.tg_config['chat_ids']:
            if datetime.datetime.today().day > 8:
                updater.bot.send_message(chat_id=i, text="Heute ist Telko um 20:00 Uhr. Wie immer im Discord vom MHN.")
                log_string = "Done sending to " + str(i)
                logging.debug(log_string)
            elif datetime.datetime.today().day > 8 and datetime.datetime.today().hour < 19:
                updater.bot.send_message(chat_id=i, text="Heute ist Telko um 20:00 Uhr. Wie immer im Discord vom MHN.")
                log_string = "Done sending to " + str(i)
                logging.debug(log_string)
            elif datetime.datetime.today().day < 7:
                updater.bot.send_message(chat_id=i, text="Vergesst nicht an jedem ersten Donnerstag im Monat findet die IT team Telko auf dem MHN Discordserver um 20:00 Uhr statt.")
                log_string = "Done sending to " + str(i)
                logging.debug(log_string)
    except Exception as e:
        print(e)

schedule.every().thursday.at("16:00").do(reminder)
schedule.every().thursday.at("20:00").do(reminder)


if do_now is True:
    reminder()
    do_now = False
    

updater.start_polling()

while True:
    schedule.run_pending()
    time.sleep(1)
    
