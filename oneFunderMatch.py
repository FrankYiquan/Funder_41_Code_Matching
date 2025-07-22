# from collections import defaultdict
# import pandas as pd
# import csv

# from funder_match import get_funder_from_openAlex, exact_match, get_funder_parent

# if __name__ == "__main__":
#     try:
#         #load required csv file

#         #load external funder_count_openAlex csv
#         extFunders_df = pd.read_csv("unique_funders/output/sorted_funder_data.csv")
#         extFunders_dict = extFunders_df.to_dict(orient='records')

#         # load internal funder csv
#         intFunders_df = pd.read_csv("internal_funders/output/new_internal_41.csv")
#         intFunders_dict = intFunders_df.to_dict(orient='records')
#         #create a dict with country as key record as value
#         country_intFunder_dict = defaultdict(list)
#         for record in intFunders_dict:
#             country = record.get("Country", "Unknown")
#             country_intFunder_dict[country].append(record)

        
#         # for testing
#         output = pd.read_csv("match_output.csv")
#         output_dict = output.set_index("unique_funder").to_dict(orient='index')

#         country = pd.read_csv("resource/country_code.csv")
#         country_dict = country.set_index("alpha-2").to_dict(orient='index')


#         records = []

#         #visulization
#         total_extFunders = len(extFunders_dict)
#         processed = 0

#         #for each funder in external funder list, begin the matching logic
#         for extFunder in extFunders_dict:

#             extFunder = extFunders_dict[364]
#             #testing
#             # key = extFunder.get("funder_name")
#             # if output_dict.get(key).get("matched_object") != "parent/not_found":
#             #     output_dict[key]['unique_funder'] = key
#             #     records.append(output_dict[key])
#             #     continue

#             extFunder_object = {
#                 "funder_name": extFunder.get("funder_name"),
#                 "openalex": extFunder.get("openalex_id")
#             }


#             # get info about this external funder from openalex
#             funder_opneAlex_object = get_funder_from_openAlex(extFunder_object)

#             # do the matching using either (funder names & country) or (acronym & country)
#             #child_match contains external funder openalex & ror info + matched name and code (if matched)
#             child_match = exact_match(funder_opneAlex_object, country_dict, country_intFunder_dict, intFunders_dict, False) #1

#             #if no matched result, use ror to locate parent and use parent info to perform matching
#             print(child_match.get("parent_rorId"))
#             parent_match = {} 
#             if child_match.get("matched") == "not_found" and child_match.get("parent_rorId", "not_found") != "not_found":
#                 print("here")
#                 hasParentAndNotMatched = True
#                 parent_ror = child_match.get("parent_rorId")
#                 while hasParentAndNotMatched:
#                     parent = get_funder_parent(parent_ror) #get parent info from ror

#                     #parent match contains parent ror info + matched funder name and code (if matched)
#                     parent_match = exact_match(parent, country_dict, country_intFunder_dict, intFunders_dict, True) #2
#                     if parent_match["matched"] == "not_found" and parent.get("parent_Id", "not_found") != "not_found":
#                         hasParentAndNotMatched = True
#                         parent_ror = parent.get("parent_rorId")
#                     else:
#                         hasParentAndNotMatched = False

            
#             #format child_match and parent match(if had) to a record in csv file
#             record = {
#                 "unique_funder": extFunder_object.get("funder_name"),
#                 "matched_funder": child_match.get("matched_funder")if child_match.get("matched") != "not_found" else parent_match.get("matched_funder", "not_found"),
#                 "matched_funder_code": child_match.get("code")if child_match.get("matched") != "not_found" else parent_match.get("code", "not_found"),
#                 "matched_object": "child/"+ child_match.get('matched') if child_match.get("matched") != "not_found" else "parent/" if parent_match != {} else  "child/" + parent_match.get("matched", "not_found")
#             }

#             records.append(record)
#             processed += 1


#             print(f"processed funder: {record.get('unique_funder')}, {record.get('matched_object')}, ({processed}/{total_extFunders})")
#             print(record)
#             break
      
            

#         # except Exception as e:
#         #     print(f"Error processing funder: {extFunder.get('funder_name')}, error: {e}")
#         #     break  # or use `continue` if you want to skip and keep going

#     finally:
#         #save the result to the output file when there is an error
#         # with open('new_match_output.csv', 'w', newline='') as csvfile:
#         #     fieldnames = ['unique_funder', 'matched_funder', 'matched_funder_code', 'matched_object']  # Replace with your actual fields
#         #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#         #     writer.writeheader()
#         #     writer.writerows(records)
            
#         print("The result has been saved to match_output.csv")
