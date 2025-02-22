import os
from bs4 import BeautifulSoup
import pandas as pd

# Define paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Parent directory
HTML_FILE = os.path.join(BASE_DIR, "static", "nba_page_structure.html")
CSV_FILE = os.path.join(BASE_DIR, "static", "nba_shooting_stats.csv")

# Load the HTML file
with open(HTML_FILE, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find all tables and select the shooting stats table (Index 2 from earlier analysis)
tables = soup.find_all("table")
shooting_table = tables[2] if len(tables) > 2 else None

if shooting_table:
    # Extract header rows (Main Categories and Subcategories)
    header_rows = shooting_table.find_all("tr")[:2]  # First two rows are headers

    # Extract main headers (distance categories)
    main_headers = [th.text.strip() for th in header_rows[0].find_all("th")]
    main_headers = [h if h else main_headers[i - 1] for i, h in enumerate(main_headers)]  # Fill empty categories

    # Extract subheaders (FGM, FGA, FG% under each distance category)
    sub_headers = [th.text.strip() for th in header_rows[1].find_all("th")]

    # Create final column names: Combine main headers and subheaders properly
    column_names = []
    main_index = -1
    for sub in sub_headers:
        if sub in ["FGM", "FGA", "FG%"]:
            column_names.append(f"{main_headers[main_index]} {sub}")  # Include distance category in column name
        else:
            main_index += 1
            column_names.append(sub)  # For non-FGM/FGA/FG% headers like "Player", "Team", etc.

    # Extract rows data
    rows = []
    for row in shooting_table.find_all("tr")[2:]:  # Skip header rows
        cols = row.find_all("td")
        row_data = [col.text.strip() for col in cols]
        if row_data:
            rows.append(row_data)

    # Ensure headers and data column alignment
    num_columns = min(len(column_names), len(rows[0])) if rows else len(column_names)
    column_names = column_names[:num_columns]
    rows = [row[:num_columns] for row in rows]

    # Convert to DataFrame
    df_shooting_stats = pd.DataFrame(rows, columns=column_names)

    # Save to CSV
    df_shooting_stats.to_csv(CSV_FILE, index=False)

    print(f"✅ Data successfully extracted and saved to {CSV_FILE}")

else:
    print("❌ Error: Shooting stats table not found in the provided HTML file.")
