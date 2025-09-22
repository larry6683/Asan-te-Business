import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class LogUtils:
    @staticmethod
    def log_exception(action: str, exception: Exception):
        logger.error(f"fatal error during action: {action}. Exception: type: {type(exception)}, args: {exception.args}")

    @staticmethod
    def log_unsupported_operation(action: str):
        logger.error(f'unsupported operation: {action}')

    @staticmethod
    def log_object(name, obj):
        logger.info(f'{name}: {json.loads(json.dumps(obj))}')

    @staticmethod
    def log_info(message):
        logger.info(message)

    @staticmethod
    def log_error(message):
        logger.error(message)