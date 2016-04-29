# This piece of code performs data visualization
# we make X-Y scatter points, to see crime distribution by X and Y

import matplotlib.pyplot as plt
import pandas as pd

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

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
categories = (pd.unique(df.Category.ravel())).tolist()

# Plot X-Y scatter for each category and save figures in current directory
i=0
for cat in categories:
    cat_df = df[df.Category == cat]
    fig1 = plt.figure()
    ax = fig1.add_subplot(1,1,1)
    ax.scatter(cat_df['X'],cat_df['Y'])
    i = i+1
    fig1 = plt.gcf()
    plt.show()
    plt.draw()
    fig1.savefig(cat+'.png')
    plt.close()
