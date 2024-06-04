import streamlit as st
import requests
import json

st.title('Model Prediction')

def categorize_failure(data, model_result):
    error = 'No Failure'
    temperature_error = False
    temperature_threshold = 79
    pressure_error = False
    pressure_threshold = 98
    vibration_error = False
    vibration_x_threshold = 88
    vibration_y_threshold = 99
    vibration_z_threshold = 89
    frequency_error = False
    frequency_threshold = 89

    if model_result==True:
    
        if data['Temperature'] > temperature_threshold:
            temperature_error = True
        if data['Pressure'] > pressure_threshold:
            pressure_error = True
        if data['VibrationX'] > vibration_x_threshold or data['VibrationY'] > vibration_y_threshold or data['VibrationZ'] > vibration_z_threshold:
            vibration_error = True
        if data['Frequency'] < frequency_threshold:
            frequency_error = True
    

    if any([temperature_error, pressure_error, vibration_error, frequency_error]):
        error = ''
        if temperature_error:
            error += 'Temperature '
        if pressure_error:
            error += 'Pressure '
        if vibration_error:
            error += 'Vibration '
        if frequency_error:
            error += 'Frequency '
        error += 'Failure'
    
    return error

# Input features

Cycle = st.number_input('Enter Cycle:', step=10)
Preset_1 = st.number_input('Enter Preset_1:', min_value=1, max_value=3, step=1)
Preset_2 = st.number_input('Enter Preset_2:', min_value=1, max_value=8, step=1)
Temperature = st.number_input('Enter Temperature:', step=10)
Pressure = st.number_input('Enter Pressure:', step=10)
VibrationX = st.number_input('Enter VibrationX:', step=10)
VibrationY = st.number_input('Enter VibrationY:', step=10)
VibrationZ = st.number_input('Enter VibrationZ:', step=10)
Frequency = st.number_input('Enter Frequency:', step=10)

if st.button('Predict'):
    data = {
        'Temperature': Temperature,
        'Pressure': Pressure,
        'VibrationX': VibrationX,
        'VibrationY': VibrationY,
        'VibrationZ': VibrationZ,
        'Frequency': Frequency,
        'Preset_1': Preset_1,
        'Preset_2': Preset_2,
        'Cycle': Cycle
    }
    response = requests.post('http://fastapi:8000/predict', data=json.dumps(data))
    prediction = response.json()['prediction'][0]

    st.markdown("---")
    error_message = categorize_failure(data, prediction)
    st.write('Prediction: ', prediction)
    st.write('Error Message: ', error_message)