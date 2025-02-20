from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer

app = FastAPI()

# Define global objects for transformation
imputer = SimpleImputer(strategy='median')
scaler = MinMaxScaler(feature_range=(0, 1))
features = []


def train_model(file: UploadFile = File(...)):
    global imputer, scaler, features, model
    
    df_train = read_file(file)
    
    if 'TARGET' not in df_train.columns:
        raise HTTPException(status_code=400, detail="TARGET column is missing from training data.")
    
    X = df_train.drop(columns=['TARGET'])
    y = df_train['TARGET']
    
    features = X.columns.tolist()
    
    # Fit and transform training data
    imputer.fit(X)
    X_transformed = imputer.transform(X)
    scaler.fit(X_transformed)
    X_transformed = scaler.transform(X_transformed)
    
    # Train the model
    model.fit(X_transformed, y)
    
    return {"message": "Model trained successfully", "features": features}

@app.post("/predict")
def predict(file: UploadFile = File(...)):
    global imputer, scaler, features, model
    
    df_test = read_file(file)
    
    missing_features = set(features) - set(df_test.columns)
    if missing_features:
        raise HTTPException(status_code=400, detail=f"Missing features: {missing_features}")
    
    df_test = df_test[features]  # Ensure column order
    
    X_test_transformed = imputer.transform(df_test)
    X_test_transformed = scaler.transform(X_test_transformed)
    
    predictions = model.predict(X_test_transformed)
    
    return {"predictions": predictions.tolist()}
