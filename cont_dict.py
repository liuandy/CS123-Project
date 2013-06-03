import pickle

dict = {}

dict['AAGE'] = 1
dict['ACLSWKR'] = 0
dict['ADTIND'] = 0
dict['ADTOCC'] = 0
dict['AHGA'] = 0
dict['AHRSPAY'] = 1
dict['AHSCOL'] = 0
dict['AMARITL'] = 0
dict['AMJIND'] = 0
dict['AMJOCC'] = 0
dict['ARACE'] = 0
dict['AREORGN'] = -1
dict['ASEX'] = 0
dict['AUNMEM'] = 0
dict['AUNTYPE'] = 0
dict['AWKSTAT'] = 0
dict['CAPGAIN'] = 1
dict['CAPLOSS'] = 1
dict['DIVVAL'] = 1
dict['FILESTAT'] = 0
dict['GRINREG'] = 0
dict['GRINST'] = -1
dict['HHDFMX'] = 0
dict['HHDREL'] = 0
dict['MARSUPWT'] = -1
dict['MIGMTR1'] = -1
dict['MIGMTR3'] = -1
dict['MIGMTR4'] = -1
dict['MIGSAME'] = 0
dict['MIGSUN'] = -1
dict['NOEMP'] = 1
dict['PARENT'] = 0
dict['PEFNTVTY'] = 0
dict['PEMNTVTY'] = 0
dict['PENATVTY'] = 0
dict['PRCITSHP'] = 0
dict['SEOTR'] = 0
dict['VETQVA'] = 0
dict['VETYN'] = 0
dict['WKSWORK'] = 1
dict['YEAR'] = 0
dict['CLASS'] = -1

with open('contdict_pickle', 'wb') as f:
	pickle.dump(dict, f)
