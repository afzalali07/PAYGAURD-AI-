"""Train Isolation Forest and persist genuine held-out evaluation metrics."""
from pathlib import Path
import json,joblib,pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix,accuracy_score,precision_score,recall_score,f1_score
from generate_dataset import FEATURES,generate
ROOT=Path(__file__).parent
def train():
    data=generate();split=int(len(data)*.8);train_data,test=data.iloc[:split],data.iloc[split:]
    model=IsolationForest(n_estimators=240,contamination=.14,random_state=42,n_jobs=-1).fit(train_data[FEATURES])
    pred=(model.predict(test[FEATURES])==-1).astype(int);truth=test.label.values
    tn,fp,fn,tp=confusion_matrix(truth,pred,labels=[0,1]).ravel()
    metrics={'accuracy':accuracy_score(truth,pred),'precision':precision_score(truth,pred,zero_division=0),'recall':recall_score(truth,pred,zero_division=0),'f1':f1_score(truth,pred,zero_division=0),'falsePositiveRate':fp/(fp+tn) if fp+tn else 0,'confusionMatrix':{'tn':int(tn),'fp':int(fp),'fn':int(fn),'tp':int(tp)},'testSamples':len(test)}
    out=ROOT/'model';out.mkdir(exist_ok=True);joblib.dump(model,out/'isolation_forest.joblib');(out/'metrics.json').write_text(json.dumps(metrics,indent=2));return model,metrics
if __name__=='__main__':print(train()[1])
