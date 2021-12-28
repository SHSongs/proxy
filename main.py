import socket
import select
import sys
from forward import get_forward_sock

buffer_size = 4096


def verify_request(data):
    if len(data) == 0:
        return None

    request_data = data.decode('utf-8')
    request_data = request_data.split(' ')

    request_method = request_data[0]
    if request_method != "GET":
        print("요청방법이 올바르지 않습니다")
        return None
    else:
        return request_data


def get_key_from_request(data):
    try:
        return int(data[1].split('/')[1])
    except:
        return None


def remove_server_name_from_get_request(request_data):
    tmp = request_data[1].split('/')[2:]
    request_data[1] = '/' + '/'.join(tmp)
    request_data = ' '.join(request_data)
    data = bytes(request_data, encoding="utf-8")
    print(data)
    return request_data


class TheServer:
    input_list = []
    channel = {}

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)
        self.client_sock_lst = []

    def main_loop(self):
        self.input_list.append(self.server)

        while True:
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for s in inputready:
                if s == self.server:
                    self.on_accept(s)
                    break

                if s not in self.client_sock_lst:
                    data = s.recv(buffer_size)
                    if len(data) == 0:
                        self.on_close(s)
                        break
                    else:
                        self.on_recv(s, data)

    def on_accept(self, s):
        clientsock, clientaddr = self.server.accept()
        self.client_sock_lst.append(clientsock)

        data = clientsock.recv(buffer_size)

        request_data = verify_request(data)
        if request_data is None:
            self.on_close(s)
            return

        key = get_key_from_request(request_data)
        if key is None:
            return

        request_data = remove_server_name_from_get_request(request_data)
        data = bytes(request_data, encoding="utf-8")
        print(data)

        forward = get_forward_sock(key)
        if forward:
            print("{0} has connected".format(clientaddr))
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock
            self.on_recv(clientsock, data)
        else:
            print("Can't establish a connection with remote server. Closing connection with client side {0}".format(
                clientaddr))
            clientsock.close()

    def on_close(self, s):  #
        print("{0} has disconnected".format(s.getpeername()))
        self.client_sock_lst.remove(self.channel[s])
        # remove objects from input_list
        self.input_list.remove(s)
        self.input_list.remove(self.channel[s])
        out = self.channel[s]
        # close the connection with client
        self.channel[out].close()
        # close the connection with remote server
        self.channel[s].close()
        # delete both objects from channel dict
        del self.channel[out]
        del self.channel[s]

    def on_recv(self, s, data):
        # here we can parse and/or modify the data before send forward
        print(data)
        self.channel[s].send(data)


if __name__ == '__main__':
    server = TheServer('', 9090)
    try:
        server.main_loop()
    except KeyboardInterrupt:
        print("Ctrl C - Stopping server")
        sys.exit(1)
