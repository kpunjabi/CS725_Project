###########################################################
# Random Forest Classiifer
# Project: San fransisco Crime Classification
##########################################################

# importing library for Random Forest--------------------
library(randomForest)

# Data Processing ---------------------------------------
train = read.csv("final_train.csv")
test_data <- read.csv("final_test.csv")
train$Hour = as.factor(train$Hour)
train$Month = as.factor(train$Month)
train$Year = as.factor(train$Year)
test_data$Hour = as.factor(test_data$Hour)
test_data$Month = as.factor(test_data$Month)
test_data$Year = as.factor(test_data$Year)

##################################################################
# training 2 Random forest classifer 
model_Rf_1 = randomForest(Category ~ PdDistrict + Month + Year + Hour,data = train,importance=TRUE, ntree = 200, mtry=2,do.trace=TRUE)
model_Rf_2 = randomForest(Category ~ PdDistrict + X + Y + Hour,  data = final,importance=TRUE, ntree = 200, mtry=2, do.trace=TRUE)

#######################################################
# Prediction on test data and writing

predClass_1 = predict(model_Rf_1, test_data, type = "prob")
predClass_2 = predict(model_Rf_2, test_data, type = "prob")

write.table(predClass_1, file = "output_RandomForest_1.csv", sep = ",", row.names = FALSE)
write.table(predClass_2, file = "output_RandomForest_2.csv", sep = ",", row.names = FALSE)

########################################
# Plotting Results

# plot of importance features 
varImpPlot(model_Rf_1)
varImpPlot(model_Rf_2)

# plot of Class Error
plot(model_Rf_1)
plot(model_Rf_2)







