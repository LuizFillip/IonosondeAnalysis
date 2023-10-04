import pandas as pd
import base as b
import os 


def concat_all_pre_values(site = 'saa'):
    
    p = f'digisonde/data/drift/PRE/{site}/'
    out = []
    
    for f in os.listdir(p):
        
        if 'R' not in f:
            
            df = b.load(p + f)
            
            df = df.rename(columns = {'vzp': 'vp'})
            out.append(df)
            
    df = pd.concat(out).sort_index()  
    
    df.index = pd.to_datetime(df.index.date)
    
    
    return df['vp'].to_frame('vp')

def Filename(df):
    
    save_in = 'digisonde/data/PRE/saa/'
    
    ys = df.index[0].year
    ye = df.index[-1].year
    
    return f'{save_in}{ys}_{ye}.txt'

def main():
    
    df = concat_all_pre_values(site = 'saa')
    df.to_csv(Filename(df))