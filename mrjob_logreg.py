from mrjob.job import MRJob

class MRLogReg(MRJob):
	def steps(self):
		''', self.mr(mapper = self.mapper, reducer = self.reducer)'''
		return [self.mr(mapper = self.splitter, reducer = self.splitreduce)]
		
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