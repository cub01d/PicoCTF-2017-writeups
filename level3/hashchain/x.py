import socket
import md5

url = "shell2017.picoctf.com"
port = 58801

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((url, port))
s.recv(512)
s.send("f\n")
buf = s.recv(512).split()

userid = buf[5]
buf = s.recv(512).split()
nexthash = buf[0]

print "userid: ", userid 
print "nexthash: ",  nexthash

hash = md5.new(userid).hexdigest()
for i in xrange(100):
	if md5.new(hash).hexdigest() == nexthash:
#		print hash, md5.new(hash).hexdigest(), nexthash
		break
	hash = md5.new(hash).hexdigest()

print "sending hash"
s.send(hash + "\n")
print "receiving data"
print s.recv(512)
