import pandas as pd
import json

# Function to load data from JSON file and save it to Excel
def create_excel_from_json(json_file, excel_file):
    # Load data from JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Create a DataFrame from the loaded data
    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file
    df.to_excel(excel_file, index=False)

    print(f"Data successfully written to {excel_file}")

if __name__ == '__main__':
    json_file = 'bros.json'  # Input JSON file
    excel_file = 'air_conditioners.xlsx'  # Output Excel file
    create_excel_from_json(json_file, excel_file)
