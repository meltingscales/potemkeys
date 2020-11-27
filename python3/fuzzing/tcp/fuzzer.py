import collections
import socket
from typing import List, Iterator

HOST = 'localhost'
PORT = 13337
MSG_SIZE = 1024

ALPHANUM = '0123456789'
ALPHALOWER = 'abcdefghijklmnopqrstuvwxyz'
ALPHACAP = ALPHALOWER.upper()


class SequentialPasswordGenerator:

    def __init__(self,allowedChars=ALPHALOWER):
        self.chars: List[str] = []
        self.charpositions: List[int] = []
        self.dictionary = allowedChars

    def __iter__(self):
        while True:
            # First letter initial condition
            if len(self.charpositions) is 0:
                self.charpositions.append(0)
            else:  # just add 1 to the end, we will carry the ones later
                self.charpositions[-1] += 1

            # must determine if we need to carry the one (recursively?)
            # we need to go backwards
            for i in range(len(self.charpositions)-1, -1, -1):

                number = self.charpositions[i]
                if number >= len(self.dictionary):  # we need to carry the 1 backwards
                    if i == 0:  # We're at the largest digit.
                        # we would overflow...In this case, we need to expand the array by prepending an element.
                        oldCharPositions = self.charpositions
                        self.charpositions = [1, ]
                        [self.charpositions.append(x) for x in oldCharPositions]
                        self.charpositions[1] = 0 # it's a 0 now, leave the other digits alone

                    else:
                        self.charpositions[i - 1] += 1

                        # TODO check if we are going to overflow


            self.chars = []
            for k in self.charpositions:
                self.chars.append(self.dictionary[k])

            yield ''.join(self.chars)


def send_passcode(sock: socket.socket, password: str) -> str:
    sock.sendall(bytes(password, 'ASCII'))
    data = sock.recv(MSG_SIZE)
    return data.decode()


def password_correct(response: str) -> bool:
    return 'Success' in response


def no_fuzzing(sock: socket.socket):
    """ This method shows you what manual fuzzing/bruteforcing would look like..."""

    response = send_passcode(sock, "password123")
    if password_correct(response):
        print("We got a bitcoin!")
        print(response)
        exit(0)
    else:
        print("Wrong password...")
        print("Response from server:")
        print(response)

    response = send_passcode(sock, "admin123")
    if password_correct(response):
        print("We got a bitcoin!")
        print(response)
        exit(0)
    else:
        print("Wrong password...")
        print("Response from server:")
        print(response)

    '''...etc...'''


def bruteforcing(sock: socket.socket):
    found_password = False

    while not found_password:
        pass


def fuzzing_part_of_pass(sock: socket.socket):
    """Suppose your friend at the NSA has tipped you off to the fact that the password starts with 'cr'..."""
    pass


if __name__ == "__main__":
    spg = SequentialPasswordGenerator()
    print(spg)

    i = 0
    for password in spg:
        print(password)
        print(i)
        i+=1

    exit(0)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', PORT))

    no_fuzzing(s)
