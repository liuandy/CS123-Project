setwd("C:/Users/Andy/Dropbox/Schoolwork/CS123/Project Data")

data <- read.table("census-income.data", sep = ",", header =F, na.strings = "NA")
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
test1 <- data.frame(age = cont_data$V1, class = class)
test1.logr <- glm(class ~ age, data = test1, family = binomial)

summary(predict(test1.logr, test1, type = "response"))

# From here, we see that with only age, we do not have nearly enough predictive power.
# Everything is classified as below median income.

# Let's look at wage per hour
summary(cont_data$V6)
# We stop to note that this data makes absolutely no sense.
# 

test2 <- data.frame(age = cont_data$V1, wph = cont_data$V6, class = class)
test2.logr <- glm(class ~ age + wph, data = test2, family = binomial)

sum(predict(test2.logr, test2, "response") > .5)
# We make four classifications into 1.

# Let's try something that is tried and true in income classification
test3 <- data.frame(educ = data$V5, class = class)
test3.logr <- glm(class ~ factor(educ), data = test3, family = binomial)

# 3056 classifications into the 50,000+ category. That's lovely.
sum(predict(test3.logr, test3, "response") > .5)

test3.misclass <- class - (predict(test3.logr, test3, "response") > .5)

# Misclassing 50,000+ as 50,000-
sum(test3.misclass == - 1) / sum(class)

# Misclassing 50,000- as 50,000+
sum(test3.misclass == 1)/ abs(sum(class - 1))

# So, we see from this that education is a great stand-alone predictor of income.
# That's rather unsurprising.

niu <- apply(data, 1, function(x) (sum(x == " Not in universe") > 0))
sum(niu)

missing <- apply(data, 1, function(x) (sum(x == " ?") > 0))
sum(missing)