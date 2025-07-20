
import pandas as pd
import re

import csv
def normalize_internel_funders():
    de = pd.read_csv('resource/internel_funders.csv')
    internelFunder_dict = de.to_dict(orient='records')

    result = []

    for intFunder in internelFunder_dict:
        name = intFunder.get("Name")
        #print(name)
        # Name Format: Funder_name (Country, City)
        intFunder_name = name.split("(")[0]
        intFunder_Country, intFunder_City = get_country_city(name)
        intFunder_acronym =  name.split(") -")[-1].strip() if ") -" in name else "not_found"
        intFunder_acronym_strip = name.split(") -")[-1].strip().replace(" ", "") if ") -" in name else "not_found"

        record = {
            "Code": intFunder.get("Code"),
            "Name": intFunder.get("Name"),
            "Type": intFunder.get("Type"),
            "Country": intFunder_Country,
            "City": intFunder_City,
            "Name_Only": intFunder_name,
            "Acronym": intFunder_acronym,
            "Acronym_Strip": intFunder_acronym_strip
        }

        result.append(record)

    with open('internal_funders/output/updated_new_internal_41.csv', 'w', newline='') as csvfile:
        fieldnames = ['Code', 'Name', 'Type', 'Country', "City", "Name_Only", "Acronym", "Acronym_Strip"]  # Replace with your actual fields
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(result)

# extract funderName, country, and city from internel matched funder
def extract_country_city(funder_name):
    # Find the last occurrence of "(" and ")"
    last_parenthesis_part = funder_name.split("(")[-1].split(")")[0].strip()

    # Handle case if there's a '/' in the string (multiple cities)
    if "/" in last_parenthesis_part:
        last_parenthesis_part = last_parenthesis_part.split("/")[0].strip()

    # Split by comma to get country and city
    try:
        intFunder_Country, intFunder_City = [x.strip() for x in last_parenthesis_part.split(",")]
        return intFunder_Country, intFunder_City
    except ValueError:
        # In case the format is wrong or there's no comma
        return "not_found", "not_found"
    



def get_country_city(funder_name):
    # Find the last (...) group
    match = re.findall(r"\(([^()]*)\)", funder_name)
    if match:
        parts = match[-1].split(",")
        if len(parts) >= 2:
            country = parts[0].strip()
            city = ",".join(parts[1:]).strip()
            return country, city
    return "not_found", "not_found"


normalize_internel_funders()
