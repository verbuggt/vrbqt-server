import datetime
import logging

LOG_PATH = "./logs/"
LOG_FILE = f"{LOG_PATH if LOG_PATH.endswith('/') else LOG_PATH + '/'}buq_log-{datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}"
LOG_LEVEL = logging.DEBUG

logging.basicConfig(filename=LOG_FILE)

logging.info("info")
logging.debug("debug")
logging.critical("crit")
