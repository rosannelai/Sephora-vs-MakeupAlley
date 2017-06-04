import pandas as pd
import glob2
from os.path import basename as bs
import os.path

all_data = pd.DataFrame()

for f in glob2.glob("./sephora/*.csv"):
    print f
    if os.path.getsize(f) > 0:
        df = pd.read_csv(f, index_col = None, header=None, names=None, sep='|', skiprows = 0)
        df.index = [bs(f)] * len(df)
        df.to_csv("sephora_all.csv", encoding='utf8', mode='a', header=False, sep='\t')
    print df
    
