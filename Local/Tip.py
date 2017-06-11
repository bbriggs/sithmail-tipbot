from Legobot.Lego import Lego
import logging

logger = logging.getLogger(__name__)


class Tip(Lego):
    def __init__(self, baseplate, lock, redis, *args, **kwargs):
        super().__init__(baseplate, lock)
        self.r = redis  # initialized redis connection
        self.prefix = "/kudos"

    def listening_for(self, message):
        if message['text'] is not None:
            # Only care if first "word" is a ++ or --
            return self._is_incr(message['text'].split()[0])

    @staticmethod
    def _is_incr(cmd):
        return cmd.endswith('++') or cmd.endswith('--')

    def handle(self, message):
        opts = self._handle_opts(message)
        cmd = message['text'].split()[0]
        return_val = "this is a default return val"
        if self._is_incr(cmd):
            resp = self._incr(cmd)
            if resp is not False:
                return_val = "{} has {} meaningless internet points.".format(
                    cmd[:-2], resp)
            else:
                logger.debug(str(resp))
                return_val = "Redis is sleeping right now."
        self.reply(message, return_val, opts)

    def _incr(self, cmd):
        target = cmd[:-2]
        if cmd.endswith("++"):
            # lol you can create nested keys
            resp = self.r.incr('{}/{}'.format(self.prefix, target))
            logger.debug("Redis increment: {}".format(str(resp)))
            return resp
        elif cmd.endswith("--"):
            resp = self.r.decr('{}/{}'.format(self.prefix, target))
            logger.debug("Redis decrement: {}".format(str(resp)))
            return resp
        else:
            return False

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
        return 'tip'

    def get_help(self):
        return 'Tip some imaginary internet points'
