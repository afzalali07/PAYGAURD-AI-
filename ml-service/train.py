"""Train, calibrate, version, and evaluate PayGuard's Isolation Forest."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,joblib,numpy as np,pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix,accuracy_score,precision_score,recall_score,f1_score
from generate_dataset import FEATURES,generate,transform_payloads
ROOT=Path(__file__).parent

def train(feedback=None):
    data=generate();split=int(len(data)*.8);training,test=data.iloc[:split].copy(),data.iloc[split:].copy();feedback=feedback or []
    if feedback:
        frame=transform_payloads([normalize_feedback(x['features']) for x in feedback]);frame['label']=[int(x['label']) for x in feedback];training=pd.concat([training,frame[frame.label==0]],ignore_index=True);test=pd.concat([test,frame],ignore_index=True)
    contamination=float(np.clip((training.label.sum()+25)/len(training),.06,.2));model=IsolationForest(n_estimators=320,contamination=contamination,random_state=42,n_jobs=-1,max_samples='auto').fit(training[training.label==0][FEATURES]);normal_scores=-model.decision_function(training[training.label==0][FEATURES]);threshold=float(np.quantile(normal_scores,.975));test_scores=-model.decision_function(test[FEATURES]);pred=(test_scores>=threshold).astype(int);truth=test.label.astype(int).to_numpy();tn,fp,fn,tp=confusion_matrix(truth,pred,labels=[0,1]).ravel();version='iforest-'+datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')+'-'+hashlib.sha1(str(len(feedback)).encode()).hexdigest()[:6]
    metrics={'modelVersion':version,'trainedAt':datetime.now(timezone.utc).isoformat(),'calibratedThreshold':threshold,'contamination':contamination,'feedbackSamples':len(feedback),'accuracy':float(accuracy_score(truth,pred)),'precision':float(precision_score(truth,pred,zero_division=0)),'recall':float(recall_score(truth,pred,zero_division=0)),'f1':float(f1_score(truth,pred,zero_division=0)),'falsePositiveRate':float(fp/(fp+tn) if fp+tn else 0),'confusionMatrix':{'tn':int(tn),'fp':int(fp),'fn':int(fn),'tp':int(tp)},'testSamples':len(test)};bundle={'model':model,'threshold':threshold,'version':version};out=ROOT/'model';out.mkdir(exist_ok=True);joblib.dump(bundle,out/'isolation_forest.joblib');(out/'metrics.json').write_text(json.dumps(metrics,indent=2));return bundle,metrics
if __name__=='__main__':print(json.dumps(train()[1],indent=2))

def normalize_feedback(x):
    return {'amount':x.get('amount',0),'amount_ratio':x.get('amountRatio',1),'user_amount_ratio':x.get('userAmountRatio',1),'frequency_24h':x.get('frequency24h',0),'frequency_1h':x.get('frequency1h',0),'hours_since_last':x.get('timeSinceLastPayment',9999),'new_beneficiary':x.get('newBeneficiary',0),'duplicate':x.get('duplicate',0),'historical_count':x.get('historicalCount',0),'transaction_hour':x.get('transactionHour',12),'new_device':x.get('newDevice',0),'new_location':x.get('newLocation',0),'account_changed':x.get('accountChanged',0),'split_payment':x.get('splitPayment',0),'category':x.get('merchantCategory','other')}
