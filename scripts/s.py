import pandas as pd

def merge_nba_datasets(general_stats_path, salary_path, shooting_stats_path, output_path):
    # Load datasets
    df_general = pd.read_csv(general_stats_path)
    df_salary = pd.read_csv(salary_path)
    df_shooting = pd.read_csv(shooting_stats_path)
    
    # Standardize column names for merging
    df_general.rename(columns={"Player": "player", "Age": "age"}, inplace=True)
    df_salary.rename(columns={"Player": "player", "Rk": "salary_rank"}, inplace=True)
    
    # Rename salary columns to avoid confusion
    salary_cols = {col: f"salary_{col.replace('-', '_')}" for col in df_salary.columns if col.startswith("20") or col == "Guaranteed" or col == "years"}
    df_salary.rename(columns=salary_cols, inplace=True)
    
    # Merge datasets
    df_merged = df_general.merge(df_salary, on="player", how="outer").merge(df_shooting, on="player", how="outer")
    
    # Remove duplicate columns
    df_merged.drop(columns=[col for col in ["Team_x", "Team_y", "team"] if col in df_merged.columns], inplace=True)
    df_merged.drop(columns=[col for col in ["Age", "age"] if col in df_merged.columns and col != "age"], inplace=True)
    
    # Save merged dataset
    df_merged.to_csv(output_path, index=False)
    print(f"Merged dataset saved to {output_path}")

# Example usage
if __name__ == "__main__":
    general_stats_file = "nba_player_general_stats.csv"  # Change as needed
    salary_file = "nba_player_salary.csv"  # Change as needed
    shooting_stats_file = "nba_shooting_stats.csv"  # Change as needed
    output_file = "nba_merged_data.csv"  # Change as needed
    merge_nba_datasets(general_stats_file, salary_file, shooting_stats_file, output_file)
