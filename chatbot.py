import logging
import threading
import configparser
from Legobot.Lego import Lego
from legos.stocks import Stocks
from legos.xkcd import XKCD
from legos.dice import Roll
from legos.wtf import WikipediaTopFinder
from legos.ctftime import CTFtime
from Legobot.Connectors.IRC import IRC
from Legobot.Legos.Help import Help
from Local.Tip import Tip
from Local.magic8ball import Magic8ball
from Local.greetings import Greetings
from Local.markov import MarkovListener
from Local.markov import MarkovGenerator

import redis

config = configparser.ConfigParser()
config.read('config.ini')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)

# Initialize lock and baseplate
lock = threading.Lock()
baseplate = Lego.start(None, lock)
baseplate_proxy = baseplate.proxy()

r = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

# Add children
baseplate_proxy.add_child(IRC,
                          channels=[channel.strip() for channel in config.get(
                              "sithmail", "channels").split(",")],
                          nickname=config['sithmail']['username'],
                          server=config['sithmail']['host'],
                          port=int(config['sithmail']['port']),
                          use_ssl=config.getboolean('sithmail', 'ssl'),
                          username=config['sithmail']['username'])
baseplate_proxy.add_child(Help)
#baseplate_proxy.add_child(Roll)
#baseplate_proxy.add_child(WikipediaTopFinder)
#baseplate_proxy.add_child(XKCD)
#baseplate_proxy.add_child(Stocks)
#baseplate_proxy.add_child(Tip, r)
#baseplate_proxy.add_child(Magic8ball, r)
#baseplate_proxy.add_child(CTFtime)
#baseplate_proxy.add_child(Greetings)
baseplate_proxy.add_child(MarkovListener, r)
baseplate_proxy.add_child(MarkovGenerator, r)
