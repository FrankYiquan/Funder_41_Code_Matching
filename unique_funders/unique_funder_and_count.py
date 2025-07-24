import json
import csv
from collections import Counter, defaultdict

from all_articles import get_data_openAlex

# this extract funder name, grant-specific id, openalex id from articles in a self-defined time intervel; funder have no duplicates.
def get_all_funder(start_year: int, end_year: int, schoolId):
    funder_counts = Counter()
    funder_set = set()
    openalex_dict = defaultdict(str)

    for year in range(start_year, end_year + 1):
        input_file_name = 'unique_funders/output/article_grant.json' 
        base_url = f'https://api.openalex.org/works?filter=institutions.id:https://openalex.org/{schoolId},publication_year:{year}&sort=publication_date:desc'
        
        # get article from OpenAlex API
        get_data_openAlex(base_url, input_file_name).get_data_openAlex()

        # Load JSON data
        with open(input_file_name, 'r') as json_file:
            data = json.load(json_file)

        # Extract funder names and OpenAlex IDs
        for item in data:
            for grant in item.get('grants', []):
                funder_name = grant.get('funder_display_name', '')
                award_id = grant.get('award_id', '')
                openalex_id = grant.get("funder", "").split(".org/")[1]  # Extract OpenAlex ID
                
                # Add funder if conditions are met
                if funder_name and funder_name != "CERN" and award_id:
                    funder_set.add(funder_name)
                    funder_counts[funder_name] += 1
                    openalex_dict[funder_name] = openalex_id  # Map funder name to OpenAlex ID

        print(f"Processed year {year}: found {len(funder_set)} unique funders so far.")
        
    # # Save unique funder names to a JSON file
    # with open("unique_funders/output/unique_funders.json", "w") as f:
    #     json.dump(sorted(list(funder_set)), f, indent=2)

    # # Save funder counts to a JSON file
    # sorted_counts = dict(funder_counts.most_common())
    # with open("unique_funders/output/funder_counts.json", "w") as f:
    #     json.dump(sorted_counts, f, indent=2)

    # Save the combined data to a CSV file
    with open("unique_funders/output/funder_data.csv", mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['funder_name', 'count', 'openalex_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write the header
        for funder_name in funder_set:
            writer.writerow({
                'funder_name': funder_name,
                'count': funder_counts[funder_name],
                'openalex_id': openalex_dict.get(funder_name, '')
            })

    print("Saved unique_funders.json, funder_counts.json, and funder_data.csv.")

#Example Usage

# schoolId = "I6902469" #openAlex id for Brandeis University
# get_all_funder(2018, 2024, schoolId)