import csv

#after get the openalex id, funder count, you can sort the file by funder count
def sort_csv_by_count(input_file, output_file):
    # Read the CSV data
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        # Sort the rows by the 'count' column in descending order
        sorted_rows = sorted(reader, key=lambda row: int(row['count']), reverse=True)

    # Write the sorted data to a new CSV file
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['funder_name', 'count', 'openalex_id']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()  # Write the header
        writer.writerows(sorted_rows)  # Write the sorted rows

    print(f"Data sorted and saved to {output_file}")

# # Example usage
# input_file = 'funder_data.csv'  # Your input file path
# output_file = 'output/sorted_funder_data.csv'  # The output sorted file path

# sort_csv_by_count(input_file, output_file)
