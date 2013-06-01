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
import pylab


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
#create a small samples
n = 1000
rowstokeep = random.sample(data.index,n)
s = data.ix[rowstokeep]
colstokeep = ['CLASS','AHRSPAY','WKSWORK','AHGA']
s = s[colstokeep]
train_cols = ['AHGA']
s['intercept'] = 1.0  #manually add in intercept term. or not. 

#Create factor variables
for elem in s['AHGA'].unique():
    s[str(elem)] = s['AHGA'] == elem #A bool for each possible observations
	
	
#Use this procedure to perform logistic regression
y = s[s.columns[0]]
X = s[s.columns[6:]]  #educational dummy variables. Make sure that we don't create a Singular matrix. 

y_tr = y[:900]
X_tr = X.irow(range(900))
y_test = y[900:] #Not a list
X_test = X.irow(range(900,1000))

logger = sm.Logit(y,X)
logger = sm.Logit(y_tr,X_tr)
logger = logger.fit()

yhat = logger.predict() #returns a bunch of values between 0 and 1. 

loggerfit = logger.fit()

# A function to calculate misclassification rates
 
def logpredict(logfit,newX,y):
	y_hat = map(round,logfit.predict(newX))
	misclass = y -y_hat
	length = len(y)
	falsepos = float(sum(misclass==1))/length
	falseneg = float(sum(misclass==-1))/length
	#False pos: thought they were class, now they're not
	#False neg: thought they weren't class, but they were!
	return(falsepos,falseneg)

def kfold_cv_pandas(X,K,randomise = True):
	""" kfold cv algorithm adapted for use with PANDAS data conventions
	note that the outcome var y must be the 1st column of input X   """
	lenx = len(X) #len() operator works even for pandas data frames
	rows = random.sample(X.index,lenx)
	X = X.ix[rows] #this permutes all rows. 
	for k in xrange(K):
		training = X.irow([i for i in xrange(lenx) if i % K !=k])
		validation = X.irow([i for i in xrange(lenx) if i % K == k])
		yield training, validation
		
		
#So, now we have a returned generator object. We want to find error rate


def CV_fit(yX,n,randomize = True):
	firsttry = kfold_cv_pandas(yX,n,randomize)
	for training, validation in firsttry:
		y = training[training.columns[0]]
		X = training[training.columns[5:]]
		logger = sm.Logit(y,X)
		fitted = logger.fit()
		yield(logpredict(fitted,X,y))


##To do: this function is extremely wasteful because you call subplot SO MANY DAMN TIMES!
Ks = [10,20,30,40,50]
k_cv,fp_cv,fn_cv = [],[],[]
for k in Ks:
	CVresults = CV_fit(s,k)
	for fp, fn in CVresults:
		k_cv.append(k)
		fp_cv.append(fp)
		fn_csv.append(fn)
pylab.figure(1)
pylab.subplot(211)
pylab.xlim(Ks[0]-2,Ks[-1]+2)
pylab.ylim([.05,.07])
pylab.plot(k_cv,fp_cv,'bo')
pylab.subplot(212)
pylab.xlim(Ks[0]-2,Ks[-1]+2)
pylab.ylim(.0,.01)
pylab.plot(k_cv,fn_cv,'g^')
pylab.show()

		
#[X,y] = k_fold_cross_validation(s,2
	
#Test:
logpredict(loggerfit,y)



#Next: k-fold cross-validation. 

