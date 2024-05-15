import os
import pandas as pd
from datetime import datetime

# Step 1: Create a folder named 'attendance folder'
attendance_folder = 'attendance folder'
os.makedirs(attendance_folder, exist_ok=True)

# Step 2: Define the data for the Excel sheet
data = {
    'NAME': [],
    'REGESTRATION NUMBER': [],
    'ATTENDANCE': []
}

# Step 3: Get the current date for the Excel sheet name
current_date = datetime.now().strftime('%Y-%m-%d')
excel_file_name = f"{current_date}.xlsx"
excel_file_path = os.path.join(attendance_folder, excel_file_name)

# Step 4: Create a DataFrame from the data
df = pd.DataFrame(data)

# Step 5: Write the data to the Excel file
try:
    df.to_excel(excel_file_path, index=False, sheet_name='Attendance', startrow=1, header=True)
    print(f"Excel file '{excel_file_name}' created successfully in '{attendance_folder}' folder.")
except Exception as e:
    print(f"An error occurred while writing data to the Excel file: {e}")