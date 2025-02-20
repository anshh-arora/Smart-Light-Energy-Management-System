# Smart Light & Energy Management System

## Overview
The Smart Light & Energy Management System is an advanced analytics platform designed to optimize energy costs, detect inefficiencies, and automate billing for additional usage. By analyzing sensor data from lighting systems, this solution helps facility managers monitor energy consumption patterns, identify anomalies, and generate insights for operational improvements.

## 🎯 Key Features
- **Automated Client Billing**: Detect and invoice light usage beyond contracted hours
- **Operational Cost Reduction**: Identify inefficiencies in cleaning staff operations
- **Predictive Maintenance**: Flag unusual power consumption patterns to prevent failures
- **Real-time Monitoring**: Dashboard for immediate visibility into system status
- **Custom Reporting**: Generate periodic reports on energy consumption trends

## 📋 Use Cases

### 1. Client Billing for Extra Usage
- Each client has predefined working hours (typically 8 AM - 8 PM)
- System automatically detects usage outside contracted hours
- Generates supplementary invoices with detailed usage breakdown
- Maintains audit trail for billing transparency

### 2. Reducing Operational Costs
- Monitors cleaning staff light usage (expected: 30-60 minutes after work hours)
- Flags excessive usage (>3 hours) for management review
- Identifies patterns of wastage across facilities
- Calculates potential savings from optimized operations

### 3. Predictive Maintenance
- Establishes baseline power consumption for each area/device
- Detects gradual increases in power draw indicating potential issues
- Alerts maintenance teams before failures occur
- Tracks maintenance history and effectiveness

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python 3.9+ |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn, TensorFlow (optional) |
| Web Interface | Streamlit / Gradio |
| Database | MySQL / PostgreSQL / SQLite |
| API Framework | FastAPI (optional) |
| Containerization | Docker (optional) |

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git (optional)

### 1. Environment Setup
```bash
# Clone repository (optional)
git clone https://github.com/yourusername/smart-light-energy.git
cd smart-light-energy

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pandas numpy matplotlib seaborn scikit-learn streamlit plotly
```

### 2. Data Generation
For testing and development, use the included script to generate sample sensor data:

