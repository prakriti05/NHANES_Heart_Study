# -*- coding: utf-8 -*-
"""model_comparision.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Pw8XCSPUDyLC4SkD-8LFQdIa1TRdSN-D
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Load the datasets
bmx_data = pd.read_sas('P_BMX.xpt')
bp_data = pd.read_sas('P_BPXO.xpt')
demo_data = pd.read_sas('P_DEMO.xpt')
hdl_data = pd.read_sas('P_HDL.xpt')
hscrp_data = pd.read_sas('P_HSCRP.xpt')
ucm_data = pd.read_sas('P_UCM.xpt')

# Merge all datasets on SEQN (the unique respondent identifier)
merged_data = demo_data.merge(bmx_data, on='SEQN', how='inner')  # merge with demographics
merged_data = merged_data.merge(bp_data, on='SEQN', how='inner')  # merge with blood pressure data
merged_data = merged_data.merge(hdl_data, on='SEQN', how='inner')  # merge with HDL cholesterol data
merged_data = merged_data.merge(hscrp_data, on='SEQN', how='inner')  # merge with HSCRP data
merged_data = merged_data.merge(ucm_data, on='SEQN', how='inner')  # merge with urine chromium data

# Select features and target variable (assuming Hypertension status is the target)
required_columns = ['BMXWT', 'BMXHT', 'BPXDI1', 'BPXSY1', 'BPXSY2', 'BPXSY3', 'BPXSY4', 'HDL', 'HSCRP', 'URXUCM']

# Check if the required columns exist in the merged data
existing_columns = [col for col in required_columns if col in merged_data.columns]

# If all required columns are present, proceed with feature selection
if len(existing_columns) == len(required_columns):
    X = merged_data[existing_columns]
    y = merged_data['BPXDI1']  # Target: Hypertension status (0 = no, 1 = yes)
else:
    print("The following columns are missing:", list(set(required_columns) - set(existing_columns)))

# Print the column names of the merged dataframe to inspect
print("Columns available in merged data:")
print(merged_data.columns)

# Adjusted column names based on the columns available in the merged data
X = merged_data[['BMXWT', 'BMXHT', 'BPXODI1', 'BPXOSY1', 'BPXOSY2', 'BPXOSY3', 'LBXHSCRP', 'URXUCM']]

# Assuming you are predicting hypertension status (0 = no, 1 = yes), use a relevant target
y = merged_data['BPXODI1']  # Replace with the appropriate column for the target (e.g., hypertension status)

# Ensure no missing values are in X or y
X = X.dropna()
y = y[X.index]

# Check for missing values
print(X.isnull().sum())

# Drop rows with missing values (or you can fill them using imputation methods)
X = X.dropna()
y = y[X.index]

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

from sklearn.metrics import accuracy_score, precision_score, classification_report

# Train a Logistic Regression model
lr_model = LogisticRegression(max_iter=10000)  # Added max_iter to avoid convergence issues
lr_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred_lr = lr_model.predict(X_test)

# Evaluate the model
accuracy_lr = accuracy_score(y_test, y_pred_lr)

# Since it's multiclass, specify the average method
precision_lr = precision_score(y_test, y_pred_lr, average='weighted')

print(f'Logistic Regression - Accuracy: {accuracy_lr}, Precision: {precision_lr}')
print(classification_report(y_test, y_pred_lr))

# Save the trained model
joblib.dump(lr_model, 'logistic_regression_model.pkl')

# Save the metrics to a CSV file
metrics = {
    'Accuracy': accuracy_lr,
    'Precision': precision_lr
}
metrics_df = pd.DataFrame(metrics, index=[0])
metrics_df.to_csv('model_metrics.csv', index=False)

# Remove rows with any missing values in the features or target
X_clean = X.dropna()
y_clean = y[X_clean.index]  # Make sure y matches the cleaned X

# Split the cleaned data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_clean, y_clean, test_size=0.2, random_state=42)

# Now train the logistic regression model
lr_model = LogisticRegression()
lr_model.fit(X_train, y_train)

# Make predictions
y_pred_lr = lr_model.predict(X_test)

# Evaluate the model
accuracy_lr = accuracy_score(y_test, y_pred_lr)
precision_lr = precision_score(y_test, y_pred_lr)

print(f'Logistic Regression - Accuracy: {accuracy_lr}, Precision: {precision_lr}')
print(classification_report(y_test, y_pred_lr))

# Plot confusion matrix for binary classification
conf_matrix_lr = confusion_matrix(y_test, y_pred_lr)
disp = ConfusionMatrixDisplay(conf_matrix_lr, display_labels=['No Hypertension', 'Hypertension'])
disp.plot(cmap=plt.cm.Blues)
plt.title("Logistic Regression - Confusion Matrix")
plt.show()

from sklearn.impute import SimpleImputer

# Impute missing values with the mean of each column
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

# Train the logistic regression model
lr_model = LogisticRegression()
lr_model.fit(X_train, y_train)

# Make predictions
y_pred_lr = lr_model.predict(X_test)

# Evaluate the model
accuracy_lr = accuracy_score(y_test, y_pred_lr)
precision_lr = precision_score(y_test, y_pred_lr)

print(f'Logistic Regression - Accuracy: {accuracy_lr}, Precision: {precision_lr}')
print(classification_report(y_test, y_pred_lr))

# Plot confusion matrix for binary classification
conf_matrix_lr = confusion_matrix(y_test, y_pred_lr)
disp = ConfusionMatrixDisplay(conf_matrix_lr, display_labels=['No Hypertension', 'Hypertension'])
disp.plot(cmap=plt.cm.Blues)
plt.title("Logistic Regression - Confusion Matrix")
plt.show()