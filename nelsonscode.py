#References
#http://blog.yhathq.com/posts/logistic-regression-and-python.html
#http://pandas.pydata.org/pandas-docs/stable/indexing.html
#http://statsmodels.sourceforge.net/stable/index.html
from mrjob.job import MRJob
import urllib2, pickle
import pandas
import statsmodels.api as sm
import pylab as pl
import numpy as np
import random
import pylab
#import nelsonfunctions as nf #There aren't any glaring naming issues here. 

#------------------- begin functions------------------------------------------------------------#

def logpredict(logfit,newX,y):
	"""using an already fitted logistic regression object, predicts outcomes (kind of) given new X.
	Then calculates error rate in terms of false positive and false negative predictions"""
	y_hat = map(round,logfit.predict(newX))
	misclass = y -y_hat
	length = len(y)
	falsepos = float(sum(misclass==1))/length
	falseneg = float(sum(misclass==-1))/length
	#False pos: thought they were class, now they're not
	#False neg: thought they weren't class, but they were!
	return(falsepos*100,falseneg*100)

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
		

def CV_fit(yX,n,randomize = True):
	"""use kfold_csv_pandas to divide data set, fit it with a logistic method, and calculate error rates using logpredict"""
	folded = kfold_cv_pandas(yX,n,randomize)
	for training, validation in folded:
		y = training[training.columns[0]]
		X = training[training.columns[5:]]  ## <-- Adjust parameters here##
		logger = sm.Logit(y,X)
		fitted = logger.fit()
		yield(logpredict(fitted,X,y)) #Could collapse results, but then we lose empirical standard deviation. 
#------------------- end functions------------------------------------------------------------#


#--------------------- begin data description----------------------------#
#Load dataf - data filled (with knn)
data = pandas.read_csv('census_original.csv', index_col = 0)
#note how many missing obserations there are: 
print data.dropna()
#95130
print data
#199523
95130/199523
# = .476....over half of the data has an na column...
#--------------------- end data description----------------------------#


#--------------------- Seperate data for logistic regression----------#
#Transfering R to python
#create a small samples
n = len(data)
rowstokeep = random.sample(data.index,n)
s = data.ix[rowstokeep]

#choose predictor variable 
colstokeep = ['CLASS','AHRSPAY','WKSWORK','AHGA']
s = s[colstokeep]
train_cols = ['AHGA']
s['intercept'] = 1.0  #manually add in intercept term. or not. 
factorvars = ['AHGA']
#Create factor variables 	
for fv in factorvars:
	for elem in s[fv].unique():
		s[str(elem)] = s['AHGA'] == elem #A bool for each possible observations
	
	
#Use this procedure to perform logistic regression
y = s[s.columns[0]]
X = s[s.columns[6:]]  #educational dummy variables. Make sure that we don't create a Singular matrix. 

y_tr = y[:900]
X_tr = X.irow(range(900))
y_test = y[900:] #Not a list
X_test = X.irow(range(900,1000))

logger = sm.Logit(y,X)
#logger = sm.Logit(y_tr,X_tr)
fitted = logger.fit()
yhat = fitted.predict(X) #returns a bunch of values between 0 and 1. 
logpredict(fitted,X,y)
#--------------------- end data seperation & logistic regression -------#

#---------------begin functions for computationally intensive cross-validation-----#
# A function to calculate misclassification rates
 #-------------------begin cross validation scripting---------------------#
Ks = [10,20,30,40,50,200,400,600,800,1000] #<--- adjust this. 
k_cv,fp_cv,fn_cv = [],[],[]
for k in Ks:
	CVresults = CV_fit(s,k)
	for fp, fn in CVresults:
		k_cv.append(k)
		fp_cv.append(fp)
		fn_cv.append(fn)

#Turn the cross validation results into a data frame
d = {'k_cv' : k_cv, 'fp_cv' : fp_cv, 'fn_cv' : fn_cv}
cvdata = pandas.DataFrame(d)
#store data outwards: 
cvdata.to_csv("cvresults.csv")

#-----plotting----------#
pylab.figure(1)
pylab.subplot(211).set_title("False Positive Error rate under Cross Validation")
pylab.subplot(211).set_ylabel("% error")
pylab.subplot(211).set_xlabel("k-fold CV")
pylab.xlim(Ks[0]-2,Ks[-1]+2)
#pylab.ylim([.05,.07])
pylab.plot(k_cv,fp_cv,'bo')
pylab.subplot(212).set_title("False Negative Error rate under Cross Validation")
pylab.subplot(212).set_ylabel("% error")
pylab.subplot(212).set_xlabel("k-fold CV")
pylab.xlim(Ks[0]-2,Ks[-1]+2)
#pylab.ylim(.0,.01)
pylab.plot(k_cv,fn_cv,'g^')
pylab.show()
#----end plotting-------#

#-------begin mrjob stuff-----------------------------#
#-------right now this is just copied from andy's-----#
# class MRUniqueVal(MRJob):
	
	# def mapper(self, _, line):
		# url = 'https://s3.amazonaws.com/cs12300-spr13-aliu/data/pickled_data'
		# p_data = urllib2.urlopen(url).read()
		# data = pickle.loads(p_data)
		
		# for l in line:
			# var = l.strip().upper()
			# rv = list(set(data[var]))
			# yield (None, (var, rv))
	
	# def reducer(self, key, value):
		# yield (key, list(value))
		
	# def steps(self):
		# return [self.mr(mapper = self.mapper, combiner = None, reducer = self.reducer)]


def f(x):
	return exp(x)/(1+exp(x))
	
x = range(-600,600)
x = [i/100. for i in x]
y = [f(i) for i in x]
pylab.plot(x,y)
pylab.title("Logistic Function")
pylab.xlabel("x")
pylab.ylabel("f(x)") 
pylab.show()