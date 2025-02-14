import logging
from logging import NullHandler

__version__ = "0.1.0"

# logger to be using by the app, shouldn't initialise if this lib is used as a lib
# https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
logging.basicConfig(level=logging.ERROR, format="%(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("linkwarden_companion")
logger.addHandler(NullHandler())
