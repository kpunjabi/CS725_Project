# This piece of code performs preprocessing - on test data
# including standardization/normalization to match train data setting

import pandas as pd
import numpy as np

np.random.seed(2349784) # just some random seed ;)

# Read test.csv
df = pd.read_csv('test.csv')

# Outlier adjustment - 
# set the outlier(s), if any, to 
# nearest valid value = X_min from train.csv
def correctTheX(x):
    if (x > -121.0):
        return -122.36
    else:
        return x

df['X'] = df['X'].apply(lambda x: correctTheX(x))

# This is now the test dataset
df = df[df.X < -121.0]

# Factor out PdDistrict and DayOfWeek
dummies = []
cols = ['PdDistrict','DayOfWeek']
for col in cols:
    dummies.append(pd.get_dummies(df[col]))
    
bike_dummies = pd.concat(dummies, axis=1)
df = pd.concat((df, bike_dummies), axis=1)
df = df.drop(['PdDistrict','DayOfWeek'], axis=1)

# Standardize and Normalize X and Y to [-1,1].

X_max = df['X'].max()
X_min = df['X'].min()
Y_max = df['Y'].max()
Y_min = df['Y'].min()

# Normalize X and Y between -1 and + 1
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
df.to_csv('TestData_processed.csv', index=False)