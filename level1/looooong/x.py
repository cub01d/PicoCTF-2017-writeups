from pwn import *
url = "shell2017.picoctf.com"
port = 51091

r = remote(url, port)
stuff = r.read()

#To prove your skills, you must pass this test.
#Please give me the 'B' character '763' times, followed by a single '0'.
#To make things interesting, you have 30 seconds.

character = stuff[67:68]
n = int(stuff[81:84])
singlestart = stuff.index('single')
singlec = stuff[stuff.index("'", singlestart) +1]

payload = character*n + singlec

r.sendline(payload)
r.interactive()

