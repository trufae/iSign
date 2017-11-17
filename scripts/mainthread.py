import threading
from client import Client

class mainThread(threading.Thread):
    client = None
    def __init__(self, threadID, client):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.client = client
    def run(self):
        pass