from mrjob_logreg import MRLogReg
import sys

if __name__ == '__main__':
	job = MRLogReg(args = sys.argv[1:])
	with job.make_runner() as runner:
		runner.run()
		
		with open('logreg_output.csv', 'w') as f:
			for line in runner.stream_output():
				key, value = job.parse_output_line(line)
				
				f.write('\'%s\',%s,%s,%s,%s\n' % (key, value[0][0], value[0][1], value[0][2], value[0][3]))