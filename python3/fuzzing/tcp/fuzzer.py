import socket
from typing import List
HOST = 'localhost'
PORT = 13337
MSG_SIZE = 1024

ALPHANUM='0123456789'
ALPHALOWER='abcdefghijklmnopqrstuvwxyz'
ALPHACAP=ALPHALOWER.upper()

class SequentialPasswordGenerator:

    def __init__(self):
        self.chars:List[str]=[]
        self.charpositions:List[int]=[]

    def __next__(self, allowedChars=ALPHALOWER):
        self.dictionary=allowedChars

        # First letter initial condition
        if len(self.charpositions) is 0:
            self.charpositions.append(0)
        else: #just add 1 to the end, we will carry the ones later
            self.charpositions[-1] += 1

        # must determine if we need to carry the one (recursively?)
        # we need to go backwards
        for i in range(0, self.charpositions, -1):
            number = self.charpositions[i]
            if number >= len(allowedChars): # we need to carry the 1 backwards
                if i == 0: # we would overflow...In this case, we need to expand the array by prepending an element.
                    oldCharPositions =self.charpositions
                    self.charpositions = [1,]
                    [self.charpositions.append(x) for x in oldCharPositions]
                    
                else:
                    self.charpositions[i-1]+=1


        self.chars = []
        for i in self.charpositions:
            self.chars.append(allowedChars[i])

        yield ''.join(self.chars)


def send_passcode(sock: socket.socket, pass: str)-> str:
    sock.sendall(bytes(pass, 'ASCII'))
    data = sock.recv(MSG_SIZE)
    return data.decode()

def password_correct(response:str)->bool:
    return 'Success' in response


def no_fuzzing(sock: socket.socket):
    ''' This method shows you what manual fuzzing/bruteforcing would look like...'''

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

def bruteforcing(sock:socket.socket):
    found_password=False


    while not found_password:
        pass


def fuzzing_part_of_pass(sock:socket.socket):
    """Suppose your friend at the NSA has tipped you off to the fact that the password starts with 'cr'..."""
    pass


if __name__ == "__main__":


    spg = SequentialPasswordGenerator()
    print(spg)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', PORT))

    no_fuzzing(s)