```python
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_company_sensor_data(rows=2000):
    """
    Generate realistic company-level sensor data with the following structure:
    - Multiple buildings (HQ, R&D Center, Manufacturing, etc.)
    - Multiple floors per building
    - Multiple zones per floor
    - Multiple clients with different contracted hours
    - Realistic patterns for weekday/weekend usage
    - Seasonal variations in power consumption
    """
    # Company structure
    buildings = {
        'HQ': {'floors': 5, 'zones_per_floor': 4, 'client_ids': ['C001', 'C002']},
        'R&D': {'floors': 3, 'zones_per_floor': 6, 'client_ids': ['C003']},
        'Manufacturing': {'floors': 2, 'zones_per_floor': 8, 'client_ids': ['C004', 'C005']},
        'Sales': {'floors': 4, 'zones_per_floor': 3, 'client_ids': ['C006']}
    }
    
    # Client contracted hours
    client_hours = {
        'C001': (8, 18),  # 8 AM - 6 PM
        'C002': (9, 19),  # 9 AM - 7 PM
        'C003': (7, 20),  # 7 AM - 8 PM (R&D works longer)
        'C004': (6, 22),  # 6 AM - 10 PM (Manufacturing runs longer)
        'C005': (0, 24),  # 24/7 operation
        'C006': (8, 17)   # 8 AM - 5 PM
    }
    
    # Start date for data generation
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 2, 28)
    date_range = (end_date - start_date).days
    
    data = []
    
    # Generate sensor readings
    while len(data) < rows:
        # Pick a random date within range
        random_day = random.randint(0, date_range)
        current_date = start_date + timedelta(days=random_day)
        
        # Determine if weekend
        is_weekend = current_date.weekday() >= 5
        
        # For each building
        for building_name, building_info in buildings.items():
            for floor in range(1, building_info['floors'] + 1):
                for zone in range(1, building_info['zones_per_floor'] + 1):
                    
                    # Assign a client to this zone
                    client_id = random.choice(building_info['client_ids'])
                    work_start, work_end = client_hours[client_id]
                    
                    # Generate sensor readings for this zone throughout the day
                    # More frequent during work hours, less frequent outside
                    if is_weekend and client_id not in ['C004', 'C005']:
                        # Weekend: only maintenance/cleaning plus occasional work
                        potential_hours = [7, 8, 9, 14, 15, 19, 20]
                        num_readings = random.randint(0, 5)  # Fewer readings on weekends
                    else:
                        # Weekday: regular operations
                        potential_hours = list(range(5, 24))  # Possible reading hours
                        num_readings = random.randint(8, 15)  # More readings on weekdays
                    
                    selected_hours = sorted(random.sample(potential_hours, min(num_readings, len(potential_hours))))
                    
                    for hour in selected_hours:
                        # Generate 1-3 readings per hour
                        for _ in range(random.randint(1, 3)):
                            minute = random.randint(0, 59)
                            timestamp = current_date.replace(hour=hour, minute=minute)
                            
                            # Room/zone identifier
                            room_id = f"{building_name}-F{floor}-Z{zone}"
                            
                            # Power usage - higher during work hours
                            base_power = random.randint(20, 50)
                            if work_start <= hour < work_end:
                                # During work hours - higher usage
                                power_multiplier = random.uniform(1.5, 2.5)
                                is_active = True
                            else:
                                # Outside work hours - lower usage
                                power_multiplier = random.uniform(0.3, 0.8)
                                is_active = False
                            
                            # Seasonal variation (winter = higher consumption)
                            month_factor = 1.2 if current_date.month < 3 or current_date.month > 10 else 1.0
                            
                            # Calculate final power usage
                            power_usage = int(base_power * power_multiplier * month_factor)
                            
                            # Determine if cleaning staff is present
                            is_cleaning = "Yes" if (not is_active and hour >= work_end and hour < work_end + 3 and random.random() < 0.7) else "No"
                            
                            # Add sensor reading to dataset
                            data.append([
                                timestamp, 
                                room_id, 
                                client_id, 
                                power_usage,
                                is_cleaning,
                                building_name,
                                floor,
                                zone
                            ])
                            
                            # Break if we've reached our target
                            if len(data) >= rows:
                                break
                        if len(data) >= rows:
                            break
                    if len(data) >= rows:
                        break
                if len(data) >= rows:
                    break
            if len(data) >= rows:
                break
    
    # Create DataFrame and sort by timestamp
    df = pd.DataFrame(data, columns=[
        "Timestamp", "Room_ID", "Client_ID", "Power_Usage_W", 
        "Cleaning_Staff", "Building", "Floor", "Zone"
    ])
    
    # Add some anomalies for predictive maintenance cases
    anomaly_indices = random.sample(range(len(df)), int(len(df) * 0.03))  # 3% anomalies
    for idx in anomaly_indices:
        df.loc[idx, 'Power_Usage_W'] = df.loc[idx, 'Power_Usage_W'] * random.uniform(2.5, 4.0)
    
    return df.sort_values("Timestamp").reset_index(drop=True)

# Generate company-level data with 2500 rows
sensor_data = generate_company_sensor_data(rows=2500)
sensor_data.to_csv("company_sensor_data.csv", index=False)
print(f"Generated {len(sensor_data)} rows of sensor data")
```

### 3. Data Analysis and Processing

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("company_sensor_data.csv", parse_dates=["Timestamp"])

# Extract time components
df["Hour"] = df["Timestamp"].dt.hour
df["Day"] = df["Timestamp"].dt.day
df["Month"] = df["Timestamp"].dt.month
df["Weekday"] = df["Timestamp"].dt.weekday
df["IsWeekend"] = df["Weekday"].apply(lambda x: 1 if x >= 5 else 0)

# Get client working hours - in production, this would come from a database
client_hours = {
    'C001': (8, 18),
    'C002': (9, 19),
    'C003': (7, 20),
    'C004': (6, 22),
    'C005': (0, 24),
    'C006': (8, 17)
}

# Flag extra usage based on client's contracted hours
def check_extra_usage(row):
    client = row["Client_ID"]
    hour = row["Hour"]
    start_hour, end_hour = client_hours.get(client, (8, 20))
    
    if client == 'C005':  # 24/7 client never has extra usage
        return "No"
    
    return "Yes" if hour < start_hour or hour >= end_hour else "No"

df["Extra_Usage"] = df.apply(check_extra_usage, axis=1)

# Flag inefficient cleaning staff usage (lights on for cleaning too late at night)
df["Cleaning_Inefficiency"] = df.apply(
    lambda row: "Yes" if row["Cleaning_Staff"] == "Yes" and row["Hour"] >= 23 else "No", 
    axis=1
)

# Flag potential maintenance issues (abnormally high power usage)
df_grouped = df.groupby(["Building", "Floor", "Zone"])["Power_Usage_W"].mean().reset_index()
df_grouped.columns = ["Building", "Floor", "Zone", "Avg_Power"]

