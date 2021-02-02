from threading import Timer


class Throttle:
    def __init__(self, task, batchSize=50, delay=0.5):
        if not task:
            raise Exception("Task has not assigned")
        self.task = task
        self.batchSize = batchSize
        self.delay = delay
        self.timer = None
        self.queue = {}

    def do(self, data, done):
        if not done:
            raise Exception("Done has not assigned")
        self.queue[data] = done
        if len(self.queue) >= self.batchSize:
            self.wrappedTask()
        else:
            if self.timer:
                timer = self.timer
                self.timer = None
                timer.cancel()
                del timer
            self.timer = Timer(self.delay, self.wrappedTask)
            self.timer.start()

    def wrappedTask(self):
        if self.timer:
            timer = self.timer
            self.timer = None
            timer.cancel()
            del timer
        if len(self.queue) == 0:
            return
        queue = self.queue
        self.queue = {}
        for (data, done) in queue.items():
            done(self.task(data))
        del queue


if __name__ == "__main__":
    import time

    def printAndReturn(a):
        print("start: " + str(a))
        return a

    throttle = Throttle(printAndReturn, 3)
    throttle.do("1", done=lambda a: print("done1: " + str(a)))
    throttle.do("2", done=lambda a: print("done1: " + str(a)))
    throttle.do("2", done=lambda a: print("done1: " + str(a)))
    time.sleep(1)
    throttle.do("3", done=lambda a: print("done1: " + str(a)))
    time.sleep(1)
    throttle.do("4", done=lambda a: print("done1: " + str(a)))
    time.sleep(0.2)
    throttle.do("5", done=lambda a: print("done2: " + str(a)))
    time.sleep(0.3)
    throttle.do("6", done=lambda a: print("done2: " + str(a)))
    time.sleep(0.4)
    throttle.do("7", done=lambda a: print("done2: " + str(a)))
    time.sleep(0.5)
    throttle.do("8", done=lambda a: print("done2: " + str(a)))
    time.sleep(1)
    throttle.do("9", done=lambda a: print("done2: " + str(a)))
