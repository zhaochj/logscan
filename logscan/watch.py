import threading
from os import path
from queue import Queue
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from .match import Matcher


class Watcher(FileSystemEventHandler):
    def __init__(self, filename, counter):
        self.filename = path.abspath(filename)
        self.queue = Queue
        self.matchers = Matcher(self.queue, counter)
        #self.matcher = Matcher(checker.name, checker.expr)
        #self.checker = checker
        #self.counter = None
        self.queue = queue
        self.observer = Observer()
        self.fd = None   # fd 文件描述符缩写
        self.offset = 0
        if path.isfile(self.filename):
            self.fd = open(self.filename)
            self.offset = path.getsize(self.filename)   # offset指针指向文件末尾

    def on_deleted(self, event):
        if path.abspath(event.src_path) == self.filename:
            self.fd.close()

    def on_modified(self, event):
        if path.abspath(event.src_path) == self.filename:
            self.fd.seek(self.offset, 0)   # 移动文件游标
            '''
            self.matcher对象是Watcher类的构造方法所接收的参数，即是match模块中Matcher类的实例，
            getattr函数表示在Matcher类实例中有match方法，则把变量match指向match方法所在的地址，否
            则返回一个book值False（lambda x: False这个匿名函数返回False这个bool值）
            '''
            # match = getattr(self.matcher, 'match', lambda x: False)
            for line in self.fd:
                line = line.rstrip('\n')
                self.queue.put(line)
                # if self.matcher.match(line):   # 判断line这一行中的内容是否会被规则匹配到
                #     # print('matched {0}'.format(line))
                #     if self.counter is not None:
                #         self.counter.inc(self.matcher.name)   # 匹配计数
            self.offset = self.fd.tell()   # 获取到最新的游标位置

    def on_moved(self, event):
        # 此函数处理日志文件滚动情况
        if path.abspath(event.src_path) == self.filename:   # 当filename文件发生重命名时需要关闭文件描述符
            self.fd.close()
        if path.abspath(event.dest_path) == self.filename and path.isfile(self.filename):
            '''
            当监控的文件发生滚动后会再生成一个与原来文件名相同的文件，这时需要再把开此文件，
            并把offset游标指向此文件的最后。在上边的if语句中增加了一个判断生成文件是否是一个文件的条件，这样更严谨
            '''
            self.fd = open(self.filename)
            self.offset = path.getsize(self.filename)

    def on_created(self, event):
        if path.abspath(event.src_path) == self.filename and path.isfile(self.filename):
            self.fd = open(self.filename)
            self.offset == path.getsize(self.filename)

    def start(self):
        #t = threading.Thread(target=self.checker.check, name='Check-{0}'.format(self.checker.name))
        #t.start()
        """
         schedule监听一个路径并在调用适当的方法中指定一个event handler来响应 file system event。
         schedule方法接收三个参数，原型是schedule(event_handler, path, recursive=False),event_handler表示一个
         事件处理实例，有适当的事件处理方法响应file system event。Watcher类实例就是一个这样的类实例；第二个path参数
         表示监听的目录；第三个参数表示是否递归，True表示递归的遍历其子目录，False表示不会递归。返回一个ObservedWatch
         的对象实例
        """
        self.matchers.start()
        self.observer.schedule(self, path.dirname(self.filename), recursive=False)
        self.observer.start()
        """
         observer是观察者，调用start方法表示启动监听，在各个平台底层有不同的实现，
         参考：http://pythonhosted.org/watchdog/api.html#module-watchdog.observers
        """
        self.observer.join()   # 多线程时主线程会等待子线程结束

    def stop(self):
        self.matchers.stop()
        self.observer.stop()
        """
        fd.closed，当文件关闭时返回True，否则返回False
        """
        if self.fd is not None and not self.fd.closed:  # 判断当文件描述符不为None且又没有关闭时，执行close()操作
            self.fd.close()

if __name__ == '__main__':
    import sys

    class Matcher:
        def match(self, line):
            return True

    w = Watcher(sys.argv[1], Matcher())
    w2 = Watcher(sys.argv[2], Matcher())

    try:
        t1 = threading.Thread(target=w.start)
        t1.start()
        t2 = threading.Thread(target=w2.start)
        t2.start()
    except KeyboardInterrupt:
        w.stop()
        w2.stop()
