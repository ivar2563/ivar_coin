import multiprocessing
import time
import threading
from threading import Lock


mutex = Lock()

start = time.perf_counter()
def do_somthing(num):
    mutex.acquire()
    print(num)
    time.sleep(num)
    mutex.release()



if __name__ == "__main__":
    x = threading.Thread(target=do_somthing, args=(2,))
    x2 = threading.Thread(target=do_somthing, args=(5,))
    x3 = threading.Thread(target=do_somthing, args=(1,))
    x4 = threading.Thread(target=do_somthing, args=(12,))
    x.start()
    x2.start()
    x3.start()
    x4.start()
    x.join()
    x2.join()
    x3.join()
    x4.join()

    finish = time.perf_counter()
    print(round(finish - start, 2))