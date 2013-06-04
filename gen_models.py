import pandas as pd, statsmodels.api as sm, numpy as np
import urllib2, pickle
import time

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
data_test = pd.read_csv('test_nomissing.csv', index_col = 0)

with open('scan_range.txt', 'r') as f:
	in_names = f.readlines()

timer = time.time()

runs = 0

with open('scan_results.csv', 'w') as f:
	for in_name in in_names:
		varlist = in_name.strip().split(',')
		varlist = filter(lambda x: x in cont_dict and cont_dict[x] != -1, varlist)

		data2 = data[varlist + ['CLASS']].copy()
		data2_t = data_test[varlist + ['CLASS']].copy()

		regvars = []
		for var in varlist:
			if cont_dict[var] == 0:
				levels = list(set(data2[var]))

				
				i = 0
				for l in levels[1:]:
					data2[var + str(i)] = 1 * (data2[var] == l)
					data2_t[var + str(i)] = 1 * (data2_t[var] == l)
					regvars.append(var + str(i))
					i += 1
			else:
				regvars.append(var)


		logger = sm.Logit(data2['CLASS'], data2[regvars])

		fit = logger.fit()
		preds = fit.predict()

		errs = np.array(data2['CLASS']) - np.round(preds)

		t1err = len(filter(lambda x: x == -1, errs)) / float(len(data2['CLASS']) - sum(data2['CLASS']))
		t2err = len(filter(lambda x: x == 1, errs)) / float(sum(data2['CLASS']))


		preds_test = fit.predict(data2_t[regvars])
		errs_test = np.array(data2_t['CLASS']) - np.round(preds_test)

		t1err_t = len(filter(lambda x: x == -1, errs_test)) / float(len(data_test['CLASS']) - sum(data_test['CLASS']))
		t2err_t = len(filter(lambda x: x == 1, errs_test)) / float(sum(data_test['CLASS']))
		
		f.write("'%s',%s,%s,%s,%s\n" % (in_name.strip(), t1err, t2err, t1err_t, t2err_t))
		
		runs += 1
		
		if (runs - 1) % 10 == 0:
			print 'Run ' + str(runs - 1) + ' completed. Time: ' + str(time.time() - timer)