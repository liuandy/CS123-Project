#sources: 

#Required modules:
#numpy: a language extension that defines the numerical array and matrix
#pandas: primary package to handle and operate directly on data.
#statsmodels: statistics & econometrics package with useful tools for parameter estimation & statistical testing
#pylab: for generating plots


#References
#http://blog.yhathq.com/posts/logistic-regression-and-python.html
#http://pandas.pydata.org/pandas-docs/stable/indexing.html
#http://statsmodels.sourceforge.net/stable/index.html

import pandas as pd
import statsmodels.api as sm
import pylab as pl
import numpy as np
import random


#Learning pandas:
#First, run readdata.py

#note how many missing obserations there are: 
print data.dropna()
#95130
print data
#199523
95130/199523
# = .476....over half of the data has an na column...

#We could explore logit vs. probit.
#note that pandas includes a .index part 

#Transfering R to python
#create a small sample
n = 1000
rowstokeep = random.sample(data.index,n)
s = data.ix[rowstokeep]
colstokeep = ['CLASS','AHRSPAY','WKSWORK','AHGA']
s = s[colstokeep]
train_cols = ['AHGA']
s['intercept'] = 1.0  #manually add in intercept term
########This returns an error because python does not automatically handle factor variables
#We must create these variables seperately.
for elem in s['AHGA'].unique():
    s[str(elem)] = s['AHGA'] == elem
	
y = s[s.columns[0]]
X = s[s.columns[5:]]
logit = sm.Logit(s[s.columns[0]], s[s.columns[5:]])
result = logit.fit()

yhat = result.predict() #returns a bunch of values between 0 and 1. 
loggerfit = logger.fit()
 
# A function to calculate misclassification rates
 
def logpredict(logfit,y):
	y_hat = map(round,logfit.predict())
	misclass = y -y_hat
	falsepos = float(sum(misclass==1))/float(len(misclass))
	falseneg = float(sum(misclass==-1))/float(len(misclass))
	return([falsepos,falseneg])

#Test:
logpredict(loggerfit,y)
	
# fit the model
