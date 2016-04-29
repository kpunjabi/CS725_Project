# This piece of code performs data preprocessing
# including standardization/normalization

import pandas as pd
import numpy as np

np.random.seed(2349784) # just some random seed ;)

# Read the raw dataset (train.csv)
df = pd.read_csv('train.csv')

# Create another data frame to separate out Category
df_Category = df.copy()
df_Category = df_Category.drop(['Dates', 'Descript', 'DayOfWeek', 'PdDistrict', 'Resolution', 'Address', 'X', 'Y'], axis=1)
df_Category.info()

# String massaging: get rid of '/' in category names
df_Category['Category'] = df_Category['Category'].apply(lambda x: "LARCENY_THEFT" if(x=="LARCENY/THEFT") else x)
df_Category['Category'] = df_Category['Category'].apply(lambda x: "FORGERY_COUNTERFEITING" if(x=="FORGERY/COUNTERFEITING") else x)
df_Category['Category'] = df_Category['Category'].apply(lambda x: "DRUG_NARCOTIC" if(x=="DRUG/NARCOTIC") else x)
df_Category['Category'] = df_Category['Category'].apply(lambda x: "PORNOGRAPHY_OBSCENE_MAT" if(x=="PORNOGRAPHY/OBSCENE MAT") else x)

# Factor out Category into binary 0/1 variables
dummies = []
cols = ['Category']
for col in cols:
    dummies.append(pd.get_dummies(df_Category[col]))

bike_dummies = pd.concat(dummies, axis=1)
df_Category = pd.concat((df_Category, bike_dummies), axis=1)
df_Category = df_Category.drop(['Category'], axis=1)


# Now, work on the main train dataset

# First, outlier removal: there are some spurious points with X values > -121.0
df = df[df.X < -121.0]

# Factor out PdDistrict and DayOfWeek
dummies = []
cols = ['PdDistrict','DayOfWeek']
for col in cols:
    dummies.append(pd.get_dummies(df[col]))
    
bike_dummies = pd.concat(dummies, axis=1)
df = pd.concat((df, bike_dummies), axis=1)
df = df.drop(['PdDistrict','DayOfWeek', 'Descript', 'Resolution'], axis=1)

# Standardize and Normalize X and Y to [-1,1].
# Raw ranges are
# X --> -122.51 to -122.36
# Y --> 37.71 to 37.82

X_max = df['X'].max()
X_min = df['X'].min()
Y_max = df['Y'].max()
Y_min = df['Y'].min()

df['X'] = df['X'].apply(lambda x: (2 * x - X_max - X_min)/(X_max - X_min))
df['Y'] = df['Y'].apply(lambda y: (2 * y - Y_max - Y_min)/(Y_max - Y_min))

X_max = df['X'].max()
X_min = df['X'].min()
Y_max = df['Y'].max()
Y_min = df['Y'].min()

# Standardize X and Y as ((x - mean) / stddev)
X_mean = df['X'].mean()
X_std = df['X'].std()
Y_mean = df['Y'].mean()
Y_std = df['Y'].std()
# print(X_mean, X_std, Y_mean, Y_std)
df['X'] = df['X'].apply(lambda x: (x - X_mean)/(X_std))
df['Y'] = df['Y'].apply(lambda y: (y - Y_mean)/(Y_std))

# Helper functions to extract month, year and hour from timestamp
def getMonth(x):
    mylist = x.split()
    nums = mylist[0].split('-')
    return int(nums[1])
    
def getYear(x):
    mylist = x.split()
    nums = mylist[0].split('-')
    return int(nums[0])
    
def getHour(x):
    mylist = x.split()
    hours = mylist[1].split(':')
    return int(hours[0])

df['Month'] = df['Dates'].apply(lambda x: getMonth(x))
df['Year'] = df['Dates'].apply(lambda x: getYear(x))
df['Hour'] = df['Dates'].apply(lambda x: getHour(x))

# Drop Dates
df = df.drop(['Dates'], axis=1)

# Write to a new csv file
df.to_csv('TrainData_processed.csv', index=False)