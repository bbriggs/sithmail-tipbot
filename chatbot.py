import logging
import threading
import configparser
from Legobot.Lego import Lego
from legos.stocks import Stocks
from legos.xkcd import XKCD
from legos.dice import Roll
from legos.wtf import WikipediaTopFinder
from legos.devopsy import Devopsy
from Legobot.Connectors.IRC import IRC
from Legobot.Legos.Help import Help

config = configparser.ConfigParser()
config.read('config.ini')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)

# Initialize lock and baseplate
lock = threading.Lock()
baseplate = Lego.start(None, lock)
baseplate_proxy = baseplate.proxy()

# Add children
baseplate_proxy.add_child(IRC,
                          channels=['#social'],
                          nickname=config['sithmail']['username'],
                          server=config['sithmail']['host'],
                          port=int(config['sithmail']['port']),
                          use_ssl=config.getboolean('sithmail','ssl'),
                          username=config['sithmail']['username'],
                          password=config['sithmail']['password'])
baseplate_proxy.add_child(Help)
baseplate_proxy.add_child(Roll)
baseplate_proxy.add_child(WikipediaTopFinder)
baseplate_proxy.add_child(XKCD)
baseplate_proxy.add_child(Devopsy)
baseplate_proxy.add_child(Stocks)
