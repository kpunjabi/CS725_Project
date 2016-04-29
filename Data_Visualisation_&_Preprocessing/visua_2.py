# This piece of code performs data visualization
# we make a crime intensity map

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Read the raw dataset (train.csv)
df = pd.read_csv('train.csv')

# Outlier removal: there are some spurious points with X values > -121.0
df = df[df.X < -121.0]

# String massaging: get rid of '/' in category names
df['Category'] = df['Category'].apply(lambda x: "LARCENY_THEFT" if(x=="LARCENY/THEFT") else x)
df['Category'] = df['Category'].apply(lambda x: "FORGERY_COUNTERFEITING" if(x=="FORGERY/COUNTERFEITING") else x)
df['Category'] = df['Category'].apply(lambda x: "DRUG_NARCOTIC" if(x=="DRUG/NARCOTIC") else x)
df['Category'] = df['Category'].apply(lambda x: "PORNOGRAPHY_OBSCENE_MAT" if(x=="PORNOGRAPHY/OBSCENE MAT") else x)

districts = (pd.unique(df.PdDistrict.ravel())).tolist()
# print(districts)
categories = (pd.unique(df.Category.ravel())).tolist()
# print(categories)

# The Idea for Crime Intensity Map is that
# we will divide the entire geography (X and Y)
# into a grid of 0.01 x 0.01

# Calculations required for making the grid
X_max = df['X'].max()
X_min = df['X'].min()
Y_max = df['Y'].max()
Y_min = df['Y'].min()
# Scaling
df['X'] = df['X'].round(decimals=2) * 100
df['Y'] = df['Y'].round(decimals=2) * 100
df['X'] = df['X'].apply(lambda x: int(x))
df['Y'] = df['Y'].apply(lambda y: int(y))

X_max = df['X'].max()
X_min = df['X'].min()
Y_max = df['Y'].max()
Y_min = df['Y'].min()

# grid dimensions = (Y_max - Y_min)+1 x (X_max - X_min)+1
crime_map = []
for i in range(int(Y_max - Y_min)+1):
    crime_map.append([])
    for j in range(int(X_max - X_min)+1):
        df_count = df[df['X'] == X_min + j]
        df_count = df_count[df_count['Y'] == Y_min + i]
        a = ((df_count['X']).value_counts()).tolist()
        if(len(a) > 0):
            crime_map[i].append(int(a[0]))
        else:
            crime_map[i].append(0)

# Debugging prints
# print(crime_map)
# print(sum( x for sublist in crime_map for x in sublist ))

#Change crime_map to log scale for better visualization
for i in range(int(Y_max - Y_min)+1):
    for j in range(int(X_max - X_min)+1):
        if(crime_map[i][j] > 0):
            crime_map[i][j] = np.log(crime_map[i][j])
            
# Plot the map
fig = plt.figure(2)
cmap2 = LinearSegmentedColormap.from_list('my_colormap',
                                           ['yellow','orange','brown'],
                                           256)
img2 = plt.imshow(crime_map,interpolation='nearest',
                    cmap = cmap2,
                    origin='lower')
plt.colorbar(img2,cmap=cmap2)
fig.savefig("crime_intensity.png")