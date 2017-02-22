library("rpart")
library('rpart.plot')
library(caret)
library(RevoTreeView)
library(party)
library(partykit)
library(rattle)
library(readr)
positive=dick2[dick2$RESPONSE==1,]
negative=dick2[dick2$RESPONSE==0,]
rndNegativeIdx=sample(seq_len(nrow(negative)), size = nrow(positive))

final= rbind(positive, negative[rndNegativeIdx,])
final <- read_csv("~/Desktop/dick2.csv")
final <- read_csv("~/Desktop/underSampling.csv")
#final=rbind(positive, negative[rndNegativeIdx,])
#final=dick2
final=final[,c(-1,-3,-4,-5)]
final$RESPONSE=as.factor(final$RESPONSE)
final$SAMESTATE=as.factor(final$SAMESTATE)
form <- as.formula(RESPONSE ~.)

tree.1 <- ctree(form,data=final)
,control=rpart.control(minsplit=10,cp=0.00001,maxdepth=4),method='class'
prp(tree.1)



