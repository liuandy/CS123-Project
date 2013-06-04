import sys
import pandas as pd
from knnfill import *

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
				temp = 0
			else:
				temp = 1
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

data2 = data.copy()

subset = map(lambda x: len(x) == 0, find_missing(data))

data_nomiss = data2[subset]
data_miss = data2[map(lambda x: not x, subset)]