#!/usr/bin/python
from pwn import *

# Connection Info
host = 'localhost'
port = 4444

# Gadgets

# Addresses

# Exploit Function
def exploit(conn):
    payload = "A"*100
    conn.sendline(payload)
    conn.interactive()

if __name__=="__main__":
    conn = remote(host, port)
    exploit(conn)
