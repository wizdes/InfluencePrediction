import sys

f = open("ccr_data.txt")
lines = f.readlines()
dArray = [0,0,0]
for index, elt in enumerate(lines):
	dArray[index % 3] += float(elt)
for elt in dArray:
	print 1.0 * elt / 6