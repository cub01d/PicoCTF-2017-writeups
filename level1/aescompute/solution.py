# Encrypted with AES in ECB mode. All values base64 encoded
# ciphertext = ACw5ftWAMhGPpxkbT1iun8aLQ55rGrYUMjeyZfIlYd8Whz8TwCMg1AgeTA83J7qt
# key = zb9v8uGYo/BWzbhouenY2g==

from Crypto.Cipher import AES
from base64 import b64decode

ciphertext = b64decode("ACw5ftWAMhGPpxkbT1iun8aLQ55rGrYUMjeyZfIlYd8Whz8TwCMg1AgeTA83J7qt")
key = b64decode("zb9v8uGYo/BWzbhouenY2g==")

cipher = AES.new(key)
plaintext = cipher.decrypt(ciphertext)

print plaintext
