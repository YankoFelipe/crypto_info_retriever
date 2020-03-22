import sched
import time

s = sched.scheduler(time.time, time.sleep)


def do_something(sc):
    print("palta")
    s.enter(1, 1, do_something, ('first',))


s.enter(1, 1, do_something, ('first',))

s.run()
