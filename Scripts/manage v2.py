from Scripts.BlockChainApi import app, start_up
import threading
import atexit

dataLock = threading.Lock()

thread = threading.Thread()


def create_app():
