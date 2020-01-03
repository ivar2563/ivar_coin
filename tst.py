import time
import logging

try:
    import simplejson as json
except ImportError:
    import json

from random import random


class IvarException(ValueError):
    def __init__(self, var, message):
        self.var = var
        self.message = message
        msg = "{} didn't work, and the message is '{}'".format(self.var, self.message)
        ValueError.__init__(self, msg)


class SomeContainer(object):
    def __init__(self, var):
        self.var = var

    def do_stuff(self):
        try:
            assert self.var > 0
            self.var -= 1
            raise IvarException(self.var, "Msg")

            # if random() > 0.95:
            #   raise IvarException(self)

        except IvarException as e:
            logging.info(e)
            print(e)


class KeyboardSubException(KeyboardInterrupt):

    def __init__(self, somearg):
        pass


try:
    while True:
        time.sleep(.5)

        assert False

except AssertionError:
    logging.info("Assertion error")
except KeyboardSubException:
    logging.info("Program quit")
except KeyboardInterrupt:
    pass
except Exception as e:
    logging.exception(e)
except IvarException():
    pass
finally:
    pass

x = SomeContainer(20)
x.do_stuff()
logging.info("Good bye")
