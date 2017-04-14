c = p = q = dp = dq = 0

with open("RSA.txt", "r") as f:
	[c, p, q, dp, dq] =  [long(x.strip()[3:]) for x in f.readlines()]

def int2Text(number, size):
	text = "".join([chr((number >> j) & 0xff)
		for j in reversed(range(0, size << 3, 8))])
	return text.lstrip("\x00")

pc = pow(c,dp, p)
qc = pow(c, dq, q)
for i in range(40):
	print int2Text(pc, i), int2Text(qc, i)
