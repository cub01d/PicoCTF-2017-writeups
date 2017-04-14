import md5

# userid = buf[7]
# seed = buf[14]
# nexthash = buf[-1]

userid = raw_input("userid: ")
nexthash = raw_input("nexthash: ")

seed = md5.new(userid).hexdigest()
hash = seed
for i in xrange(100):
	if md5.new(hash).hexdigest() == nexthash:
		print hash
		break
	hash = md5.new(hash).hexdigest()
