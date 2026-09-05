from pathlib import Path
import json,joblib,numpy as np
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from train import train,ROOT
from generate_dataset import transform_payloads
app=FastAPI(title='PayGuard ML Service',version='2.0.0')
model_path=ROOT/'model'/'isolation_forest.joblib';metrics_path=ROOT/'model'/'metrics.json'
def load_model():
    if model_path.exists() and metrics_path.exists():
        loaded=joblib.load(model_path)
        if isinstance(loaded,dict) and 'version' in loaded:return loaded,json.loads(metrics_path.read_text())
    return train()
bundle,metrics=load_model()
class PaymentFeatures(BaseModel):
    amount:float=Field(gt=0);amountRatio:float=Field(ge=0);userAmountRatio:float=Field(default=1,ge=0);frequency24h:int=Field(default=0,ge=0);frequency1h:int=Field(default=0,ge=0);timeSinceLastPayment:float=Field(ge=0);newBeneficiary:int=Field(ge=0,le=1);duplicate:int=Field(ge=0,le=1);historicalCount:int=Field(ge=0);transactionHour:int=Field(default=12,ge=0,le=23);newDevice:int=Field(default=0,ge=0,le=1);newLocation:int=Field(default=0,ge=0,le=1);accountChanged:int=Field(default=0,ge=0,le=1);splitPayment:int=Field(default=0,ge=0,le=1);merchantCategory:str='other'
class FeedbackItem(BaseModel):features:dict;label:int=Field(ge=0,le=1)
class RetrainRequest(BaseModel):samples:list[FeedbackItem]=Field(default_factory=list,max_length=5000)
@app.get('/health')
def health():return {'status':'healthy','model':'isolation-forest','modelVersion':bundle['version']}
@app.get('/metrics')
def get_metrics():return metrics
@app.post('/predict')
def predict(p:PaymentFeatures):
    raw={'amount':p.amount,'amount_ratio':p.amountRatio,'user_amount_ratio':p.userAmountRatio,'frequency_24h':p.frequency24h,'frequency_1h':p.frequency1h,'hours_since_last':p.timeSinceLastPayment,'new_beneficiary':p.newBeneficiary,'duplicate':p.duplicate,'historical_count':p.historicalCount,'transaction_hour':p.transactionHour,'new_device':p.newDevice,'new_location':p.newLocation,'account_changed':p.accountChanged,'split_payment':p.splitPayment,'category':p.merchantCategory};row=transform_payloads([raw]);decision=float(-bundle['model'].decision_function(row)[0]);threshold=bundle['threshold'];is_anomaly=decision>=threshold;scale=max(abs(threshold),.05);score=float(np.clip(.5+(decision-threshold)/(4*scale),0,1));score=max(score,.66) if is_anomaly else min(score,.64);return {'isAnomaly':is_anomaly,'anomalyScore':round(score,4),'rawScore':round(decision,5),'calibratedThreshold':round(threshold,5),'modelVersion':bundle['version']}
@app.post('/retrain')
def retrain(request:RetrainRequest):
    global bundle,metrics
    if len(request.samples)<5:raise HTTPException(400,'At least five reviewed outcomes are required.')
    bundle,metrics=train([{'features':x.features,'label':x.label} for x in request.samples]);return {'status':'retrained',**metrics}
