import threading
import logging
import time


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s')


def worker(message):
    logging.debug("worker is started, {0}".format(message))


if __name__ == '__main__':
    #logging.debug("i am main thread")
    #t = threading.Thread(target=worker, name='worker', args=('ha ha',))
    t = threading.Thread(target=worker, name='worker', kwargs={'message': 'ha,ha'})
    t.daemon = True
    t.start()
    t.join()
    logging.debug("main thread exiting")


