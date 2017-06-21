from Legobot.Lego import Lego
import logging
import random

logger = logging.getLogger(__name__)


class Magic8ball(Lego):
    def __init__(self, baseplate, lock, redis, *args, **kwargs):
        super().__init__(baseplate, lock)
        self.r = redis  # initialized redis connection
        self.fortunes = "/eight-ball"

    def listening_for(self, message):
        if message['text'] is not None:
            # Only care if first "word" is a ++ or --
            return message['text'].split()[0] == '!8ball'

    def handle(self, message):
        opts = self._handle_opts(message)
        splitmessage = message['text'].split()
        if len(splitmessage) > 1 and splitmessage[1] == "add":
            return_val = self._set(splitmessage[1:])
        else:
            return_val = self._get()
        self.reply(message, return_val, opts)

    def _get(self):
        try:
            resp = self.r.srandmember(self.fortunes).decode('utf-8')
        except Exception as e:
            logger.error("An error occurred while attempting to read from Redis: {}".format(e))
            return "Outlook cloudy. Redis sucks. Try again later."
        if resp is not None:
            return resp
        else:
            logger.error("Redis returned a None when asked for a fortune")
            return "The magical 8-ball has heard no prayers. Perhaps you should offer advice to those who come after you."

    def _set(self, fortune):
        if len(fortune) > 1:
            fortune = " ".join(fortune[1:])
        else:
            return "Your advice to those who seek supplication must have actual words..."
        try:
            resp = self.r.sadd(self.fortunes, fortune)
        except Exception as e:
            logger.error("Error while attempting to write to Redis: {}".format(e))
        if resp == 1:
            return "Your plea to the gods of randomness has been received."
        elif resp == 0:
            logger.warn("Duplicate value received for 8ball set: {}".format(fortune))
            return "That plea is one I have heard before."
        else:
            logger.error("Unable to write to Redis: {}".format(resp))
            return "Your prayers have been ignored by the gods."

    def _handle_opts(self, message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target': target}
        except IndexError:
            opts = None
            logger.error('''Could not identify message source in message:
                        {}'''.format(str(message)))
        return opts

    def get_name(self):
        return '8ball'

    def get_help(self):
        return 'Shake the magic 8-ball and see what happens. Usage: !8ball. Add a response: !8ball add <message>'
