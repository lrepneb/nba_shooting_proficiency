import pandas as pd
import os

def count_contract_years(file_path, output_path):
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Identify columns that represent years (filtering those that look like year ranges)
    year_columns = [col for col in df.columns if col.replace("-", "").isdigit()]
    
    # Create a new column 'years' counting the number of non-empty year columns per row
    df['years'] = df[year_columns].apply(lambda row: row.notna().sum(), axis=1)
    
    # Drop the '-additional' column if it exists
    df = df.drop(columns=[col for col in df.columns if '-additional' in col], errors='ignore')

    df.replace({'\$': ''}, regex=True, inplace=True)
    
    # Save the updated dataframe
    df.to_csv(output_path, index=False)
    print(f"Updated dataset saved to {output_path}")

# Example usage
if __name__ == "__main__":
    input_file = "nba_player_salary.csv"  # Input file path
    output_file = input_file  # Output file path
    count_contract_years(input_file, output_file)
