import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import urllib
from sqlalchemy import create_engine

server_name = '.' 
database_name = 'clinic_db'

params = urllib.parse.quote_plus(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes;TrustServerCertificate=yes;')
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
print("تم الاتصال بـ SQL Server بنجاح!")

df_depts = pd.DataFrame({
    'Dept_ID': ['D01', 'D02', 'D03', 'D04', 'D05'],
    'Dept_Name': ['Cardiology', 'Pediatrics', 'Dentistry', 'Orthopedics', 'Ophthalmology']
})

np.random.seed(42)
df_doctors = pd.DataFrame({
    'Doctor_ID': [f'DR-{i:03d}' for i in range(1, 21)],
    'Dept_ID': np.random.choice(df_depts['Dept_ID'], 20),
    'Experience_Years': np.random.randint(2, 25, 20),
    'Avg_Rating': np.round(np.random.uniform(3.5, 5.0, 20), 1)
})

df_patients = pd.DataFrame({
    'Patient_ID': [f'PT-{i:05d}' for i in range(1, 1001)],
    'Gender': np.random.choice(['Male', 'Female'], 1000),
    'Age': np.random.randint(1, 90, 1000),
    'Blood_Type': np.random.choice(['A+', 'O+', 'B+', 'AB+', 'O-', 'A-'], 1000, p=[0.3, 0.4, 0.1, 0.05, 0.1, 0.05])
})

num_appointments = 5000
start_date = datetime(2025, 1, 1)

df_appointments = pd.DataFrame({
    'Appt_ID': [f'AP-{i:06d}' for i in range(1, num_appointments + 1)],
    'Patient_ID': np.random.choice(df_patients['Patient_ID'], num_appointments),
    'Doctor_ID': np.random.choice(df_doctors['Doctor_ID'], num_appointments),
    'Appt_Date': [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(num_appointments)],
    'Status': np.random.choice(['Show', 'No-Show', 'Canceled'], num_appointments, p=[0.75, 0.15, 0.10]),
})

df_appointments['Wait_Time_Min'] = np.where(
    df_appointments['Status'] == 'Show', 
    np.random.randint(5, 60, num_appointments), 
    0
)

print("Loading tables to the database...")

df_depts.to_sql('Departments_Dim', con=engine, if_exists='replace', index=False)
df_doctors.to_sql('Doctors_Dim', con=engine, if_exists='replace', index=False)
df_patients.to_sql('Patients_Dim', con=engine, if_exists='replace', index=False)
df_appointments.to_sql('Appointments_Fact', con=engine, if_exists='replace', index=False)

print("All tables loaded successfully!")