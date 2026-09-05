"""Generate privacy-safe transaction patterns modeled on realistic payment behaviour."""
from pathlib import Path
import numpy as np
import pandas as pd

FEATURES=['log_amount','amount_ratio','user_amount_ratio','frequency_24h','frequency_1h','log_hours_since_last','new_beneficiary','duplicate','log_historical_count','hour_sin','hour_cos','new_device','new_location','account_changed','split_payment','category_risk']
CATEGORY_RISK={'payroll':.1,'rent':.12,'inventory':.25,'technology':.35,'travel':.45,'professional_services':.3,'other':.4}

def _features(raw):
    hour=raw['transaction_hour'].to_numpy()
    return pd.DataFrame({'log_amount':np.log1p(raw.amount),'amount_ratio':raw.amount_ratio,'user_amount_ratio':raw.user_amount_ratio,'frequency_24h':raw.frequency_24h,'frequency_1h':raw.frequency_1h,'log_hours_since_last':np.log1p(raw.hours_since_last),'new_beneficiary':raw.new_beneficiary,'duplicate':raw.duplicate,'log_historical_count':np.log1p(raw.historical_count),'hour_sin':np.sin(2*np.pi*hour/24),'hour_cos':np.cos(2*np.pi*hour/24),'new_device':raw.new_device,'new_location':raw.new_location,'account_changed':raw.account_changed,'split_payment':raw.split_payment,'category_risk':raw.category.map(CATEGORY_RISK).fillna(.4)})

def generate(seed=42,n_normal=7000,n_anomaly=1200):
    rng=np.random.default_rng(seed);cats=np.array(list(CATEGORY_RISK))
    normal=pd.DataFrame({'amount':rng.lognormal(8.8,.65,n_normal),'amount_ratio':np.clip(rng.lognormal(-.03,.3,n_normal),.15,2.6),'user_amount_ratio':np.clip(rng.lognormal(0,.45,n_normal),.1,3),'frequency_24h':rng.poisson(1.2,n_normal),'frequency_1h':rng.binomial(2,.08,n_normal),'hours_since_last':rng.exponential(150,n_normal),'new_beneficiary':rng.binomial(1,.07,n_normal),'duplicate':rng.binomial(1,.018,n_normal),'historical_count':rng.negative_binomial(4,.2,n_normal)+1,'transaction_hour':np.clip(np.rint(rng.normal(13,4,n_normal)),0,23),'new_device':rng.binomial(1,.035,n_normal),'new_location':rng.binomial(1,.025,n_normal),'account_changed':rng.binomial(1,.006,n_normal),'split_payment':rng.binomial(1,.01,n_normal),'category':rng.choice(cats,n_normal,p=[.1,.08,.3,.18,.08,.12,.14])})
    anomaly=pd.DataFrame({'amount':rng.lognormal(10.7,.9,n_anomaly),'amount_ratio':rng.uniform(2.8,14,n_anomaly),'user_amount_ratio':rng.uniform(2.5,12,n_anomaly),'frequency_24h':rng.integers(3,13,n_anomaly),'frequency_1h':rng.integers(1,7,n_anomaly),'hours_since_last':rng.uniform(.01,12,n_anomaly),'new_beneficiary':rng.binomial(1,.42,n_anomaly),'duplicate':rng.binomial(1,.38,n_anomaly),'historical_count':rng.integers(0,14,n_anomaly),'transaction_hour':rng.choice([0,1,2,3,4,22,23],n_anomaly),'new_device':rng.binomial(1,.58,n_anomaly),'new_location':rng.binomial(1,.46,n_anomaly),'account_changed':rng.binomial(1,.34,n_anomaly),'split_payment':rng.binomial(1,.43,n_anomaly),'category':rng.choice(cats,n_anomaly)})
    # Create varied anomaly families instead of making every signal extreme.
    masks=rng.random((n_anomaly,5));anomaly.loc[masks[:,0]<.35,['amount_ratio','user_amount_ratio']]=rng.uniform(.8,2.2,(sum(masks[:,0]<.35),2));anomaly.loc[masks[:,1]<.45,'duplicate']=0;anomaly.loc[masks[:,2]<.45,'account_changed']=0;anomaly.loc[masks[:,3]<.45,'split_payment']=0;anomaly.loc[masks[:,4]<.35,['new_device','new_location']]=0
    normal['label']=0;anomaly['label']=1;raw=pd.concat([normal,anomaly],ignore_index=True);features=_features(raw);features['label']=raw.label;return features.sample(frac=1,random_state=seed).reset_index(drop=True)

def transform_payloads(rows):
    raw=pd.DataFrame(rows);defaults={'amount':0,'amount_ratio':1,'user_amount_ratio':1,'frequency_24h':0,'frequency_1h':0,'hours_since_last':9999,'new_beneficiary':0,'duplicate':0,'historical_count':0,'transaction_hour':12,'new_device':0,'new_location':0,'account_changed':0,'split_payment':0,'category':'other'}
    for key,value in defaults.items():
        if key not in raw:raw[key]=value
    return _features(raw)

if __name__=='__main__':
    out=Path(__file__).parent/'data';out.mkdir(exist_ok=True);data=generate();split=int(len(data)*.8);data.iloc[:split].to_csv(out/'train.csv',index=False);data.iloc[split:].to_csv(out/'test.csv',index=False);print(f'Generated {split} training and {len(data)-split} held-out rows')
