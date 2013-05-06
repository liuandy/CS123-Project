import re

with open('census-income.names.txt', 'r') as f:
	lines = f.readlines()

lines = lines[23:68]

codes = []

for line in lines:
	code = re.findall('\t(\w+)\n', line)[0]
	if code in ['AGI', 'FEDTAX', 'PTOTVAL', 'TAXINC', 'PEARNVAL']:
		continue
	codes.append(code)

codes.append('YEAR')
codes.append('CLASS')

with open('names.txt', 'w') as f:
	f.write('[')
	for code in codes[:-1]:
		f.write("'" + code + "', ")
	f.write("'" + codes[-1] + "'")
	f.write(']')