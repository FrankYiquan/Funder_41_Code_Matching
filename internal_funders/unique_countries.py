import pandas as pd
import os

def save_unique_countries():
    """
    Reads the fixed CSV file, extracts unique countries from the 'Country' column,
    saves them to 'unique_countries' (no extension) in the same folder,
    and returns the list of unique countries.
    """
    csv_path = "internal_funders/output/new_internal_41.csv"
    try:
        df = pd.read_csv(csv_path)
        unique_values = sorted(df["Country"].dropna().unique())

        folder = os.path.dirname(csv_path)
        output_path = os.path.join(folder, "unique_countries")  # no extension

        with open(output_path, "w", encoding="utf-8") as f:
            for country in unique_values:
                f.write(f"{country}\n")

        print(f"Unique countries written to: {output_path}")
        return unique_values

    except FileNotFoundError:
        print(f"File not found: {csv_path}")
        return []
    except KeyError:
        print("Column 'Country' not found in the CSV.")
        return []

# Example usage:
unique_countries = save_unique_countries()
