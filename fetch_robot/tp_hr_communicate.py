import server
import time


class HRInterface:
    def __init__(self):
        self.fetch_server = server.ServerControl()
        # self.human_server.daemon = True
        self.fetch_server.start()
        # time.sleep(2)
        self.received_msg = None
        self.sent_msg = None
    #
    def send_msg(self, msg):
        self.fetch_server.send_message(msg)

    def receive_msg(self):
        self.received_msg = self.fetch_server.get_message()
        return self.received_msg


if __name__ == '__main__':
    hrint = HRInterface()
    while True:
        a = hrint.receive_msg()
        if a:
            print(a)
            break
    hrint.send_msg('hhh')

