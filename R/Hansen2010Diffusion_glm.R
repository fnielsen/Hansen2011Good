# $Id: Hansen2010Diffusion_glm.R,v 1.6 2010/12/02 20:25:05 fn Exp $ 

detach(d)
data = read.csv('Hansen2010Diffusion_glm.csv')
data_news = read.csv('mat_rows_newsness.txt')
attach(data)
attach(data_news)

binarousal <- arousal > 2
negative <- valence < 0
positive <- valence > 0 

summary(glm(retweet ~ hashtag + mention + url + length + negative, family = binomial))
# Coefficient for NegativeTRUE is negative

summary(glm(retweet ~ hashtag + mention + url + length + negative*newsness, family = binomial))

i = abs(data$arousal)>1
d = data[i,]
dnewsness = data_news[i,]
detach(data)
attach(d)
dnegative <- valence < 0

summary(glm(retweet ~ hashtag + mention + url + dnegative, family = binomial))

summary(glm(retweet ~ hashtag + mention + url + length + dnegative*dnewsness, family = binomial))




############



r <- glm(retweet ~ hashtag + mention + url + followers + followees + log(followees+1) + length + englishness + valence + arousal + normvalence + normarousal, family = binomial)
summary(r)

r <- glm(retweet ~ hashtag + mention + url + length + arousal, family = binomial)
summary(r)

r <- glm(retweet ~ hashtag + mention + url + length + binarousal, family = binomial)
summary(r)

r <- glm(retweet ~ hashtag + mention + url + length + negative, family = binomial)
summary(r)







