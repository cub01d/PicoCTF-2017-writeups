#!/usr/bin/python -u
import random,string

ct = "BNZQ:3o8b2bgl0689u4aj640407963277k0fc"

random.seed("random")
# randints = [random.randrange(0,26) for i in range(len(ct))]


flag = ""
for c in ct:
  if c.islower():
#    flag += chr((ord(c)-ord('a')+random.randrange(0,26))%26 + ord('a'))
    flag += chr((ord(c)-ord('a')-random.randrange(0,26))%26 + ord('a'))
  elif c.isupper():
#    flag += chr((ord(c)-ord('A')+random.randrange(0,26))%26 + ord('A'))
    flag += chr((ord(c)-ord('A')-random.randrange(0,26))%26 + ord('A'))
  elif c.isdigit():
#    flag += chr((ord(c)-ord('0')+random.randrange(0,10))%10 + ord('0'))
    flag += chr((ord(c)-ord('0')-random.randrange(0,10))%10 + ord('0'))
  else:
    flag += c
print "Unguessably Randomized Flag: "+flag
