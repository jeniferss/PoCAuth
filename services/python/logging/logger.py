import logging
import sys

# Define logger colors
logging.addLevelName( logging.DEBUG, "\x1b[1;38m%s\x1b[1;0m" % logging.getLevelName(logging.DEBUG))
logging.addLevelName( logging.INFO, "\x1b[1;34m%s\x1b[1;0m" % logging.getLevelName(logging.INFO))
logging.addLevelName( logging.WARNING, "\x1b[1;33m%s\x1b[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.ERROR, "\x1b[1;31m%s\x1b[1;0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName( logging.CRITICAL, "\x1b[1;41m%s\x1b[1;0m" % logging.getLevelName(logging.CRITICAL))

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler and set level to debug
channel = logging.StreamHandler(sys.stdout)
channel.setLevel(logging.DEBUG)

# Create formatter
STRING = '%(levelname)-21s | %(asctime)s [%(filename)s:%(lineno)s]: %(message)s'
DATE = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(STRING, datefmt=DATE)

# Add formatter to channel
channel.setFormatter(formatter)

# Add channel to logger
logger.addHandler(channel)


logger.debug('Mensagem qualquer')
logger.error('Mensagem qualquer')
logger.info('Mensagem qualquer')
logger.warning('Mensagem qualquer')