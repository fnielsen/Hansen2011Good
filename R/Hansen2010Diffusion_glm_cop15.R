# $Id: Hansen2010Diffusion_glm_cop15.R,v 1.5 2010/12/02 20:25:43 fn Exp $ 

data = read.csv('Hansen2010Diffusion_cop15glm.csv')
data_news = read.csv('mat_rows_newsness.txt')
attach(data)
attach(data_news)


binarousal <- arousal > 2
negative <- valence < 0
positive <- valence > 0 
binambivalence <- ambivalence > 2

summary(glm(retweet ~ hashtag + mention + url + negative, family = binomial))
# Coefficient for NegativeTRUE is positive

summary(glm(retweet ~ hashtag + mention + url + log(length) + negative, family = binomial))
# Coefficient for NegativeTRUE is negative

# So the result switches depending on the presence of the length covariate. :-(


summary(glm(retweet ~ hashtag + mention + url + length + negative*newsness, family = binomial))



i = abs(data$arousal)>1
d = data[abs(data$arousal)>1,]
dnewsness = data_news[i,]
detach(data)
attach(d)
dnegative <- valence < 0
dpositive <- valence > 0 

summary(glm(retweet ~ hashtag + mention + url + dnegative, family = binomial))

summary(glm(retweet ~ hashtag + mention + url + dnegative*dnewsness, family = binomial))




############ 

# log(length) gives lower AIC
summary(glm(retweet ~ hashtag + mention + url + log(length) + dnegative, family = binomial))

# log(length) + lengthnourl gives significant drop in AIC.
summary(glm(retweet ~ hashtag + mention + url + log(length) + lengthnourl, family = binomial))
