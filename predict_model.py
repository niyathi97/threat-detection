import pandas as pd
import joblib  # Importing joblib to load the saved model and scaler

# Step 1: Load the saved model and scaler
model = joblib.load('random_forest_model.pkl')  # Load the trained model
scaler = joblib.load('scaler.pkl')  # Load the scaler used during training

# Step 2: Load the new data (make sure the file path is correct)
new_data = pd.read_csv('clean_nsl_kdd.csv')  # Replace 'clean_nsl_kdd.csv' with your actual data file

# Step 3: Preprocess the new data (same steps as during training)
new_data = pd.get_dummies(new_data, columns=['protocol_type', 'service', 'flag'])  # One-hot encoding

# Step 4: Separate features (X) and target (y)
X_new = new_data.drop('label', axis=1)  # Features (drop the 'label' column)

# Step 5: Standardize the new data using the same scaler
X_new_scaled = scaler.transform(X_new)  # Use the same scaler used during training

# Step 6: Predict using the trained model
y_pred = model.predict(X_new_scaled)

# Step 7: Output the predictions
# If you want to print out the predictions, or save to a CSV file, you can do so here
new_data['predictions'] = y_pred  # Add predictions to the dataframe
print(new_data[['predictions']].head())  # Print first few predictions

# Optionally, save the results to a new CSV file
new_data.to_csv('predicted_results.csv', index=False)
