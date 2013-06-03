from mrjob_logreg import MRLogReg
import sys

if __name__ == '__main__':
	job = MRLogReg(args = sys.argv[1:])
	with job.make_runner() as runner:
		runner.run()
		
		for line in runner.stream_output():
			key, value = job.parse_output_line(line)
			print key, value