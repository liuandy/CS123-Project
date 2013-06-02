from test_mr import MRTerribleTerribleDamage
import sys

if __name__ == '__main__':
	job = MRTerribleTerribleDamage(args = sys.argv[1:])
	with job.make_runner() as runner:
		runner.run()
		
		rv = []
		
		for line in runner.stream_output():
			key, value = job.parse_output_line(line)
			print (key, value)