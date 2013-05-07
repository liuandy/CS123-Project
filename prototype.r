
setwd("C:/Users/nauner/SkyDrive/School/ClassMaterials/Chicago2012-2013/Spring/CMSC123/andyproj/CS123-Project")
data <- read.table("census-income.data", sep = ",", header =F, na.strings = "NA")
names(data) <- c("AAGE","ACLSWKR","ADTIND","ADTOCC","AHGA","AHRSPAY","AHSCOL","AMARITL","AMJIND","AMJOCC","ARACE","AREORGN","ASEX","AUNMEM","AUNTYPE","AWKSTAT","CAPGAIN","CAPLOSS","DIVVAL","FILESTAT","GRINREG","GRINST","HHDFMX","HHDREL","MARSUPWT","MIGMTRM1","MIGMTR3","MIGMTR4","MIGSAME","MIGSUN","NOEMP","PARENT","PEFNTVTY","PEMNTVTY","PENATVTY","PRCITSHP","SEOTR","VETQVA","VETYN","WKSWORK","YEAR","INC")
# Extract only the continuous data to work with for now
cont_data <- data[,c(1,3,4,6,17,18,19,25,31,37,39,40,41)]

# Pull out the class vector
class <- as.integer(data[,42] == levels(data[,42])[2])

# How much of our data are labeled with 1?
sum(class) / length(class)
# 6%... oh dear.

# Normalizing the data
for (i in 1:(dim(cont_data)[2])) {
  cont_data[,i] <- (cont_data[,i] - mean(cont_data[,i])) / sd(cont_data[,i])
}

# Building a data-frame for log regression only using age as predictor
test1 <- data.frame(age = cont_data$AAGE, class = class)
test1.logr <- glm(class ~ age, data = test1, family = binomial)

#(note: family = binomial specifies log regression. )

summary(predict(test1.logr, test1, type = "response"))
#results: max is .18210, so everything classed as 0. Majority classifier

# From here, we see that with only age, we do not have nearly enough predictive power.
# Everything is classified as below median income.

# Let's look at wage per hour. Remember, this is normalized to mean 0, sd=1
summary(cont_data$AHRSPAY)

test2 <- data.frame(age = cont_data$AAGE, wph = cont_data$AHRSPAY, class = class)
test2.logr <- glm(class ~ age + wph, data = test2, family = binomial)

sum(predict(test2.logr, test2, "response") > .5)
# We make four classifications into 1.

# Let's try something that is tried and true in income classification
test3 <- data.frame(educ = data$AHGA, class = class)
test3.logr <- glm(class ~ factor(educ), data = test3, family = binomial)

# 3056 classifications into the 50,000+ category. That's lovely.
sum(predict(test3.logr, test3, "response") > .5)

test3.misclass <- class - (predict(test3.logr, test3, "response") > .5)

# Misclassing 50,000+ as 50,000-
sum(test3.misclass == - 1) / sum(class)
#results of .1154902 indicates that 11% of above 5K classified as under 5K

# Misclassing 50,000- as 50,000+
sum(test3.misclass == 1)/ abs(sum(class - 1))
#result of .0574 indicates that 5% of under 5K classified as over 5K

# So, we see from this that education is a great stand-alone predictor of income.
# That's rather unsurprising.

#not in universe: 
niu <- apply(data, 1, function(x) (sum(x == "  Not in universe") > 0))
sum(niu)

missing <- apply(data, 1, function(x) (sum(x == " ?") > 0))
sum(missing)

#Try to find the "best" model using AIC (Akaike Information Criteria)
#AIC defined as -2max loglik + 2*p 

testaic = data.frame(vars = cont_data,class=class)
aicmodel <- glm(class~  .,data = testaic, family=binomial)
sum(abs(class-(predict(aicmodel,testaic,type="response"))))
aic.misclass <- class - (predict(aicmodel,testaic,type="response") > .5)
sum(aic.misclass == - 1) / sum(class)   #.07389759
sum(aic.misclass == 1)/ abs(sum(class - 1))  #.05255396
#Now, use AIC

#Try to find the "best" model using AIC (Akaike Information Criteria)
#AIC defined as -2max loglik + 2*p m
step(aicmodel)
#resulting model
#Note that step() removed VETYN, veteran's benefits

aicres <- glm(formula = class ~ vars.AAGE + vars.ADTIND + vars.ADTOCC + vars.AHRSPAY + vars.CAPGAIN + vars.CAPLOSS + vars.DIVVAL + vars.MARSUPWT + vars.NOEMP + vars.SEOTR + vars.WKSWORK + vars.YEAR, family = binomial, data = testaic)
aicres.misclass <- class - (predict(aicres,testaic,type="response") > .5)
sum(aicres.misclass == - 1) / sum(class)   #.07389
sum(aicres.misclass == 1)/ abs(sum(class - 1))  #.05255396

#Note that the results for the two models are the same. Perhaps they are predicting the same points?
summary((predict(aicmodel,testaic,type="response") > .5)==(predict(aicres,testaic,type="response")  > .5))
#Yes, these models predict the same points. 

#Can we obtain any information from diagnostic plots?
#(This might freeze your computer)
plot(aicres)
#we see that most normality assumptions are not being fulfilled.
#Note that in residuals vs. leverage, there is huge residual (point 154634)

#Let's try another model selection algorithm:
b <- regsubsets(class ~., data = testaic, family=binomial)
res<-summary(b)



#So, will this model perform better on a smaller subset of the data? 


#Variable selection: start with small model, and get biger? 


#principal components?!

#Now, use crossvalidation



#