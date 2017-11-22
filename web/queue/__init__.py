from time import sleep, time, strftime
from threading import Thread
from datetime import timedelta

class Queue():
    def __init__(self, time = 10*60, sleep_time = 0):
        self.line = []
        self.time = time

        self.stopped = False
        self.current_user = None

        self.sleep_time = sleep_time
        self.thread = None

        self.time_left = self.time

        self.start()

    def addUser(self, user):
        self.line.append(user)

    def currentUsersNumber(self):
        return len(self.line)

    def getCurrentUser(self):
        return self.current_user

    def timeLeft(self):
        initial = time()

        last = self.time + initial
        self.time_left = last - time()

        while self.time_left > 0:
            self.time_left = last - time()
            sleep(0.1)

    def setCurrentUser(self):
        if self.currentUsersNumber() > 0:
            self.current_user = self.line[0]
            thread = Thread(target = self.timeLeft)
            thread.start()
            sleep(self.time + 1)
        else:
            self.current_user = None
            self.time_left = 0
            sleep(self.sleep_time)

        if self.current_user != None:
            del self.line[0]

    def positionInLine(self, user):
        try:
            return self.line.index(user) + 1
        except:
            return -1

    def userInLine(self, user):
        try:
            self.line.index(user)
            return True
        except:
            return False

    def spectedTime(self, user):
        pos = self.positionInLine(user) - 1
        if pos > 0:
            time_ = (pos-1)*self.time + self.time_left
            a = timedelta(seconds = round(time_, 0))

            return pos, str(a)
        else:
            return pos, "0:00:00"

    def permanent(self):
        while not self.stopped:
            self.setCurrentUser()

    def start(self):
        if self.thread == None:
            self.thread = Thread(target=self.permanent)
            # self.thread.daemon = True
            self.thread.start()
        else:
            self.thread.start()

    def stop(self):
        self.Thread = None
        self.stopped = True

# queue = Queue(10)
#
# usrs = ["MrPotato", "MrsPotato", "Bananaas", "MeVale"]
# for usr in usrs:
#     queue.addUser(usr)
#
# sleep(1e-3)
# for i in range(100):
#     temp = [queue.spectedTime(usr) for usr in queue.line]
#     print(temp, queue.current_user)
#     sleep(1)
# queue.stop()
