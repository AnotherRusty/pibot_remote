import socket, sys
from time import sleep

HOST = '192.168.11.128'
# HOST = '172.20.10.3'
PORT = 8998

BOF = 0x5a
EOF = 0x0a

class TestMessage():
    def __init__(self):
        self.id = 2
        self.len = 0
     
    def pack(self):
        bof = bytes(bytearray([BOF]))
        eof = bytes(bytearray([EOF]))
        msg_id = bytes(bytearray([self.id]))
        msg_len = bytes(bytearray([self.len]))
        p = bof + msg_id + msg_len + eof
        return p

socks = [socket.socket(), socket.socket()]
try:
    for sock in socks:
        sock.connect((HOST, PORT))
        print('connected to server')
    
    # for i in range(2):
    #     for sock in socks:
    #         sock.send(TestMessage().pack())
    #     sleep(2)
    while True:
        for sock in socks:
            data = sock.recv(1)
            print repr(data)

except Exception as e:
    print(e)
    sock.close()
    print("error! disconnect")
    sys.exit()

