# app.py

import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the trained model and feature list
with open('model_and_features.pkl', 'rb') as f:
    save_object = pickle.load(f)

model = save_object['model']
feature_list = save_object['features']

st.title("🛡️ Smart Insurance Premium Predictor")

# User input collection
def user_input():
    st.header("Enter Customer Details:")
    inputs = {}
    
    # Collect inputs dynamically based on feature names
    for feature in feature_list:
        if feature == "Gender":
            inputs[feature] = st.selectbox("Gender", ["Male", "Female"])
        elif feature == "Marital Status":
            inputs[feature] = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
        elif feature == "Education Level":
            inputs[feature] = st.selectbox("Education Level", ["High School", "Bachelor's", "Master's", "PhD", "Other"])
        elif feature == "Occupation":
            inputs[feature] = st.selectbox("Occupation", ["Engineer", "Doctor", "Teacher", "Lawyer", "Other"])
        elif feature == "Location":
            inputs[feature] = st.selectbox("Location", ["Urban", "Suburban", "Rural"])
        elif feature == "Policy Type":
            inputs[feature] = st.selectbox("Policy Type", ["Comprehensive", "Third-Party", "Other"])
        elif feature == "Smoking Status":
            inputs[feature] = st.selectbox("Smoking Status", ["Yes", "No"])
        elif feature == "Exercise Frequency":
            inputs[feature] = st.selectbox("Exercise Frequency", ["Daily", "Weekly", "Rarely", "Never"])
        elif feature == "Property Type":
            inputs[feature] = st.selectbox("Property Type", ["Apartment", "House", "Condo", "Other"])
        elif feature == "Start_Date":
            inputs[feature] = st.date_input("Policy Start Date")
        elif feature in [ "Annual Income", "Health Score", 
                        "Credit Score", "Insurance Duration"]:
            inputs[feature] = st.number_input(f"{feature}", value=0.0)
        elif feature in ["Age","Vehicle Age","Number of Dependents","Previous Claims"]:
            inputs[feature] = st.number_input(f"{feature}",value=18,step=1)
        elif feature == "Customer Feedback":
            inputs[feature] = st.text_input("Customer Feedback", value="Good")
        else:
            inputs[feature] = st.text_input(feature, value="Unknown")
    
    return pd.DataFrame([inputs])

# Take input from user
input_df = user_input()

# Predict when button clicked
if st.button("Predict Premium"):
    try:
        # Predict
        prediction = model.predict(input_df)
        premium_amount = np.expm1(prediction)[0]  # Reversing log1p
        
        st.success(f"💰 Predicted Premium Amount: ₹ {premium_amount:.2f} ")
    except Exception as e:
        st.error(f"Something went wrong: {e}")