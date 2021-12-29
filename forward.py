import socket

forward_to_dict = {8000: ('127.0.0.1', 8000), 10000: ('127.0.0.1', 10000)}


def get_forward_sock(key):
    try:
        forward_to = forward_to_dict[key]
        print("forward_to: ", forward_to)
        return Forward().start(forward_to[0], forward_to[1])
    except KeyError:
        print("value is not found")
        return None


class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception as inst:
            print("[exception] - {0}".format(inst.strerror))
            return False
