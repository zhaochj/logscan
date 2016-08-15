import threading
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s')


def worker(message):
    print('exec worker')
    time.sleep(5)
    logging.debug("worker is started, {0}".format(message))

if __name__ == '__main__':
    t = threading.Thread(target=worker, name='worker', kwargs={'message': 'ha,ha'})
    t.daemon = True
    t.start()
    t.join(timeout=3)
    logging.debug("main thread exiting")


