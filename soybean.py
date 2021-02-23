import pandas as pd
import numpy as np
from datetime import datetime

class soybean():
  def __init__(self, interval, product, expiry = False):
    self.interval = interval
    self.product = product
    self.expiry = expiry

    def load_data(self, name):
      path = '/content/QuantAnalysis/'+ self.interval + '/' + self.product + name + '.csv'
      df = pd.read_csv(path)
      df.drop(labels='Unnamed: 0', axis=1,inplace=True)
      df['Timestamp'] = pd.to_datetime(df['Timestamp'], infer_datetime_format= True)
      df.set_index(keys='Timestamp',inplace=True)
      return df

    self.c1 = load_data(self, 'c1')
    self.c2 = load_data(self, 'c2')
    self.c3 = load_data(self, 'c3')
    self.c1_c2_spread = load_data(self, ('c1-'+self.product+'c2'))
    self.c2_c3_spread = load_data(self, ('c2-'+self.product+'c3'))

    def add_expiry(self, df, name):
      df['Expiry_first'] = 'F'
      df['Expiry_last'] = 'F'
      expiry_S = ['F','H','K','N','Q','U','X','F','H']
      expiry_dates_S = ['2020-01-15','2020-03-15','2020-05-15','2020-07-15','2020-08-15','2020-09-15','2020-11-15']
      expiry_SMBO = ['F','H','K','N','Q','U','V','Z','F','H']
      expiry_dates_SMBO = ['2020-01-15','2020-03-15','2020-05-15','2020-07-15','2020-08-15','2020-09-15','2020-10-15', '2020-12-15']
      if name == 'c1':
        start = 0; end = 0
      elif name == 'c2':
        start = 1; end = 1
      elif name == 'c3':
        start = 2; end = 2
      elif name == 'c1-c2':
        start = 0; end = 1
      elif name == 'c2-c3':
        start = 1; end = 2
      if self.product =='1S':
        for i in range(0,len(df)):
          for key in range(6,-1,-1):
            if df.index[i] <= pd.Timestamp(expiry_dates_S[key]):
              df.iloc[i,-2] = expiry_S[key+start]
              df.iloc[i,-1] = expiry_S[key+end]

      elif self.product =='1SM' or self.product =='1BO':
        for i in range(0,len(df)):
          for key in range(7,-1,-1):
            if df.index[i] <= pd.Timestamp(expiry_dates_SMBO[key]):
              df.iloc[i,-2] = expiry_SMBO[key+start]
              df.iloc[i,-1] = expiry_SMBO[key+end]

      return df

    if expiry == True:
      self.c1 = add_expiry(self, self.c1, 'c1')
      self.c2 = add_expiry(self, self.c2, 'c2')
      self.c3 = add_expiry(self, self.c3, 'c3')
      self.c1_c2_spread = add_expiry(self, self.c1_c2_spread, 'c1-c2')
      self.c2_c3_spread = add_expiry(self, self.c2_c3_spread, 'c2-c3')
