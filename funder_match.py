import requests
from rapidfuzz import fuzz
import pandas as pd
import re


def fuzzy_similarity(name1, name2):
    #print(name1, name2)
    return fuzz.ratio(name1.lower(), name2.lower()) 


#get funder info from openAlex based on funderOpenAlexId
def get_funder_from_openAlex(funderObject):
    funder_name = funderObject.get("funder_name")
    funder_openalex = funderObject.get("openalex")
    url = f"https://api.openalex.org/funders/{funder_openalex}"
    response = requests.get(url)
    if response.status_code == 200:
        funder = response.json()
        ror = funder.get("ids", {}).get("ror", "not_found")
        return {
            "funder_name": funder_name, #
            "id": funder_openalex, #
            "display_name": funder.get("display_name", "not_found"), #
            "alternate_titles": [name for name in funder.get("alternate_titles", []) if len(name) >= 7], #
            "acronyms": [name for name in funder.get("alternate_titles", []) if len(name) < 7], #
            "country_code": funder.get("country_code", "not_found"), #
            "ror": ror.split("org/")[1] if ror != "not_found" else "not_found", #
            "homepage_url": funder.get("homepage_url", "not_found") #
        }
    
    return {
        "funder_name": funder_name,
        "id": funder_openalex,
        "display_name": "not_found",
        "alternate_titles": "not_found",
        "acronyms": "not_found",
        "country_code": "not_found",
        "ror": "not_found",
        "homepage_url":"not_found"
    }

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

# first match by name and country; if not found, match by acronym and country 
def exact_match(funderObject, countryDict, internalCountryFunderDict, internalFunderDict, parent = False):
    extFunder_country = ""
    extFunder_name = funderObject.get("funder_name")
    extFunder_compareNames = list(set(filter(None, [funderObject.get("funder_name"), funderObject.get("display_name"), *(funderObject.get("alternate_titles") or [])])))
    # put all the names of a funder need to compared in a list
    extFunder_acronyms = funderObject.get("acronyms",[])
    extFunder_parent = ""

    #search for alternative names in ror
    if not parent: 
        #parent does NOT need to go to ror, b/c we pull their info from ror
        if funderObject.get("ror", "not_found") != "not_found":
            openalex_names = get_name_from_ror(funderObject.get("ror"))
            openalex_altNames = openalex_names.get("alt_names")
            openalex_acronyms = openalex_names.get("acronyms")
            extFunder_country = openalex_names.get("country_code")
            extFunder_parent = openalex_names.get("parent_rorId")
            if openalex_altNames != []:
                extFunder_compareNames = list(set(extFunder_compareNames + openalex_altNames))
            
            if openalex_acronyms != []:
                extFunder_acronyms = list(set(openalex_acronyms + extFunder_acronyms))
        else:
            extFunder_country = countryDict.get(funderObject.get("country_code"), {}).get("name")
    else:
         extFunder_country = funderObject.get("country_code")
         extFunder_parent = funderObject.get("parent_rorId")

    print(extFunder_compareNames)
    #for testing
    #determine which dict for internal funders to used (full or key-based)
    country_funder_list = []
    if extFunder_country == "" or extFunder_country == "not_found" or extFunder_country is None:
        country_funder_list = internalFunderDict
    else: 
        #filter out funder that are not in the same country as funder
        country_funder_list = internalCountryFunderDict.get(extFunder_country, [])
        #only for Netherlands
        if extFunder_country == "Netherlands":
            country_funder_list += internalCountryFunderDict.get("The Netherlands", [])
        elif extFunder_country == "The Netherlands":
            country_funder_list += internalCountryFunderDict.get("Netherlands", [])
            extFunder_country = "Netherlands"
    
        #used full search if cannot find internal funders in country as key
        if country_funder_list == []:
            country_funder_list = internalFunderDict

    matched_funder = {}
    highest_similarity_score = -1
    for intFunder in country_funder_list:
        intFunder_name = intFunder.get("Name_Only")
        intFunder_Country = intFunder.get("Country")
        if intFunder_Country == "The Netherlands":
            intFunder_Country = "Netherlands"
        intFunder_City = intFunder.get("City")

        #  (1) match by funderName and Country
        for compareName in extFunder_compareNames:
            compareName = compareName.split("(")[0] #Meta (United States) => Meta
            similarity_score = fuzzy_similarity(compareName, intFunder_name)
            if similarity_score > highest_similarity_score and (extFunder_country is None or extFunder_country == intFunder_Country):
                highest_similarity_score = similarity_score
                matched_funder = intFunder

            # if the similarity score higher than 90 and country match => matched funder
            if similarity_score >= 90 and intFunder_Country == extFunder_country:
                funderObject["matched"] = "Exact" #exact/acronym/parent/not_found
                funderObject["matched_funder"] = intFunder.get("Name")
                funderObject["matched_funder_display_name"] = extFunder_name
                funderObject["code"] = intFunder.get("Code")
                funderObject["matched_funder_country"] = intFunder_Country
                funderObject["matched_funder_city"] = intFunder_City
                funderObject["parent_rorId"] = extFunder_parent
                return funderObject

    # if not found in country-listed funder
    intFunder_Country = matched_funder.get("Country") if matched_funder.get("Country") is not None else "not_found"
    intFunder_City = intFunder.get("City")
    if highest_similarity_score > 90 or (highest_similarity_score > 65 and intFunder_Country == extFunder_country) and extFunder_parent == "not_found":
        intFunder = matched_funder
        funderObject["matched"] = "HighestScore"
        funderObject["matched_funder"] = intFunder.get("Name")
        funderObject["matched_funder_display_name"] = extFunder_name
        funderObject["code"] = intFunder.get("Code")
        funderObject["matched_funder_country"] = intFunder_Country
        funderObject["matched_funder_city"] = intFunder_City
        funderObject["parent_rorId"] = extFunder_parent
        return funderObject

    funderObject["matched"] = "not_found"
    funderObject["parent_rorId"] = extFunder_parent
    return funderObject


