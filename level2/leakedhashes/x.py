# open hashes and store to dict

hashes = {}
with open("hashdump", "r") as f:
	for line in f:
		key, value = line.split(":")
		hashes[key] = value
with open("hashes", "w") as f:
	for v in hashes.values():
		f.write(v)


