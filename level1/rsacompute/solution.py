# RSA encryption/decryption is based on a formula that anyone can find 
# and use, as long as they know the values to plug in. Given the 
# encrypted number 150815, d = 1941, and N = 435979, what is the 
# decrypted number?

c = 150815
d = 1941
N = 435979

print "flag:", c**d % N