def get_name_from_ror(rorId):
     url = f"https://api.ror.org/v2/organizations/{rorId}"
     response = requests.get(url)
     alt_names = []
     acronym = []
     if response.status_code == 200:
        funder = response.json()

        for name in funder.get("names", []):
            type = name.get("types")
            value = name.get("value")
            if "acronym" in type:
                acronym.append(value)
            else:
                alt_names.append(value)
     return {
        "alt_names": alt_names,
        "acronyms": acronym,
        "country_code": funder.get("locations")[0].get("geonames_details").get("country_name"),
        "parent_rorId": next((rel.get("id").split("org/")[1] for rel in funder.get("relationships", []) if rel.get("type") == "parent" and rel.get("id")), "not_found")
    }
                 

#search for parent of funder
# this method is only used for the funder itself does not have a 41 code
def get_funder_parent(parent_ror):
    #extract ror id
    url2 = f"https://api.ror.org/v2/organizations/{parent_ror}"
    parent_response = requests.get(url2)
    if parent_response.status_code == 200:
        parent = parent_response.json()
        parent_result = {}
        #make a new funderObject but for parent info
        parent_result["ror"] = parent.get("id").split("org/")[1] if parent.get("id", []) != [] else "not_found"
        parent_links = parent.get("links", [])
        parent_result["homepage_url"] = next((link.get("value") for link in parent_links if link.get("type") == "website"), "not_found")
        parent_result["country_code"] = parent.get("locations", [{}])[0].get("geonames_details", {}).get("country_name", "not_found")
        parent_result["parent_rorId"] = next((rel.get("id").split("org/")[1] for rel in parent.get("relationships", []) if rel.get("type") == "parent" and rel.get("id")), "not_found")
    

        #these two field is always null for parent
        parent_result["display_name"] = ""
        parent_result["id"] = ""

        #get parent name info
        for name in parent.get("names", []):
            type = name.get("types")
            value = name.get("value")
            if "ror_display" in type:
                parent_result["funder_name"] = value
            elif "acronym" in type:
                parent_result["acronyms"] = parent_result.get("acronyms", []) + [value]
            elif "label" in type or "alias" in type:
                parent_result["alternate_titles"] = parent_result.get("alternate_titles", []) + [value]

        return parent_result
    
    return {"funder_name": "not_found"}    




# print(fuzzy_similarity("Baker University", "Boston University"))
# funder_object = {
#     "funder_name": "Seventh Framework Programme",
#     "openalex": "F4320333065"
# }
# print(get_funder_from_openAlex(funder_object))


# print(fuzzy_similarity("Postdoctoral Research Foundation of China", "China Postdoctoral Science Foundation"))

# print(get_funder_parent("05eq41471"))