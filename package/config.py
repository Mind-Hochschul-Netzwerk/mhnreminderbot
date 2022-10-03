import json
import logging

try:
    with open('config.json') as config_json:
        config = json.load(config_json)
    logging_config = config["all"]["logging"]
    tg_config = config["all"]["tg"]
except Exception as e:
    logging.warning(e)
    print("Error ", e)
    raise e