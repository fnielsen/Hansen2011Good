# $Id: Hansen2010Diffusion_glm_normvalence.R,v 1.2 2010/11/08 08:51:41 fn Exp $ 

data = read.csv('/home/fnielsen/fnielsen/python/Hansen2010Diffusion_glm.csv')

detach(data)
detach(d)
d <- data
attach(d)
r1 <- glm(retweet ~ hashtag + mention + url + normvalence, family = binomial)
print("All data")
summary(r1)
detach(d)

# data[1:100, c(1,2,3,9,10,11,12)]

print("English tweets")
detach(d)
d <- data[data$englishness>0,]
attach(d)
r2 <- glm(retweet ~ hashtag + mention + url + normvalence, family = binomial)
summary(r2)
detach(d)

print("Aroused tweets >1")
detach(d)
d <- data[data$arousal>1,]
attach(d)
dnegative <- valence < 0
r3 <- glm(retweet ~ hashtag + mention + url + normvalence, family = binomial)
summary(r3)


print("English tweets, Aroused tweets >1")
detach(d)
d <- data[data$englishness>0 & data$arousal>1,]
attach(d)
r4 <- glm(retweet ~ hashtag + mention + url + normvalence, family = binomial)
summary(r4)


detach(d)
d <- data
attach(d)
negative <- normvalence < 0 
r5 <- glm(retweet ~ hashtag + mention + url + negative, family = binomial)
print("All data")
summary(r5)
detach(d)



print("English tweets")
detach(d)
d <- data[data$englishness>0,]
attach(d)
negative <- normvalence < 0
positive <- normvalence > 0
r6 <- glm(retweet ~ hashtag + mention + url + negative, family = binomial)
summary(r6)
r7 <- glm(retweet ~ hashtag + mention + url + positive, family = binomial)
summary(r7)
detach(d)

# positiveTRUE  0.32330    0.01665   19.419  < 2e-16 ***
