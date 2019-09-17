# CSAW2019Quals
Writeups for the challenges I solved for the CSAW 2019 Qualifying CTF

## Template.py
Since my focus is in binary exploitation, I've created a template python script using pwntools.

# Writeups

## baby_boi [pwn - 50]

### Information Gathering
For this challenge, they give you the source code so it's really easy to find the vulnerability (no need for reversing).
They give you a buffer that's 32 bytes in length, print out the address of printf, and call gets on it. 
Since this function has no protection (no check for buffer overflow), you can send as many bytes as you 
like before a newline or EOF as that's where it'll stop reading. Additionally, they give us a libc, so we can calculate
the offsets accordingly.

### Vulnerability: Buffer Overflow into Ret2Libc

### Crafting The Exploit
1. We need to capture the address that they give us and save it. This is important because we'll use this to calculate
the base address of libc.
2. Since this program is 64-bit and the buffer is of size 32, we need to send 40 bytes in order to get to the return address.
This is because the saved base pointer is on the stack right before the return pointer.
3. Next, we find the offset of printf in the libc. This can be done with "readelf -s libc-2.27.so | grep printf" and finding 
the right printf. It'll look something like this `0000000000064e80   195 FUNC    GLOBAL DEFAULT   13 printf@@GLIBC_2.2.5`
4. We use the address we captured in the first step, subtract the offset, and this is our libc base address.
5. Now we have every function in libc at our disposal. So let's run a one_gadget on it to find something useful. This yields `0x4f2c5 execve("/bin/sh", rsp+0x40, environ)
constraints:
  rcx == NULL` 
6. Take that offset, add it onto the libc base address, and add the result in the payload.
7. Send our payload and use pwntools interactive to get a shell and cat out the flag :-)
8. pwned


## small_boi [pwn - 100]

### Information Gathering
For this challenge, all they give you is a very small binary. It doesn't even have a main function. It goes into the entry function
and then calls another function. This will read in 0x200 bytes from STDIN using the `syscall` assembly instruction. We again have a buffer
that's only 32 bytes in size (indicated by the rbp-0x20 or just brute forcing to see what makes it crash). My initial thought is
that it'll be a relatively simple ROP, provided we are given the correct gadgets. After running ROPgadget on it, I was able to call the syscall
`execve`, because we have the "pop rax; ret" gadget, allowing us to put anything in the rax register. However, there is no gadget in
this program that will let us set the rdi register, the first parameter to the syscall (we'd want to pass it the address of the string "/bin/sh",
which also exists in the program). After beating my head against the wall for a little bit, I reached out to one of my teammates and asked for 
some input. He suggested it might be a SigROP, which is something I hadn't learned before. I did some research to figure out what it is and
how it works, and luckily pwntools has a whole suite of SigROP tools.

### Vulnerability: Buffer Overflow into SigROP

### Crafting the exploit
1. Save the addresses of the necessary gadgets in the python program. I did this using `ROPgadget --binary small_boi`.
The ones we'll need are `pop_rax; ret` and `syscall`.
2. We'll also need the address of the string "/bin/sh", which exists in the program. I got this by using `objdump -s small_boi | grep /bin`
3. Since the buffer is 32 bytes long, we'll again need to send 40 bytes to overwrite the saved base pointer.
4. We use the pop_rax register to set rax = 15 (to call [sigreturn](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/))
5. We then call the syscall
6. Next, we setup our SigReturn frame. This will set the registers accordingly for what to do when the SigReturn is triggered.
7. Set rax = 59 for `execve`
8. Set rdi = *address of binsh* (since it's the first parameter into the call)
9. Set rip = syscall to execute the syscall
10. Stringify our frame and tack it onto the end of the payload.
11. Send our payload and use pwntools interactive to get a shell and cat out the flag :-)
12. pwned
