
##################################################################
# Naive Bayes Classifier 
# Project : San fransisco Crime Classification
##################################################################
# importing Library 
library(klaR)
data = read.csv("final_train.csv")
test_data = read.csv("final_test.csv")

# Data-processing
data$Hour = as.factor(data$Hour)
data$Month = as.factor(data$Month)
data$Year = as.factor(data$Year)
test_data$Hour = as.factor(test_data$Hour)
test_data$Month = as.factor(test_data$Month)
test_data$Year = as.factor(test_data$Year)

# Divinding into Train set and Cross-validation set
indexes = sample(1:nrow(data), size=0.2*nrow(data))
cross = data[indexes,]
train = data[-indexes,]

##############################################################
# Training three Naive Bayes on different attributes

#model 1 
model_NB_2 = NaiveBayes(Category~X+Y, data = train)
predClass_NB_2 = predict(model_NB_2,cross, type = "class")

#model 2
model_NB_1 = NaiveBayes(Category~.,  data = train)
predClass_NB_1 = predict(model_NB_1,cross, type = "class")

#model 3
model_NB_3 = NaiveBayes(Category~ PdDistrict+ Hour+Year+Month + DayOfWeek, data= train)
predClass_NB_3 = predict(model_NB_3,cross, type = "class")

#############################################################
# Cross-Validation

p1 = data.frame(predClass_NB_1)
rm(predClass_NB_1)
p1_class = data.frame(p1$class)

p2 = data.frame(predClass_NB_2)
rm(predClass_NB_2)
p2_class = data.frame(p2$class)

p3 = data.frame(predClass_NB_3)
rm(predClass_NB_3)
p3_class = data.frame(p3$class)

t = data.frame(cross$Category)
colSums(p1_class == t)/nrow(t)
colSums(p2_class == t)/nrow(t)
colSums(p3_class == t)/nrow(t)


############################################################
# Prediction on Test Data
test_p1 = predict(model_NB_1, test_data, type = "class")
out_model_1= data.frame(test_p1)
rm(test_p1)
test_p2 = predict(model_NB_2, test_data, type = "class")
out_model_2= data.frame(test_p2)
rm(test_p2)
test_p3 = predict(model_NB_3, test_data, type = "class")
out_model_3= data.frame(test_p3)
rm(test_p3)

##############################
# Writing in output format
out_model_1$class = NULL
out_model_2$class = NULL
out_model_3$class = NULL

out_model_1 = cbind( Id = c(seq(0,nrow(out_model_1)-1)), out_model_1 )
out_model_2 = cbind( Id = c(seq(0,nrow(out_model_2)-1)), out_model_2 )
out_model_3 = cbind( Id = c(seq(0,nrow(out_model_2)-1)), out_model_3 )

cols <- names(out_model_1)[2:ncol(out_model_1)]
out_model_1[,(cols)] = round(out_model_1[,cols],4)
out_model_2[,(cols)] = round(out_model_2[,cols],4)
out_model_3[,(cols)] = round(out_model_3[,cols],4)

out_model_1$Id <- format(out_model_1$Id, scientific = FALSE)
out_model_2$Id <- format(out_model_2$Id, scientific = FALSE)
out_model_3$Id <- format(out_model_3$Id, scientific = FALSE)

write.table(out_model_1, file = "NB_model_out_1.csv", sep = ",", row.names = FALSE)
write.table(out_model_2, file = "NB_model_out_2.csv", sep = ",", row.names = FALSE)
write.table(out_model_3, file = "NB_model_out_3.csv", sep = ",", row.names = FALSE)


# Log-loss function 
cross_act = data.frame(cross$Category)
cross_act = model.matrix(~ . + 0, data=cross_act, contrasts.arg = lapply(cross_act, contrasts, contrasts=FALSE))

p1$class = NULL
p2$class = NULL
p3$class = NULL

loss = MultiLogLoss(cross_act[2,], p1[2,])

