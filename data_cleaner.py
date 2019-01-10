import pandas as pd
import numpy as np

def read_mta_file(path, pickle_ok=True):
    """Read the raw MTA turnstyle data and return a dataframe cleaned up as follows -
       * Dates between 04/01/2018 and 06/22/2018
       * Column names stripped
       * Column Date and Time combined into one column called date_time and 
         of the proper Numpy datetime type
       * Turnstile ID created from Unit + SCP
       * New column 'b_weekday' boolean indicates whether data is from a weekday (monday-friday)
    """
    if pickle_ok:
        try:
            spring = pd.read_pickle("spring.pickle")
            return spring
        except:
            pass
        
        
    raw_data = pd.read_csv(path)
    
    # trim by date first so that it's easier to hack on
    our_rows = raw_data[(raw_data.Date >= '04/01/2018') & 
                     (raw_data.Date < '06/22/2018')]
    spring = our_rows.copy()
    assert(spring.shape[0] == 2307938)
    
    # strip the Exists column name
    spring.columns = spring.columns.str.strip()
    
    # make turnstile ids
    spring['ts_id'] = spring.Unit + '_' + spring.SCP
        
    spring['date_time'] = pd.to_datetime(spring.Date + ' ' + spring.Time, format="%m/%d/%Y %X")
    spring['b_weekday'] = spring.date_time.dt.weekday < 5
    
    spring = spring.drop(columns=['Date', 'Time', 'Division', 'Line Name'])    
    spring.to_pickle("spring.pickle")
    
    return spring
