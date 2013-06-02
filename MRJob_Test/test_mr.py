from mrjob.job import MRJob

class MRTerribleTerribleDamage(MRJob):
	
	def mapper(self, _, line):
		for l in line:
			yield (l, int(l) ** 2)
	
	def combiner(self, l, squared):
		yield (l, squared)
	
	def reducer(self, l, squared):
		yield (l, squared)
	
if __name__ == '__main__':
	MRTerribleTerribleDamage.run()