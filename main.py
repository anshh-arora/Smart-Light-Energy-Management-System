import joblib
import pandas as pd

# Load trained model using joblib
model = joblib.load("best_model.pkl")

# Load client & worker data
clients_df = pd.read_csv("data/overused_clients.csv")  # Ensure it has 'Actual_Usage_Hours'
workers_df = pd.read_csv("data/overused_workers.csv")  # Ensure it has 'Actual_Usage_Hours'

# Function to predict maintenance cost
def predict_maintenance_cost(usage_hours):
    """Predicts maintenance cost based on actual usage hours"""
    data = pd.DataFrame({"Actual_Usage_Hours": [usage_hours]})
    prediction = model.predict(data)[0]  # Ensure `model` is trained and has `.predict()`
    return round(prediction, 2)

# Apply prediction to Clients
clients_df["Predicted_Maintenance_Cost"] = clients_df["Actual_Usage_Hours"].apply(predict_maintenance_cost)

# Apply prediction to Workers
workers_df["Predicted_Maintenance_Cost"] = workers_df["Actual_Usage_Hours"].apply(predict_maintenance_cost)

# Save updated CSVs
clients_df.to_csv("data/client_maintenance_cost.csv", index=False)
workers_df.to_csv("data/worker_maintenance_cost.csv", index=False)

print("✅ Maintenance cost predictions saved for Clients & Workers!")
