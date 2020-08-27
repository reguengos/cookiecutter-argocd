import json
import logging
import os
from datetime import datetime

logging.addLevelName(25, 'TRACE')

class Log:
    def __init__(self):
        logging.basicConfig(format='%(message)s')
        self._logger = logging.getLogger('pipeline')
        log_level = os.environ.get('log_level', 'INFO').upper()
        self._logger.setLevel(log_level)
        self._context = {}

    def set(self, **kwargs):
        self._context = {**self._context, **kwargs}

    def trace(self, **kwargs):
        self.log('TRACE', **kwargs)

    def debug(self, **kwargs):
        self.log('DEBUG', **kwargs)

    def info(self, **kwargs):
        self.log('INFO', **kwargs)

    def warning(self, **kwargs):
        self.log('WARNING', **kwargs)

    def log(self, level, **kwargs):
        if isinstance(level, str):
            level_name = level
            level = logging.getLevelName(level)
        else:
            level_name = logging.getLevelName(level)

        fields = {
            'level': level_name.lower(),
            'occurred_at': datetime.utcnow().isoformat(),
            **self._context,
            **kwargs
        }
        self._logger.log(level, json.dumps(fields))


log = Log()