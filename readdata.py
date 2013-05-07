import sys
import pandas as pd

with open('census-income.data', 'r') as f:
	lines = f.readlines()

data = []

for line in lines:
	data.append(line.strip().split(','))

data_final = []
cont_data = [0, 5, 16, 17, 18, 24, 30, 39, 40]

for line in data:
	new_line = []
	for i in range(42):
		temp = line[i].strip()
		if i == 41:
			if temp == '- 50000.':
				temp = 1
			else:
				temp = 0
		elif temp == '?':
			temp = None
		elif i in cont_data:
			try:
				temp = float(temp)
			except:
				print (i, temp)
				sys.exit(1)
		new_line.append(temp)
	data_final.append(new_line)
	
labels = ['AAGE', 'ACLSWKR', 'ADTIND', 'ADTOCC', 'AHGA', \
	'AHRSPAY', 'AHSCOL', 'AMARITL', 'AMJIND', 'AMJOCC', \
	'ARACE', 'AREORGN', 'ASEX', 'AUNMEM', 'AUNTYPE', \
	'AWKSTAT', 'CAPGAIN', 'CAPLOSS', 'DIVVAL', 'FILESTAT',\
	'GRINREG', 'GRINST', 'HHDFMX', 'HHDREL', 'MARSUPWT',\
	'MIGMTR1', 'MIGMTR3', 'MIGMTR4', 'MIGSAME', 'MIGSUN',\
	'NOEMP', 'PARENT', 'PEFNTVTY', 'PEMNTVTY', 'PENATVTY',\
	'PRCITSHP', 'SEOTR', 'VETQVA', 'VETYN', 'WKSWORK',\
	'YEAR', 'CLASS']
	
data = pd.DataFrame(data_final, columns = labels)