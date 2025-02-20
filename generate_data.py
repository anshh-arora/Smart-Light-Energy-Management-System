import os
import pandas as pd
import random
from faker import Faker

# Initialize Faker for generating fake names and emails
fake = Faker()

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Parameters
NUM_CLIENTS = 700
NUM_WORKERS = 300
TOTAL_RECORDS = NUM_CLIENTS + NUM_WORKERS

# Create empty lists for storing data
data = []

# Generate Client Data
for _ in range(NUM_CLIENTS):
    client_id = fake.uuid4()[:8]  # Unique ID
    name = fake.name()
    email = fake.email()
    allowed_hours = 12  # 8 AM - 8 PM (12 hours)
    actual_hours = round(random.uniform(10, 15), 2)  # Simulate overuse (sometimes)

    # Append client data
    data.append([client_id, name, email, "Client", allowed_hours, actual_hours])

# Generate Worker Data
for _ in range(NUM_WORKERS):
    worker_id = fake.uuid4()[:8]  # Unique ID
    name = fake.name()
    email = fake.email()
    allowed_time = 0.5  # 30 minutes allowed
    actual_time = round(random.uniform(0.3, 3), 2)  # Simulate overuse (up to 3 hours!)

    # Append worker data
    data.append([worker_id, name, email, "Worker", allowed_time, actual_time])

# Convert to DataFrame
columns = ["ID", "Name", "Email", "Role", "Allowed_Usage_Hours", "Actual_Usage_Hours"]
df = pd.DataFrame(data, columns=columns)

# Save to CSV
csv_path = "data/sensor_data.csv"
df.to_csv(csv_path, index=False)

print(f"✅ Data generated successfully: {csv_path}")
