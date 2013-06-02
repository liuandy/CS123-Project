from mrjob_uniqval2 import MRUniqueVal2
import sys

if __name__ == '__main__':
	job = MRUniqueVal2(args = sys.argv[1:])
	with job.make_runner() as runner:
		runner.run()
		
		for line in runner.stream_output():
			key, value = job.parse_output_line(line)
			print key, value