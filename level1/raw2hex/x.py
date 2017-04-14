import binascii

text = ""
with open("output", "r") as f:
	text = f.read()
# text[12:] contains the flag

flag = text[12:]
print "flag:", binascii.hexlify(flag)
