import logging
from logging import getLogger, Formatter
from logging.handlers import TimedRotatingFileHandler

class Log:
    __log_level_map = {
        'debug' : logging.DEBUG,
        'info' : logging.INFO,
        'warn' : logging.WARN,
        'error' : logging.ERROR,
        'critical' : logging.CRITICAL
    }

    __logger=None

    @staticmethod
    def init(logger_name = 'codeMarble',
             log_level = __log_level_map['debug'],
             log_filepath = 'codeMarble/resource/log/codeMarble.log'):

        Log.__logger = getLogger(logger_name)
        Log.__logger.setLevel(Log.__log_level_map['debug'])

        formatter = \
            Formatter('%(asctime)s - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(Log.__log_level_map['debug'])

        file_handler = TimedRotatingFileHandler(log_filepath,
                                                when='D',
                                                interval=1,
                                                backupCount=1,
                                                encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(Log.__log_level_map['debug'])

        Log.__logger.addHandler(console_handler)
        Log.__logger.addHandler(file_handler)

    @staticmethod
    def debug(msg):
        Log.__logger.debug(msg)

    @staticmethod
    def info(msg):
        Log.__logger.info(msg)

    @staticmethod
    def warn(msg):
        Log.__logger.warn(msg)

    @staticmethod
    def error(msg):
        Log.__logger.error(msg)

    @staticmethod
    def critical(msg):
        Log.__logger.critical(msg)