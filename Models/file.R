
###############################################################
# Further processing for uploading on Kaggle
Outdata = read.csv("NB_model_out_3.csv",check.names = FALSE)
df = data.frame(Outdata ,check.names = FALSE)
df$Id = NULL
df = cbind( Id = c(seq(0,nrow(df)-1)), df )
df$Id <- format(df$Id, scientific = FALSE)
write.table(df, file = "Upload.csv", sep = ",", row.names = FALSE)