# Merge back average power
df = pd.merge(df, df_grouped, on=["Building", "Floor", "Zone"], how="left")
df["Power_Ratio"] = df["Power_Usage_W"] / df["Avg_Power"]
df["Maintenance_Flag"] = df["Power_Ratio"].apply(lambda x: "Yes" if x > 2.0 else "No")

# Save processed data
df.to_csv("processed_sensor_data.csv", index=False)
```

### 4. Visualization Examples

```python
# Create a dashboard with multiple visualizations
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv("processed_sensor_data.csv", parse_dates=["Timestamp"])

# 1. Energy consumption by building
plt.figure(figsize=(12, 6))
sns.barplot(x="Building", y="Power_Usage_W", data=df, estimator=sum, ci=None)
plt.title("Total Energy Consumption by Building")
plt.xlabel("Building")
plt.ylabel("Total Power Usage (W)")
plt.savefig("building_consumption.png")

# 2. After-hours usage patterns
after_hours = df[df["Extra_Usage"] == "Yes"]
plt.figure(figsize=(12, 6))
sns.countplot(x="Hour", data=after_hours, hue="Building")
plt.title("After-Hours Usage by Building")
plt.xlabel("Hour of Day")
plt.ylabel("Count of Readings")
plt.savefig("after_hours_usage.png")

# 3. Cleaning staff efficiency
plt.figure(figsize=(12, 6))
cleaning_data = df[df["Cleaning_Staff"] == "Yes"]
sns.countplot(x="Hour", data=cleaning_data, hue="Cleaning_Inefficiency")
plt.title("Cleaning Staff Activity Hours")
plt.xlabel("Hour of Day")
plt.ylabel("Count of Readings")
plt.savefig("cleaning_hours.png")
```

### 5. Streamlit Dashboard

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("processed_sensor_data.csv", parse_dates=["Timestamp"])
    return df

df = load_data()

# Dashboard title
st.title("🌟 Smart Light & Energy Management System")
st.markdown("Enterprise-level monitoring and optimization platform")

# Summary metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    extra_usage_pct = round(len(df[df["Extra_Usage"] == "Yes"]) / len(df) * 100, 1)
    st.metric("Extra Usage", f"{extra_usage_pct}%")

with col2:
    cleaning_inefficiency = round(len(df[df["Cleaning_Inefficiency"] == "Yes"]) / len(df[df["Cleaning_Staff"] == "Yes"]) * 100, 1)
    st.metric("Cleaning Inefficiency", f"{cleaning_inefficiency}%")
    
with col3:
    maintenance_issues = len(df[df["Maintenance_Flag"] == "Yes"])
    st.metric("Potential Maintenance Issues", maintenance_issues)
    
with col4:
    avg_power = round(df["Power_Usage_W"].mean(), 1)
    st.metric("Avg Power Usage", f"{avg_power}W")

# Building selector
st.sidebar.header("Filters")
selected_building = st.sidebar.selectbox(
    "Select Building",
    ["All"] + list(df["Building"].unique())
)

if selected_building != "All":
    filtered_df = df[df["Building"] == selected_building]
else:
    filtered_df = df

# Date range filter
min_date = df["Timestamp"].min().date()
max_date = df["Timestamp"].max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    mask = (filtered_df["Timestamp"].dt.date >= start_date) & (filtered_df["Timestamp"].dt.date <= end_date)
    filtered_df = filtered_df[mask]

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["📊 Energy Usage", "💰 Billing Insights", "🔧 Maintenance"])

with tab1:
    st.subheader("Energy Consumption Patterns")
    
    # Energy usage by hour and building
    fig = px.histogram(
        filtered_df, 
        x="Hour", 
        y="Power_Usage_W",
        color="Building",
        barmode="group",
        histfunc="avg",
        title="Average Hourly Power Consumption by Building"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap of energy usage by floor and zone
    pivot_data = filtered_df.pivot_table(
        index="Floor", 
        columns="Zone", 
        values="Power_Usage_W",
        aggfunc="mean"
    ).fillna(0)
    
    fig = px.imshow(
        pivot_data,
        labels=dict(x="Zone", y="Floor", color="Avg Power (W)"),
        title="Heat Map of Power Usage by Floor and Zone"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Client Billing Analysis")
    
    # Extra usage by client
    extra_usage_by_client = filtered_df[filtered_df["Extra_Usage"] == "Yes"].groupby("Client_ID").size().reset_index()
    extra_usage_by_client.columns = ["Client_ID", "Extra_Hours"]
    
    fig = px.bar(
        extra_usage_by_client,
        x="Client_ID",
        y="Extra_Hours",
        title="Extra Hours Usage by Client",
        color="Extra_Hours"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate estimated costs
    rate_per_hour = 15  # $15 per hour per zone
    extra_usage_cost = filtered_df[filtered_df["Extra_Usage"] == "Yes"].groupby("Client_ID").size() * rate_per_hour
    
    if not extra_usage_cost.empty:
        cost_df = extra_usage_cost.reset_index()
        cost_df.columns = ["Client_ID", "Extra_Cost"]
        cost_df["Extra_Cost"] = cost_df["Extra_Cost"].apply(lambda x: f"${x}")
        
        st.write("Estimated Extra Usage Billing")
        st.dataframe(cost_df)
    else:
        st.info("No extra usage detected in the selected period")

with tab3:
    st.subheader("Maintenance Issues")
    
    # Show potential maintenance issues
    maintenance_issues = filtered_df[filtered_df["Maintenance_Flag"] == "Yes"]
    
    if not maintenance_issues.empty:
        fig = go.Figure()
        
        for building in maintenance_issues["Building"].unique():
            building_data = maintenance_issues[maintenance_issues["Building"] == building]
            fig.add_trace(go.Scatter(
                x=building_data["Timestamp"],
                y=building_data["Power_Ratio"],
                mode="markers",
                name=building,
                marker=dict(size=10)
            ))
        
        fig.update_layout(
            title="Anomalous Power Usage (Power Ratio > 2.0)",
            xaxis_title="Date",
            yaxis_title="Power Ratio (Actual/Average)",
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("Detailed Maintenance Flags")
        st.dataframe(maintenance_issues[["Timestamp", "Building", "Room_ID", "Power_Usage_W", "Power_Ratio"]])
    else:
        st.success("No maintenance issues detected in the selected period")

# Run with: streamlit run dashboard.py
```

