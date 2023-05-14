import logging.config

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class NoFishTextFilter(logging.Filter):
    def filter(self, record):
        result = ''
        if record.msg is not None:
            for symbol in record.msg:
                ASCII = ord(symbol)
                if ASCII <= 128:
                    result += symbol
            record.msg = result
        return True


class CustomStreamHandlerHandler(logging.Handler):

    def __init__(self, url):
        super().__init__()
        self.url = url

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.get(f'{self.url}?log_message={message}')


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(created)s | %(lineno)s | %(message)s"
        }
    },
    "filters": {
        "no_fish_text_filter": {
            '()': NoFishTextFilter
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "base",
            'filters': ['no_fish_text_filter']
        },
        "file_debug": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filename": "logfile_debug.log",
            "mode": "a",
            'filters': ['no_fish_text_filter']
        },
        "file_error": {
            "class": "logging.FileHandler",
            "level": "ERROR",
            "formatter": "base",
            "filename": "logfile_error.log",
            "mode": "a",
            'filters': ['no_fish_text_filter']
        },
        "file_info": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "base",
            "filename": "logfile_info.log",
            "mode": "a",
            'filters': ['no_fish_text_filter']
        },
        "file_info_utils": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "h",
            "interval": 10,
            "backupCount": 1,
            "level": "INFO",
            "formatter": "base",
            "filename": "logfile_info.utils.log",
            'filters': ['no_fish_text_filter']
        },
        "send_to_site": {
            "()": CustomStreamHandlerHandler,
            "level": "DEBUG",
            "formatter": "base",
            "url": 'http://127.0.0.1:5000/text'
        }
    },
    "loggers": {
        "module_logger": {
            "level": "DEBUG",
            "handlers": ["file_debug", "file_error", "file_info", "console", "send_to_site"],
            "propagate": False,
        },
        "utils": {
            "level": "DEBUG",
            "handlers": ["file_info_utils", "console"],
            "propagate": False,
        }
    },
    # 'root': {
    #     'level': 'DEBUG',
    #     'handlers': ['console']
    # }
}
