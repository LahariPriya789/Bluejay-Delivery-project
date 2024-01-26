import pandas as pd

# Reading the CSV file into a pandas DataFrame
file_path = r'D:\$PYTHON\Assignment_Timecard.csv'
df = pd.read_csv(file_path)

# Taking only active employees
active_employees = df[df['Position Status'] == 'Active']

# Parse date and time columns
active_employees['Time'] = pd.to_datetime(active_employees['Time'], errors='coerce', format='%m/%d/%Y %I:%M %p')
active_employees['Time Out'] = pd.to_datetime(active_employees['Time Out'], errors='coerce', format='%m/%d/%Y %I:%M %p')

# Convert 'Timecard Hours (as Time)' column to numeric
active_employees['Timecard Hours (as Time)'] = pd.to_numeric(active_employees['Timecard Hours (as Time)'], errors='coerce')

# Drop Unnamed columns
active_employees = active_employees.drop(columns=['Unnamed: 9', 'Unnamed: 10'], errors='ignore')

# Initialize variables
consecutive_days_threshold = 7
time_between_shifts_min = 1
time_between_shifts_max = 10
max_hours_single_shift = 14

# Group by employee name
grouped_by_employee = active_employees.groupby('Employee Name')

# Analyze and print results
for employee_name, employee_data in grouped_by_employee:
    shifts = employee_data.sort_values('Time')

    # Check for 7 consecutive days
    consecutive_days_count = 1
    for i in range(1, len(shifts)):
        if (shifts.iloc[i]['Time'] - shifts.iloc[i - 1]['Time']).days == 1:
            consecutive_days_count += 1
        else:
            consecutive_days_count = 1

        if consecutive_days_count == consecutive_days_threshold:
            print(f"{employee_name} has worked for {consecutive_days_threshold} consecutive days in positions: {employee_data['Position ID'].unique()}")

    # Check for time between shifts and hours in a single shift
    for i in range(1, len(shifts)):
        time_between_shifts = (shifts.iloc[i]['Time'] - shifts.iloc[i - 1]['Time Out']).total_seconds() / 3600
        hours_in_single_shift = shifts.iloc[i]['Timecard Hours (as Time)']

        if time_between_shifts > time_between_shifts_min and time_between_shifts < time_between_shifts_max:
            print(f"{employee_name} has less than 10 hours between shifts ({time_between_shifts:.2f} hours) in positions: {employee_data['Position ID'].unique()}")

        if hours_in_single_shift > max_hours_single_shift:
            print(f"{employee_name} has worked for more than 14 hours in a single shift ({hours_in_single_shift:.2f} hours) in positions: {employee_data['Position ID'].unique()}")
