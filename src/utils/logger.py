import logging
import sys


class Logger:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s  %(levelname)s:  %(message)s')

        self.consoleHandler = logging.StreamHandler(stream=sys.stdout)
        self.consoleHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.consoleHandler)

        self.fileHandler = logging.FileHandler(filename='log.txt', encoding='utf-8')
        self.fileHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.fileHandler)
