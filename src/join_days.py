import pandas as pd
import matplotlib.pyplot as plt
import base as b 
import digisonde as dg 
import numpy as np 
import datetime as dt 

b.config_labels()






def join_iono_days(
        site, 
        dn,
        parameter = 'drift',
        number = 4,
        cols = list(range(3, 8, 1))
        ):

    out = []
    
    for i in range(number):
        
        delta = dt.timedelta(days = i)
        
        file =  dg.dn2fn(dn + delta, site)
        
        df = dg.IonoChar(file, cols, sum_from = None)
        
        if parameter == 'drift':
            
            out.append(df.drift()['vz'].to_frame(site))
        else:
            out.append(df.heights)
        
    return pd.concat(out).sort_index()

def plot_multi_sites():
    
    fig, ax = plt.subplots(figsize = (12, 6))
    

    site = ['SAA0K', 'BVJ03', 'CAJ2M'][2]
    
    ds = join_iono_days(
            site, 
            dn = dt.datetime(2015, 12, 19) ,
            cols = list(range(3, 8, 1))
            )
    
    ds.plot(ax = ax)
    
dates = [
    dt.datetime(2015, 12, 2, 9), 
    dt.datetime(2015, 12, 13, 9),
    dt.datetime(2015, 12, 16, 9), 
    # dt.datetime(2015, 12, 18, 9),
    dt.datetime(2015, 12, 29, 9)
    ]

# dn = dates[0]


def quiet_time_avg(
        site = 'SAA0K',
        cols = list(range(3, 8, 1)), 
        smooth = 10
        ):
    out = []
    
    for dn in dates:
        
        file =  dg.dn2fn(dn, site)
        
        df = dg.IonoChar(file, cols, sum_from = None)
        
        ds = df.drift(smooth = smooth).set_index('time')['vz'].dropna()
        
        out.append(ds.sort_index().to_frame(dn.day))
        
    df = pd.concat(out, axis = 1).mean(axis = 1)
    return df.sort_index().iloc[:-1]
    

def float_to_time2(float_time):
    hour, minutes = tuple(str(float_time).split('.'))

    minute = round(float('0.' + minutes) * 60)
    hour = int(hour)
    return hour, minute


def renew_index_from_date(df, dn):
    
    out = []
    for t in df.index:
        try:
            hour, minute = float_to_time2(t)
            
            delta = dt.timedelta(
                hours = hour, 
                minutes = minute
                )
            out.append(dn + delta)
        except:
            
            continue
        
    df.index = out 
    
    return df 


def repeat_quiet_days(
        site, number = 4):

    out = []
    
    for i in range(number):
        
        delta = dt.timedelta(days = i)
    
        dn = dt.datetime(2015, 12, 19) + delta
        
        df = quiet_time_avg(site)
        
        out.append(renew_index_from_date(df, dn))
        
    return pd.concat(out)


