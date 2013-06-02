from mrjob.job import MRJob

class MRTerribleTerribleDamage(MRJob):
	
	def mapper(self, _, line):
		for l in line:
			yield (int(l), int(l) ** 2)
	
	def combiner(self, l, squared):
		yield (0, 100)
	
	def reducer(self, l, squared):
		yield (int(l), squared.next())
		
	def steps(self):
		return [self.mr(mapper = self.mapper, combiner = none, reducer = self.reducer)]
	
if __name__ == '__main__':
	MRTerribleTerribleDamage.run()
