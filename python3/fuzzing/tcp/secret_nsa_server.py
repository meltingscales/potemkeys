import socket
HOST = 'localhost'
PORT = 13337
MSG_SIZE = 1024

PASSCODE = "crabs"

# One bitcoin. Very valuable.
REWARD = """
                ______________
    __,.,---'''''              '''''---..._
 ,-'             .....:::''::.:            '`-.
'           ...:::.....       '
            ''':::'''''       .               ,
|'-.._           ''''':::..::':          __,,-
 '-.._''`---.....______________.....---''__,,-
      ''`---.....______________.....---''
"""

print(f"Waiting on port {PORT} for passcode {PASSCODE}...")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while 1:
    conn, addr = s.accept()
    print("Accepted connection!")
    try:
        while 1:
            conn.send(b"Give me the (max 1024-byte) passcode!")
            data = conn.recv(MSG_SIZE)

            if not data:
                print("Exiting!")
                break

            print("Received data:")
            asciidata = data.decode()
            print(asciidata)

            if PASSCODE == asciidata.strip():
                print(f"User chose right password '{asciidata}'.")
                conn.sendall(bytes("Success! Here is one bitcoin: "+REWARD, "ASCII"))
            else:
                conn.sendall(b"Failure! No bitcoins for you!")
    except ConnectionResetError as e:
        print(e)
        print("Client dropped.")
