import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Step 1: Load the cleaned dataset
df = pd.read_csv('clean_nsl_kdd.csv')

# Step 2: Convert categorical columns to numerical values using one-hot encoding
df = pd.get_dummies(df, columns=['protocol_type', 'service', 'flag'])

# Step 3: Prepare the features (X) and the target (y)
X = df.drop('label', axis=1)
y = df['label'].map({'normal': 1, 'anomaly': 0})

# ✅ Save the column names for use during inference in Flask
joblib.dump(X.columns.tolist(), 'model_columns.pkl')

# Step 4: Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 5: Split the data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 6: Initialize and tune the Random Forest model
rf = RandomForestClassifier(random_state=42)
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}

grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Step 7: Evaluate
y_pred = grid_search.best_estimator_.predict(X_test)
print("Best parameters found: ", grid_search.best_params_)
print(classification_report(y_test, y_pred))

# Step 8: Save everything
joblib.dump(grid_search.best_estimator_, 'random_forest_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("✅ Model, scaler, and column list saved successfully!")

# Step 9: Define function to get threat description and prevention based on prediction
def get_threat_description(prediction):
    if prediction == 0:  # Anomaly detected
        threat_type = "DDoS Attack"  # Example: you could add more conditions here
        prevention = "Apply rate limiting, use WAF, monitor traffic."
    else:  # Normal behavior
        threat_type = "Normal Activity"
        prevention = "No threat detected."
    return threat_type, prevention

# Save the function (or add it in Flask where predictions are made)
joblib.dump(get_threat_description, 'threat_description_function.pkl')
