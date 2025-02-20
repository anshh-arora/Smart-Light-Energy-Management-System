import smtplib
import os
import pandas as pd
from email.message import EmailMessage

# Load client & worker data
clients_df = pd.read_csv("data/overused_clients.csv")
workers_df = pd.read_csv("data/overused_workers.csv")

# Email sender details
EMAIL_ADDRESS = "ansh1529arora@gmail.com"
EMAIL_PASSWORD = "ansh1529"

# Create directories for storing emails
os.makedirs("sent_mails/clients", exist_ok=True)
os.makedirs("sent_mails/workers", exist_ok=True)

def save_email(to_email, subject, body, folder):
    """ Function to save emails as text files instead of sending """
    file_path = f"{folder}/{to_email}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"Subject: {subject}\n")
        file.write(f"To: {to_email}\n")
        file.write(f"\n{body}")

def send_email(to_email, subject, body, folder):
    """ Function to send emails (currently storing instead) """
    save_email(to_email, subject, body, folder)  # Store emails locally
    # Uncomment the below lines to actually send emails
    # msg = EmailMessage()
    # msg["Subject"] = subject
    # msg["From"] = EMAIL_ADDRESS
    # msg["To"] = to_email
    # msg.set_content(body)
    # with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    #     smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    #     smtp.send_message(msg)

# 🔹 Send Billing Emails to Clients
for _, row in clients_df.iterrows():
    client_name = row["Name"]
    client_email = row["Email"]
    allowed_hours = row["Allowed_Usage_Hours"]
    actual_hours = row["Actual_Usage_Hours"]
    extra_hours = actual_hours - allowed_hours

    if extra_hours > 0:  # Only send email if extra hours are used
        extra_cost = extra_hours * 10  # ₹10 per unit

        email_body = f"""
        Dear {client_name},

        You have exceeded your allowed energy usage by {extra_hours:.2f} hours.
        As per the agreement, you are required to pay ₹{extra_cost:.2f} for the extra usage.

        Please make the necessary payment at your earliest convenience.

        Regards,
        Energy Monitoring Team
        """

        send_email(client_email, "Billing Alert: Extra Energy Usage", email_body, "sent_mails/clients")

# 🔹 Send Warning Emails to Workers
for _, row in workers_df.iterrows():
    worker_name = row["Name"]
    worker_email = row["Email"]
    allowed_hours = row["Allowed_Usage_Hours"]
    actual_hours = row["Actual_Usage_Hours"]
    extra_hours = actual_hours - allowed_hours

    if extra_hours > 0:  # Only send email if extra hours are used
        email_body = f"""
        Dear {worker_name},

        You have exceeded the allocated time by {extra_hours:.2f} hours.
        If this continues, a fine will be charged for every extra hour used.

        Please ensure compliance with the allotted time.

        Regards,
        Operations Team
        """

        send_email(worker_email, "Warning: Excessive Usage", email_body, "sent_mails/workers")

print("✅ Emails stored successfully!")
