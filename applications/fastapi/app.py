from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle

# Define the input data model
class InputData(BaseModel):
    Cycle: float
    Preset_1: int
    Preset_2: int
    Temperature: float
    Pressure: float
    VibrationX: float
    VibrationY: float
    VibrationZ: float
    Frequency: float

app = FastAPI()

# Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.post("/predict")
def predict(data: InputData):
    # Feature engineering
    data_dict = data.dict()
    df = pd.DataFrame([data_dict])
    df['Temp_Pressure_Ratio'] = df['Temperature'] / df['Pressure']
    df['Vibration_Magnitude'] = (df['VibrationX']**2 + df['VibrationY']**2 + df['VibrationZ']**2)**0.5
    
    # Prediction
    prediction = model.predict(df)
    print(prediction)
    return {"prediction": prediction.tolist()}