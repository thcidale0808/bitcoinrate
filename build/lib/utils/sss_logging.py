import logging
import logging.config


class STDOutFilter(logging.Filter):
    def __init__(self, param=None):
        self.param = param

    def filter(self, record):
        return record.levelno <= logging.INFO


# fmt: off
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'stdout_filter': {
            '()': STDOutFilter,
        }
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s Line %(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'filters': ['stdout_filter']
        },
        'errors': {
            'level': 'WARNING',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
        'all_to_stdout': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default', 'errors'],
            'level': 'INFO',
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
        'tests': {
            'handlers': ['all_to_stdout'], # pytest does not like stderr
            'level': 'DEBUG',
            'propagate': False
        },

    }
}
# fmt: on


class SSSLogging:
    @staticmethod
    def setup():
        logging.config.dictConfig(LOGGING_CONFIG)
        logger = logging.getLogger()
        logger.debug("Instantiated Logging with DictConfig")

    @staticmethod
    def update_logger(logger, custom_logging_config):
        """
        :param logger: passed from submodule
        :param custom_logging_config: variables to update logging config of form '"key"="value","key2"="value2",..'
        :return: logger
        """

        logging_config = custom_logging_config.split(",")
        logging_config_dict = {}
        for config in logging_config:
            key, value = config.split("=")
            logging_config_dict[key] = value

        if logging_config_dict.get("set_level"):
            logger.setLevel(logging_config_dict["set_level"].upper())

        if logging_config_dict.get("filehandler"):
            logger.addHandler(logging.FileHandler(logging_config_dict["filehandler"]))

        if logging_config_dict.get("propagate"):
            logger.propagate = (
                True if logging_config_dict["propagate"].upper() == "TRUE" else False
            )

        return logger
