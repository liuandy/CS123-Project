
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
		
		
#So, now we have a returned generator object. We want to find error rate


def CV_fit(yX,n,randomize = True):
	"""use kfold_csv_pandas to divide data set, fit it with a logistic method, and calculate error rates using logpredict"""
	folded = kfold_cv_pandas(yX,n,randomize)
	for training, validation in folded:
		y = training[training.columns[0]]
		X = training[training.columns[5:]]  ## <-- Adjust parameters here##
		logger = sm.Logit(y,X)
		fitted = logger.fit()
		yield(logpredict(fitted,X,y)) #Could collapse results, but then we lose empirical standard deviation. 


		
