import socket
import threading
import time


class ServerControl(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.HEADER = 64
        self.PORT = 5051
        # self.SERVER = socket.gethostbyname(socket.gethostname())
        # print(self.SERVER)
        self.SERVER = '0.0.0.0'
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.ADDR)
        self.message = None
        self.connected = True
        self.conn = None

    def get_message(self):
        if self.message:
            send_message = self.message
            self.message = None
            return send_message
        else:
            return None

    def send_message(self, msg):
        if msg:
            self.handle_send(msg)

    def server_disconnect(self):
        self.connected = False

    def handle_receive(self, conn, addr):
        print("[NEW CONNECTION] {} connected.".format(addr))
        self.connected = True
        conn.settimeout(10000)
        while self.connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.FORMAT)
                if msg == self.DISCONNECT_MESSAGE:
                    self.connected = False
                self.message = msg
                # print(self.message)

        conn.close()

    def handle_send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        print(send_length)
        self.conn.send(send_length)
        print(message)
        self.conn.send(message)

    def run(self):
        self.server.listen(5)
        print("[LISTENING] Server is listening on {}".format(self.SERVER))
        wait_connection = True
        while wait_connection:
            conn, addr = self.server.accept()
            self.conn = conn
            rec_thread = threading.Thread(target=self.handle_receive, args=(conn, addr))
            rec_thread.start()
            wait_connection = False

    def __del__(self):
        self.connected = False
        time.sleep(0.5)


if __name__ == '__main__':
    print("[STARTING] server is starting...")
    new_server = ServerControl()
    new_server.start()