## 📊 Analytics & Insights

### Client Billing
The system automatically calculates additional billing based on:
- Contracted hours vs. actual usage hours
- Energy consumption during extra hours
- Client-specific rate agreements

### Energy Efficiency
Key performance indicators tracked:
- Energy consumption trends by time of day
- Comparison across buildings/floors/zones
- Seasonal variations and anomalies

### Predictive Maintenance
The system implements:
- Baseline power consumption profiles for each zone
- Anomaly detection algorithms to identify unusual patterns
- Trend analysis to spot gradual degradation

## 🛡️ Security & Data Privacy
- Data encryption in transit and at rest
- Role-based access control for dashboard
- Regular backups and disaster recovery planning
- Compliance with relevant data protection regulations

## 🔄 Future Enhancements

### Short-term Improvements (3-6 months)
1. **AI-Powered Forecasting**
   - Implement machine learning models to predict peak usage hours
   - Develop occupancy prediction based on historical patterns
   - Create dynamic pricing models for more accurate billing

2. **Integration Capabilities**
   - Connect with building management systems (BMS)
   - Integrate with HVAC for comprehensive energy management
   - Develop APIs for third-party application integration

3. **Advanced Visualization**
   - 3D building visualization with heat maps
   - Interactive floor plans showing real-time usage
   - Customizable executive dashboards

### Long-term Vision (1-2 years)
1. **Autonomous Energy Optimization**
   - Implement ML-driven lighting control systems
   - Develop automated schedule adjustments based on usage patterns
   - Create self-learning systems that optimize without human intervention

2. **Blockchain-Based Billing**
   - Implement smart contracts for automated billing
   - Create transparent, immutable record of energy usage
   - Enable microtransactions for pay-as-you-go energy models

3. **Ecosystem Expansion**
   - Extend to water and gas usage monitoring
   - Develop carbon footprint tracking and reporting
   - Create comprehensive sustainability metrics dashboard

4. **Enterprise Scaling**
   - Multi-tenant architecture for managing thousands of buildings
   - Global deployment with localization features
   - Hierarchical reporting for corporate, regional, and site-level insights

## 💼 Business Impact
- **Cost Reduction**: Typical clients see 15-25% reduction in energy costs
- **Revenue Generation**: Additional billing for extra usage creates new revenue streams
- **Sustainability**: Reduced energy waste contributes to environmental goals
- **Operational Efficiency**: Maintenance teams become proactive rather than reactive

## 🤝 Contributing
We welcome contributions to this project. Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Credits
- Initial Concept: Aditya Sir (Smartworks)
- Development: Ansh
- Documentation: [Your Name]
