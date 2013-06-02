from test_mr import MRTerribleTerribleDamage

if __name__ == '__main__':
	job = MRTerribleTerribleDamage([[1],[2],[3],[4],[5]])
	with job.make_runner() as runner:
		runner.run()
		
		rv = []
		
		for line in runner.stream_output():
			key, value = job.parse_output_line(line)
			print (key, value)