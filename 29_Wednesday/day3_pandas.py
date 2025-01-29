#Example use case of pandas dataframes.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#read in the dataframe for the file
df = pd.read_csv("laser_data.csv", sep=',', engine='python')

df

#divide the datafram into pairs of columns.
df_1 = df[['Time_I','Intensity']]
df_2 = df[['Time_L','Laser']]
df_3 = df[['Time_V','Vert_Emit']]
df_4 = df[['Time_H','Horz_Emit']]
df_5 = df[['Time_C','Linac_Current']]

print(df_1)

#Method 1 of cleaning data
df_1.loc[:, 'Time_I'] = df_1['Time_I'].replace('\s+\s', None, regex=True)
df_1.loc[:, 'Intensity'] = df_1['Intensity'].replace('\s+\s', None, regex=True)
df_1 = df_1.dropna()

#Method 2 of cleaning data
dex = df_2[df_2['Time_L'].str.contains('\s+\s', regex=True)].index[0]
df_2 = df_2.iloc[:dex]

#Method 2, one line
df_3 = df_3.iloc[:df_3[df_3['Time_V'].str.contains('\s+\s', regex=True)].index[0]]
df_4 = df_4.iloc[:df_4[df_4['Time_H'].str.contains('\s+\s', regex=True)].index[0]]

#df_5 doesn't need cleaning actually

#Cast data as correct types, specific timestamp format

print(df_1.dtypes)

df_1.loc[:, 'Time_I'] = pd.to_datetime(df_1['Time_I'], format='%a %b %d %H:%M:%S.%f')
df_1.loc[:, 'Intensity'] = df_1['Intensity'].astype(float)
df_2.loc[:, 'Time_L'] = pd.to_datetime(df_2['Time_L'], format='%a %b %d %H:%M:%S.%f')
df_2.loc[:, 'Laser'] = df_2['Laser'].astype(int)
df_3.loc[:, 'Time_V'] = pd.to_datetime(df_3['Time_V'], format='%a %b %d %H:%M:%S.%f')
df_3.loc[:, 'Vert_Emit'] = df_3['Vert_Emit'].astype(float)
df_4.loc[:, 'Time_H'] = pd.to_datetime(df_4['Time_H'], format='%a %b %d %H:%M:%S.%f')
df_4.loc[:, 'Horz_Emit'] = df_4['Horz_Emit'].astype(float)
df_5.loc[:, 'Time_C'] = pd.to_datetime(df_5['Time_C'], format='%a %b %d %H:%M:%S.%f')
df_5.loc[:, 'Linac_Current'] = df_5['Linac_Current'].astype(float)

print(df_1)
print(df_1.dtypes)

#Set index to timestable, and Resample data at 10s intervals
print(df_1.set_index('Time_I'))

df_1s = df_1.set_index('Time_I').resample('10s').max()
df_2s = df_2.set_index('Time_L').resample('10s', origin=df_1.first_valid_index()).bfill()
df_3s = df_3.set_index('Time_V').resample('10s', origin=df_1.first_valid_index()).max()
df_4s = df_4.set_index('Time_H').resample('10s', origin=df_1.first_valid_index()).max()
df_5s = df_5.set_index('Time_C').resample('10s', origin=df_1.first_valid_index()).max()

print(df_1s)

#Merge dataset so it shares a common dataset
df_m = pd.merge(df_1s, df_2s, how='left', left_index=True, right_index=True)
df_m = pd.merge(df_m, df_3s, how='left', left_index=True, right_index=True)
df_m = pd.merge(df_m, df_4s, how='left', left_index=True, right_index=True)
df_m = pd.merge(df_m, df_5s, how='left', left_index=True, right_index=True)

#Backfill sparse data, and filter data by operating conditions
df_m['Laser'] = df_m['Laser'].ffill()
df_mf = df_m.query('Intensity > 1').query('Linac_Current > 5').query('Vert_Emit > 5')
df_mf['Laser'] = (df_mf['Laser']-88)

#Plot time series of experiment variables
df_mf.plot()
plt.show()

#plot scatterplot comparing data at different laser conditions
ax = df_mf.query('Laser == 0').plot(kind='scatter', color='green', x='Intensity',y='Vert_Emit')
df_mf.query('Laser == 42').plot(kind='scatter', color='blue', x='Intensity',y='Vert_Emit', ax=ax)
ax.legend(["Laser at 0","Laser at 42"])
plt.show()

#Find mean and standard deviation by Laser condition.
df_pivot = pd.pivot_table(df_mf, index=['Laser'], aggfunc=['mean','std']).dropna()

print(df_pivot)

#Find z values (statistically significance), of difference with respect to 0.
df_z = (df_pivot['mean']- df_pivot['mean'].loc[0]) / np.sqrt( df_pivot['std']**2 + df_pivot['std'].loc[0]**2 )
df_z = df_z.loc[[6,42]]

print(df_z)

#No statistical significance! Better luck next time.
