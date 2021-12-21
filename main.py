# https://gist.github.com/voorloopnul/415cb75a3e4f766dc590#file-proxy-py

# !/usr/bin/python
# This is a simple port-forward / proxy, written using only the default python
# library. If you want to make a suggestion or fix something you can contact-me
# at voorloop_at_gmail.com
# Distributed over IDC(I Don't Care) license
import socket
import select  # I/O 멀티 플렉싱을 위해 사용
import time
import sys

# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
buffer_size = 4096
delay = 0.0001
forward_to_dict = {8000: ('127.0.0.1', 8000), 10000: ('127.0.0.1', 10000)}


class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception as e:
            print(e)
            return False


class TheServer:
    input_list = []
    channel = {}

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)

    def main_loop(self):
        self.input_list.append(self.server)
        while 1:
            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
                if self.s == self.server:
                    self.on_accept()
                    break

                data = self.s.recv(buffer_size)
                if len(data) == 0:
                    self.on_close()
                    break
                else:
                    self.on_recv(data)

    def on_accept(self):
        clientsock, clientaddr = self.server.accept()

        data = clientsock.recv(buffer_size)
        request_data = data.decode().split()
        request_method = request_data[0]

        if request_method == "GET":
            pass
        else:
            print("요청방법이 올바르지 않습니다")
            return

        key = int(request_data[1][1:])
        forward_to = forward_to_dict[key]
        print("forward_to: ", forward_to)
        forward = Forward().start(forward_to[0], forward_to[1])
        print(forward)

        if forward:
            print(clientaddr, "has connected")
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock

            if len(data) == 0:
                print("close")
            else:
                self.on_recv(data)


        else:
            print("Can't establish connection with remote server.", end=' ')
            print("Closing connection with client side", clientaddr)
            clientsock.close()

    def on_close(self):
        print(self.s.getpeername(), "has disconnected")
        # remove objects from input_list
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        # close the connection with client
        self.channel[out].close()  # equivalent to do self.s.close()
        # close the connection with remote server
        self.channel[self.s].close()
        # delete both objects from channel dict
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self, data):
        # here we can parse and/or modify the data before send forward
        print(data.decode('utf-8').split(' '))
        self.channel[self.s].send(data)


if __name__ == '__main__':
    server = TheServer('', 9090)
    try:
        server.main_loop()
    except KeyboardInterrupt:
        print("Ctrl C - Stopping server")
        sys.exit(1)
