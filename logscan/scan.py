from .schedule import Schedule


class Scan:
    def __init__(self):
        self.schedule = Schedule('/tmp/counter.db')

    def watch(self):
        #TODO wathch zookeeper
        pass
