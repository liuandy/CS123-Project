import pandas as pd, statsmodels.api as sm, numpy as np
import urllib2, pickle
import time

varlist = ['AAGE', 'AHGA', 'DIVVAL', 'AHRSPAY']

url = 'https://s3.amazonaws.com/cs12300-spr13-aliu/data/contdict_pickle'

print 'Loading continuous dictionary...',
p_data = urllib2.urlopen(url).read()
cont_dict = pickle.loads(p_data)
print 'Done.'

'''
print 'Loading data...',
data_url = 'https://s3.amazonaws.com/cs12300-spr13-aliu/data/pickled_data'
p_data = urllib2.urlopen(data_url).read()
data = pickle.loads(p_data)
print 'Done.'
'''

data = pd.read_csv('census_nomissing.csv', index_col = 0)

timer = time.time()

varlist = filter(lambda x: x in cont_dict and cont_dict[x] != -1, varlist)
print varlist

data2 = data[varlist + ['CLASS']].copy()

regvars = []
for var in varlist:
	if cont_dict[var] == 0:
		levels = list(set(data2[var]))
		
		print 'Expanding levels: ' + str(levels)
		
		i = 0
		for l in levels[1:]:
			data2[var + str(i)] = 1 * (data2[var] == l)
			regvars.append(var + str(i))
			i += 1
	else:
		regvars.append(var)
		
print regvars


logger = sm.Logit(data2['CLASS'], data2[regvars])

preds = logger.fit().predict()

errs = np.array(data2['CLASS']) - np.round(preds)

t1err = len(filter(lambda x: x == -1, errs)) / float(len(data2['CLASS']) - sum(data2['CLASS']))
t2err = len(filter(lambda x: x == 1, errs)) / float(sum(data2['CLASS']))

print 'Type 1 Error: %s\nType 2 Error: %s' % (t1err, t2err)
print 'Elapsed time: ' + str(time.time() - timer)