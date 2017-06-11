from Legobot.Lego import Lego
import logging

logger = logging.getLogger(__name__)

class Redis(Lego):
    def __init__(self, baseplate, lock, addr='localhost', port=6379, db=0, 
                 password=None, encoding='utf-8', charset='utf-8', 
                 *args, **kwargs):
        super().__init__(baseplate, lock)
        self.r = redis

    def set(self, key, value):
        return self.r.set(key, value)

    def get(self, key):
        return self.r.get(key).decode('utf-8')

    def update(self, key, value):
        return self.r.set(key, value, xx=True)

    def delete(self, key):
        return self.r.delete(key)

