import re

namestoparse = open("namestoparse.txt","r").read().split("\n")
ntp = [re.findall('\((.*?)\)',i) for i in namestoparse]

ntpkey = open("namestoparseKEY.txt","r").read().split("\n")
ntpkey = [i[2:].split("\t") for i in ntpkey]
ntpkey = [filter(None, str_list) for str_list in ntpkey]

for i in range(len(ntp)):
	for j in ntpkey:
		if ntp[i][0] == j[0]:
			ntp[i].append(j[1])

ntp[len(ntp)-1].append('YEAR')
CB = [i[1] for i in ntp]
understandable = [i[0] for i in ntp]
			
			
			
outputfile = open("parsednames.txt","w")



for item in CB:
	outputfile.write(item+",")
outputfile.write("\n")
for item in understandable:
	outputfile.write(item+",")
