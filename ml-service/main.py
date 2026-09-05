from pathlib import Path
import json,joblib,numpy as np,pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel,Field
from train import train,ROOT
from generate_dataset import FEATURES
app=FastAPI(title='PayGuard ML Service',version='1.0.0')
model_path=ROOT/'model'/'isolation_forest.joblib';metrics_path=ROOT/'model'/'metrics.json'
model,metrics=(joblib.load(model_path),json.loads(metrics_path.read_text())) if model_path.exists() and metrics_path.exists() else train()
class PaymentFeatures(BaseModel):
    amount:float=Field(gt=0);amountRatio:float=Field(ge=0);frequency:int=Field(ge=0);timeSinceLastPayment:float=Field(ge=0);newBeneficiary:int=Field(ge=0,le=1);duplicate:int=Field(ge=0,le=1);historicalCount:int=Field(ge=0)
@app.get('/health')
def health():return {'status':'healthy','model':'isolation-forest'}
@app.get('/metrics')
def get_metrics():return metrics
@app.post('/predict')
def predict(p:PaymentFeatures):
    row=pd.DataFrame([[p.amount,p.amountRatio,p.frequency,p.timeSinceLastPayment,p.newBeneficiary,p.duplicate,p.historicalCount]],columns=FEATURES)
    decision=float(model.decision_function(row)[0]);is_anomaly=bool(model.predict(row)[0]==-1);score=float(np.clip(.5-decision*2.2,0,1));score=max(score,.7) if is_anomaly else min(score,.64);return {'isAnomaly':is_anomaly,'anomalyScore':round(score,4)}
