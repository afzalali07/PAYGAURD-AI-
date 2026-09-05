"""Generate reproducible, labelled synthetic transaction behaviour data."""
from pathlib import Path
import numpy as np
import pandas as pd

FEATURES=['amount','amount_ratio','frequency','hours_since_last','new_beneficiary','duplicate','historical_count']
def generate(seed=42,n_normal=4000,n_anomaly=650):
    rng=np.random.default_rng(seed)
    normal=pd.DataFrame({'amount':rng.lognormal(8.7,.48,n_normal),'amount_ratio':np.clip(rng.normal(1,.3,n_normal),.15,2.2),'frequency':rng.poisson(1.1,n_normal),'hours_since_last':rng.exponential(180,n_normal),'new_beneficiary':rng.binomial(1,.08,n_normal),'duplicate':rng.binomial(1,.025,n_normal),'historical_count':rng.integers(2,45,n_normal)})
    anomaly=pd.DataFrame({'amount':rng.lognormal(10.5,.75,n_anomaly),'amount_ratio':rng.uniform(3.2,12,n_anomaly),'frequency':rng.integers(3,11,n_anomaly),'hours_since_last':rng.uniform(.05,18,n_anomaly),'new_beneficiary':rng.binomial(1,.4,n_anomaly),'duplicate':rng.binomial(1,.55,n_anomaly),'historical_count':rng.integers(0,16,n_anomaly)})
    normal['label']=0;anomaly['label']=1
    return pd.concat([normal,anomaly],ignore_index=True).sample(frac=1,random_state=seed)
if __name__=='__main__':
    out=Path(__file__).parent/'data';out.mkdir(exist_ok=True)
    data=generate();split=int(len(data)*.8);data.iloc[:split].to_csv(out/'train.csv',index=False);data.iloc[split:].to_csv(out/'test.csv',index=False)
    print(f'Generated {split} training and {len(data)-split} testing rows')
