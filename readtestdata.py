import sys
import pandas as pd

with open('census-income.test', 'r') as f:
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
	
data_test = pd.DataFrame(data_final, columns = labels)
data2 = data_test.copy()

def find_missing(data, type = 'i'):
	'''
	Outputs a list of list where each list item corresponds with
	the row in the panda data frame and the list contained at
	that index contains the list of all labels that the data are
	missing.
	'''
	import pandas as pd
	import sys

	if type not in ['i', 'l']:
		print 'Invalid type.'
		sys.exit(1)

	labels = ['AAGE', 'ACLSWKR', 'ADTIND', 'ADTOCC', 'AHGA', \
		'AHRSPAY', 'AHSCOL', 'AMARITL', 'AMJIND', 'AMJOCC', \
		'ARACE', 'AREORGN', 'ASEX', 'AUNMEM', 'AUNTYPE', \
		'AWKSTAT', 'CAPGAIN', 'CAPLOSS', 'DIVVAL', 'FILESTAT',\
		'GRINREG', 'GRINST', 'HHDFMX', 'HHDREL', 'MARSUPWT',\
		'MIGMTR1', 'MIGMTR3', 'MIGMTR4', 'MIGSAME', 'MIGSUN',\
		'NOEMP', 'PARENT', 'PEFNTVTY', 'PEMNTVTY', 'PENATVTY',\
		'PRCITSHP', 'SEOTR', 'VETQVA', 'VETYN', 'WKSWORK',\
		'YEAR', 'CLASS']

	tempdata = list(data.itertuples())
	rv = []
	for temp in tempdata:
		row_list = []
		for i in range(42):
			# Exclude columns we don't care about
			if labels[i] in ['MIGMTR1', 'MIGMTR3', 'MIGMTR4', 'MIGSUN', 'GRINST']:
				continue
			if temp[i+1] == None:
				row_list.append(labels[i])
		rv.append(row_list)
	return rv

def compute_distance(list1, list2):
	list1_small = list1[1:]
	list2_small = list2[1:]
	dist = 0

	for i in [1,2,3,4,6,7,8,9,10,11,13,14,15]:
		dist += not (list1_small[i] == list2_small[i])
	return dist

def compute_1nn(test, nomisslist):
	N = len(nomisslist)
	shortest_dist = 50
	nm_index = -1
	for i in range(N):
		dist = compute_distance(test, nomisslist[i])
		if dist < shortest_dist:
			shortest_dist = dist
			nm_index = i
	return nm_index

def knnfill1(data, data_miss, data_nomiss):
	import pandas as pd
	misslist = find_missing(data_miss)
	N = len(misslist)
	f = open('knn-log.txt', 'w')

	miss_entries = list(data_miss.itertuples())
	nomiss_entries = list(data_nomiss.itertuples())

	import time
	timer = time.time()

	for i in range(N):
		if (i - 1) % 100 == 0:
			print 'Completed ' + str(i-1) + ' rows. Total time: ' + str(time.time() - timer)
		index_1nn = compute_1nn(miss_entries[i], nomiss_entries)
		for label in misslist[i]:
			data[miss_entries[i][0]:(miss_entries[i][0] + 1)][label] = \
				data_nomiss[index_1nn:(index_1nn + 1)][label].tolist()[0]
			f.write('Row ' + str(miss_entries[i][0]) + ', label ' + label)
			f.write(', used ' + str(index_1nn))
			f.write(': ' + str(data_nomiss[index_1nn:(index_1nn + 1)][label].tolist()[0]) + '\n')
	f.close()

data_train = pd.read_csv('census_nomissing.csv', index_col = 0)
subset = map(lambda x: len(x) > 0, find_missing(data_test))
data_miss = data2[subset]