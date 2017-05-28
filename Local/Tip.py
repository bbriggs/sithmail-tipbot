from Legobot.Lego import Lego
import logging

logger = logging.getLogger(__name__)


class Tip(Lego):
    def __init__(self, baseplate, lock, redis, *args, **kwargs):
        super().__init__(baseplate, lock)
        self.r = redis  # initialized redis connection

    def listening_for(self, message):
        cmds = ['!tip']
        if message['text'] is not None:
            try:
                return message['text'].split()[0] in cmds
            except Exception as e:
                logger.error('''tip lego failed to check message text:
                            {}'''.format(e))
                return False

    def handle(self, message):
        opts = self._handle_opts(message)
        command = message['text'].split()[0]
        return_val = 'nothing wrote over this'
        if command == '!tip':
            try:
                tip_target = message['text'].split()[1]
                tip_val = message['text'].split()[2]
            except IndexError as e:
                logger.error("!tip called with insufficient arguments: \
                             {}".format(e))
                return_val = 'Insufficient arguments. Usage: !tip nick amount'
                self.reply(message, return_val, opts)
                return

            return_val = self.add(tip_target, tip_val)
            logger.debug('\n\n' + return_val + '\n\n')

        self.reply(message, return_val, opts)

    def add(self, nick, value):
        old_value = self.r.get('tips/' + nick)
        if old_value is None:
            old_value = 0
        else:
            old_value = int(old_value.decode('utf-8'))
        try:
            sum = old_value + int(value)
        except Exception as e:
            logger.error("Unable to add tip values for {}.".format(nick))
            logger.error(e)
            return "I can't math today."
        response = self.r.set('tips/' + nick, sum)
        if response is not False:
            return "{0} has {1} meaningless internet points.".format(
                nick, str(sum))
        else:
            logger.error('Could not write to redis backend in tip lego: '
                         + response)
            return "Unable to write tips at this this time."

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
