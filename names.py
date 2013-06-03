labels = ['AAGE', 'ACLSWKR', 'ADTIND', 'ADTOCC', 'AHGA', \
	'AHRSPAY', 'AHSCOL', 'AMARITL', 'AMJIND', 'AMJOCC', \
	'ARACE', 'AREORGN', 'ASEX', 'AUNMEM', 'AUNTYPE', \
	'AWKSTAT', 'CAPGAIN', 'CAPLOSS', 'DIVVAL', 'FILESTAT',\
	'GRINREG', 'GRINST', 'HHDFMX', 'HHDREL', 'MARSUPWT',\
	'MIGMTR1', 'MIGMTR3', 'MIGMTR4', 'MIGSAME', 'MIGSUN',\
	'NOEMP', 'PARENT', 'PEFNTVTY', 'PEMNTVTY', 'PENATVTY',\
	'PRCITSHP', 'SEOTR', 'VETQVA', 'VETYN', 'WKSWORK',\
	'YEAR', 'CLASS']
	
with open('labels.txt', 'w') as f:
	for l in labels:
		f.write('dict[\'' + l +'\'] = ' + '\n')
