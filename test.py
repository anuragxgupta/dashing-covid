import pandas as pd

# Creating the dataframe
CONF_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
df = pd.read_csv(CONF_URL)
df.to_csv('data.csv')
# print(df.T.head(10))
ndf = df[df['Country/Region'] == 'US']
print(ndf.T[4:].head(10))
ndf = ndf.T[4:].sum(axis='columns')#.diff()#.rolling(window=3).mean()[3:]
print(ndf.head(10))
ndf = ndf.diff()#.rolling(window=3).mean()[3:]
print(ndf.head(10))
ndf = ndf.rolling(window=3).mean()#[3:]
print(ndf.head(10))