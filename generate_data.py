import pandas as pd
import numpy as np
import config as cfg


class GenerateData:

    def __init__(self):
        self.confirmed_url = cfg.url['confirmed']
        self.death_url = cfg.url['deaths']
        self.df_confirmed = None
        self.df_deaths = None

    def process_data(self, data, cntry='India', window=3):
        data = data[data['Country/Region'] == cntry]
        data = data.T[4:].sum(axis=1).diff().rolling(window=window).sum()[40:]
        final_data = pd.DataFrame(data, columns=['Total'])
        return final_data

    def get_data(self):
        self.df_confirmed = pd.read_csv(self.confirmed_url)
        self.df_deaths = pd.read_csv(self.death_url)

    def get_total_world(self, df):
        total = df.iloc[:, -1].sum()
        return total

    def get_total_country(self, df, cntry='India'):
        total = df[df['Country/Region'] == cntry].iloc[:, -1].sum()
        return total

    def get_stat_world(self):
        data = GenerateData()
        data.get_data()
        confirmed = data.get_total_world(data.df_confirmed)
        deaths = data.get_total_world(data.df_deaths)
        return [confirmed, deaths]


if __name__ == '__main__':
    d = GenerateData()
    d.get_data()
