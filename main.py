import pandas as pd
import csv

from funder_match import get_funder_from_openAlex, exact_match, get_funder_parent

if __name__ == "__main__":
    try:
        #load required csv file

        #load external funder_count_openAlex csv
        extFunders_df = pd.read_csv("unique_funders/output/sorted_funder_data.csv")
        extFunders_dict = extFunders_df.to_dict(orient='records')

        # #load country_code csv
        # country_code_df = pd.read_csv('resource/country_code.csv')
        # country_code_dict = country_code_df.set_index('alpha-2').to_dict(orient='index')

        # load internal funder csv
        intFunders_df = pd.read_csv("resource/internel_funders.csv")
        intFunders_dict = intFunders_df.to_dict(orient='records')

        records = []

        #visulization
        total_extFunders = len(extFunders_dict)
        processed = 0

        #for each funder in external funder list, begin the matching logic
        for extFunder in extFunders_dict:
            extFunder_object = {
                "funder_name": extFunder.get("funder_name"),
                "openalex": extFunder.get("openalex_id")
            }

            try:
                # get info about this external funder from openalex
                funder_opneAlex_object = get_funder_from_openAlex(extFunder_object)

                # do the matching using either (funder names & country) or (acronym & country)
                #child_match contains external funder openalex & ror info + matched name and code (if matched)
                child_match = exact_match(funder_opneAlex_object, intFunders_dict, False) #1

                #if no matched result, use ror to locate parent and use parent info to perform matching
                parent_match = {} 
                if child_match.get("matched") == "not_found":
                    child_ror = child_match.get("ror")
                    parent = get_funder_parent(child_ror)

                    #if parent is found, perform the matching 
                    if parent.get("funder_name") != "not_found":
                        #parent match contains parent openalex info + matched funder name and code (if matched)
                        parent_match = exact_match(parent, intFunders_dict, True) #2
                
                #format child_match and parent match(if had) to a record in csv file
                record = {
                    "unique_funder": child_match.get("funder_name"),
                    "matched_funder": child_match.get("matched_funder")if child_match.get("matched") != "not_found" else parent_match.get("matched_funder", "not_found"),
                    "matched_funder_code": child_match.get("code")if child_match.get("matched") != "not_found" else parent_match.get("code", "not_found"),
                    "matched_object": "child/"+ child_match.get('matched') if child_match.get("matched") != "not_found" else "parent/" + parent_match.get("matched", "not_found")
                }

                records.append(record)
                processed += 1

                print(f"processed funder: {record.get('unique_funder')}, {record.get('matched_object')},{processed}/{total_extFunders}")

            except Exception as e:
                print(f"Error processing funder: {extFunder.get('funder_name')}, error: {e}")
                break  # or use `continue` if you want to skip and keep going

    finally:
        # save the result to the output file when there is an error
        with open('match_output.csv', 'w', newline='') as csvfile:
            fieldnames = ['unique_funder', 'matched_funder', 'matched_funder_code', 'matched_object']  # Replace with your actual fields
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(records)
            
        print("The result has been saved to match_output.csv")
