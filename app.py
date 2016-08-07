from logscan.match import Matcher
from logscan.watch import Watcher
from logscan.schedule import Schedule


if __name__ == '__main__':
    import sys
    sched = Schedule()
    try:
        sched.add_watcher(Watcher(sys.argv[1], Matcher('#123#')))
        sched.add_watcher(Watcher(sys.argv[2], Matcher('#123#')))
        sched.join()   # 因线程是daemon = True的，这里使用join方法是让主线程等待子线程运行结束后主线程才退出
    except KeyboardInterrupt:
        sched.remover_watcher(sys.argv[1])
        sched.remover_watcher(sys.argv[2])
    sched.join()
    """
    这里使用join方法是在“ctrl + c” 强制结束时，remover_watcher方法执行时因一些原因没有立刻执行完成而
    等待线程执行完成后主线程才退出，是一种清理现场的保险机制
    """

