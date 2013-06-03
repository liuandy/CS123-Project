from mrjob.job import MRJob

class MRLogReg(MRJob):
	def steps(self):
		return [self.mr(mapper = self.splitter, reducer = self.splitreduce), self.mr(mapper = self.mapper, reducer = self.reducer)]
		
	def splitter(self, key, line):
		var = line.strip().upper()
		yield (None, var)
		
	def splitreduce(self, key, line):
		# Set N to number of slaves
		N = 4
		
		rv = []
		for i in range(N):
			rv.append([])
		
		temp = list(line)
		
		temp_len = len(temp)
		
		for i in range(temp_len):
			rv[i % N].append(temp[i])
		
		for i in range(N):
			yield (i, rv[i])
			
	def mapper(self, key, line):	
		import pandas as pd, statsmodels.api as sm, numpy as np
		import urllib2, pickle
		url = 'https://s3.amazonaws.com/cs12300-spr13-aliu/data/contdict_pickle'
		p_data = urllib2.urlopen(url).read()
		cont_dict = pickle.loads(p_data)

		data_url = 'https://s3.amazonaws.com/cs12300-spr13-aliu/data/pickled_data'
		p_data = urllib2.urlopen(data_url).read()
		data = pickle.loads(p_data)
		
		data_t_url = 'https://s3.amazonaws.com/cs12300-spr13-aliu/data/test_pickle'
		p_data = urllib2.urlopen(data_t_url).read()
		data_t = pickle.loads(p_data)

		for vars in line:
			varlist = vars.strip().split(',')
			varlist = filter(lambda x: x in cont_dict and cont_dict[x] != -1, varlist)

			data2 = data[varlist + ['CLASS']].copy()
			data2_t = data_t[varlist + ['CLASS']].copy()

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

			try:
				logger = sm.Logit(data2['CLASS'], data2[regvars])

				fit = logger.fit()
				preds = fit.predict()

				errs = np.array(data2['CLASS']) - np.round(preds)

				t1err = len(filter(lambda x: x == -1, errs)) / float(len(data2['CLASS']) - sum(data2['CLASS']))
				t2err = len(filter(lambda x: x == 1, errs)) / float(sum(data2['CLASS']))

				preds_test = fit.predict(data2_t[regvars])
				errs_test = np.array(data2_t['CLASS']) - np.round(preds_test)

				t1err_t = len(filter(lambda x: x == -1, errs_test)) / float(len(data2_t['CLASS']) - sum(data2_t['CLASS']))
				t2err_t = len(filter(lambda x: x == 1, errs_test)) / float(sum(data2_t['CLASS']))

				yield (vars, (t1err, t2err, t1err_t, t2err_t))
			except:
				yield (vars, (-1, -1, -1, -1))
				pass
				
	def reducer(self, key, line):
		yield (key, list(line))
		
if __name__ == '__main__':
	MRLogReg.run()