from mrjob.job import MRJob

class MRUniqueVal(MRJob):
	
	def mapper(self, _, line):
		#import urllib2, pickle, pandas
		#url = 'https://s3.amazonaws.com/cs12300-spr13-aliu/data/pickled_data'
		#p_data = urllib2.urlopen(url).read()
		#data = pickle.loads(p_data)
		
		wtf = 0
		
		for l in line:
			wtf += 1
			var = l.strip().upper()
			#rv = list(set(data[var]))
			yield (1, (var, 'hi: ' + str(wtf)))
	
	def reducer(self, key, value):
		yield (key, list(value))
		
	def steps(self):
		return [self.mr(mapper = self.mapper, combiner = None, reducer = self.reducer)]
	
if __name__ == '__main__':
	MRUniqueVal.run()
