# -*- coding: utf-8 -*-
"""age_gender_analysis.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Pw8XCSPUDyLC4SkD-8LFQdIa1TRdSN-D
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer
import pickle

# Load the datasets
p_bmx = pd.read_sas('P_BMX.xpt')
p_bpxo = pd.read_sas('P_BPXO.xpt')
p_demo = pd.read_sas('P_DEMO.xpt')
p_hdl = pd.read_sas('P_HDL.xpt')
p_hscrp = pd.read_sas('P_HSCRP.xpt')
p_ucflow = pd.read_sas('P_UCFLOW.xpt')
p_ucm = pd.read_sas('P_UCM.xpt')
p_ucpreg = pd.read_sas('P_UCPREG.xpt')

# Check the columns of each dataset
print(p_bmx.columns)
print(p_bpxo.columns)
print(p_demo.columns)
print(p_hdl.columns)
print(p_hscrp.columns)
print(p_ucflow.columns)
print(p_ucm.columns)
print(p_ucpreg.columns)

# Merge datasets on the common column 'SEQN'
merged_data = pd.merge(p_bmx, p_bpxo, on="SEQN", how="left")
merged_data = pd.merge(merged_data, p_demo, on="SEQN", how="left")
merged_data = pd.merge(merged_data, p_hdl, on="SEQN", how="left")
merged_data = pd.merge(merged_data, p_hscrp, on="SEQN", how="left")
merged_data = pd.merge(merged_data, p_ucflow, on="SEQN", how="left")
merged_data = pd.merge(merged_data, p_ucm, on="SEQN", how="left")
merged_data = pd.merge(merged_data, p_ucpreg, on="SEQN", how="left")

# Check if the HDL column is in the merged data
print(merged_data.columns)

# Handle missing values with SimpleImputer
# Impute numerical columns with the mean
numerical_cols = merged_data.select_dtypes(include=['float64', 'int64']).columns
numerical_imputer = SimpleImputer(strategy='mean')
merged_data[numerical_cols] = numerical_imputer.fit_transform(merged_data[numerical_cols])

# Impute categorical columns with the most frequent value (mode)
categorical_cols = merged_data.select_dtypes(include=['object']).columns
categorical_imputer = SimpleImputer(strategy='most_frequent')
merged_data[categorical_cols] = categorical_imputer.fit_transform(merged_data[categorical_cols])

# Define the target column and selected features
# Example: assuming 'HTN' is the target column for hypertension classification
target_column = 'HTN'  # Replace this with your actual target column name
selected_features = ['BMXWT', 'BMXHT', 'BPXOSY1', 'BPXODI1', 'HDL', 'LBXHSCRP', 'URXUCM']  # Replace with relevant columns

# Ensure the target column exists in the merged data
if target_column not in merged_data.columns:
    raise ValueError(f"{target_column} not found in merged data")

# Select features and target
X = merged_data[selected_features]
y = merged_data[target_column]

# Ensure y is binary (1 for Hypertension, 0 for no hypertension)
y_binary = y.apply(lambda x: 1 if x > 0 else 0)  # Adjust based on your target definition

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_binary, test_size=0.2, random_state=42)

# Train a Logistic Regression model
lr_model = LogisticRegression()
lr_model.fit(X_train, y_train)

# Make predictions
y_pred_lr = lr_model.predict(X_test)

# Evaluate the model
accuracy_lr = accuracy_score(y_test, y_pred_lr)
print(f'Logistic Regression - Accuracy: {accuracy_lr}')
print(classification_report(y_test, y_pred_lr))

# Save the trained model
with open('logistic_regression_model.pkl', 'wb') as model_file:
    pickle.dump(lr_model, model_file)

# Save the model metrics
model_metrics = {
    'accuracy': accuracy_lr
}
metrics_df = pd.DataFrame([model_metrics])
metrics_df.to_csv('model_metrics.csv', index=False)

print("Model and metrics saved successfully!")