import urllib2, pickle, itertools, time

url = 'https://s3.amazonaws.com/cs12300-spr13-aliu/data/contdict_pickle'

print 'Loading continuous dictionary...',
p_data = urllib2.urlopen(url).read()
cont_dict = pickle.loads(p_data)
print 'Done.'

vars = filter(lambda x: x[1] != -1, cont_dict.items())
vars = map(lambda x: x[0], vars)

timer = time.time()

with open('scan_range.txt', 'w') as f:
	for i in range(1,3):
		temp = itertools.combinations(vars, i)
		for t in temp:
			f.write(str(t).strip('()').strip(',').replace(' ', '').replace('\'', ''))
			f.write('\n')