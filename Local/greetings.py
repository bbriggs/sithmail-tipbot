import logging
import json
import requests
import random
from Legobot.Lego import Lego

logger = logging.getLogger(__name__)

class Greetings(Lego):
    """Class to hold all factoids
    Args: Lego
    """
    def listening_for(self, message):
        """Checks if the message contains a command that we need to execute
        Args:
            self:
            message: The complete line/message that comes from an IRC channel

        Returns:
            Bool: Returns true if the first word in the message is a command for this class
        """
        cmds = ['!gray', 'zapp', 'ay', 'yo', 'sup', 'suh', 'hi', 'wassup', 'yarg', 'moin',
                'bye', 'cya']
        return message['text'].split()[0] in cmds

    def handle(self, message):
        """Execute the needed command
        Args:
            self:
            message: The complete line/message that comes from an IRC channel

        Returns:
            string: Returns the suitable factoid
        """
        opts = None
        logger.info(message)
        try:
            target = message['metadata']['source_channel']
            opts = {'target':target}
        except IndexError:
            logger.error('Could not identify message source in message: %s' % str(message))
        command = message['text'].split()[0]
        if command == "!gray":
            responses = ["Well I'm a paint my picture, Paint myself in blue, red, black and gray",
                         "All of the beautiful colors are very, very meaningful",
                         "Yeah, well you know, gray is my favorite color",
                         "I felt so symbolic yesterday",
                         "If I knew Picasso, I would buy myself a gray guitar and play",
                         "Sha la, la, la, la, la, la, la",
                         "Cut up, Maria. Show me some of them Spanish dances", 
                         "Pass me a bottle, Mr. Jones",
                         "Mr. Jones and me tell each other fairy tales",
                         "https://www.youtube.com/watch?v=-oqAU5VxFWs"]
            txt = random.choice(responses)
        elif command == "zapp":
            responses = ["Brannigan's law is like Brannigan's love: hard and fast.",
                         "If we can hit that bullseye the rest of the dominoes will fall like a house of cards: checkmate!",
                         "I am the man with no name. Zapp Brannigan at your service.",
                         "Now remember, Kif, the quickest way to a girl's bed is through her parents. Have sex with them and you're in.",
                         "I surrender and volunteer for treason.",
                         "She's built like a steakhouse but she handles like a bistro.",
                         "When I'm in command, every mission is a suicide-mission.",
                         "In the game of chess, never let your adversary see your pieces.",
                         "Champ-paggin'"]
            txt = random.choice(responses)
        elif command == 'moin':
            txt = 'moin {}'.format(message['metadata']['source_username'])
        elif command in ['ay', 'yo', 'sup', 'hi', 'wassup']:
            responses = ['suh dude', 'yo', 'hey {}'.format(message['metadata']['source_username']), 
                         'howzit', 'sup', 'sup {}'.format(message['metadata']['source_username']),
                         'ayyyyy', 'welcome!']
            txt = random.choice(responses)
        elif command in ['bye', 'cya']:
            responses = ['o/', 'later']
            txt = random.choice(responses)
        elif command == 'yarg':
            txt = 'new phone who dis'
        self.reply(message, txt, opts)
