from mrjob.job import MRJob

class MRUniqueVal2(MRJob):
	
	def steps(self):
		return [self.mr(mapper = self.splitter, reducer = self.splitreduce), self.mr(mapper = self.mapper, reducer = self.reducer)]
	
	def splitter(self, key, line):
		var = line.strip().upper()
		yield (None, var)
		
	def splitreduce(self, key, line):
		temp = list(line)
		N = len(temp) / 4
		for i in range(4):
			if i < 3:
				yield (i, temp[(i*N):((i+1)*N)])
			else:
				yield (i, temp[(i*N):])
	
	def mapper(self, key, line):
		import pandas, pickle, urllib2
		url = 'https://s3.amazonaws.com/cs12300-spr13-aliu/data/pickled_data'
		p_data = urllib2.urlopen(url).read()
		data = pickle.loads(p_data)
		
		wtf = 0
		
		for l in line:
			wtf += 1
			yield (l, (wtf, list(set(data[l]))))
	
	def reducer(self, key, line):
		yield (key, list(line))
		
if __name__ == '__main__':
	MRUniqueVal2.run()