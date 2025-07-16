import requests
from rapidfuzz import fuzz
import pandas as pd
import re


def fuzzy_similarity(name1, name2):
    return fuzz.ratio(name1.lower(), name2.lower()) 


#get funder's openAlex id based on its name
#if you get funderId when acessing article's grant, this method can be ignored
#This method is not used
def pre_process(funderName):
    url = f"https://api.openalex.org/funders?search={funderName}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        funders = data.get("results", [])
        if len(funders) > 0:
            funder = funders[0]
            id = funder.get("id", "not_found")
            return {
                "funder_name": funderName,
                "openalex": id.split("org/")[1] if id != "not_found" else "not_found"
                }
    return {
            "funder_name": funderName,
            "openalex": "not_found"
            }


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
def exact_match(funderObject, internelFunderDict, parent = False):
    extFunder_country = ""
    extFunder_name = funderObject.get("funder_name")
    extFunder_compareNames = list(set(filter(None, [funderObject.get("funder_name"), funderObject.get("display_name"), *(funderObject.get("alternate_titles") or [])])))
    # put all the names of a funder need to compared in a list
    extFunder_acronyms = funderObject.get("acronyms",[])

    #search for alternative names in ror
    if not parent: 
        #parent does NOT need to go to ror, b/c we pull their info from ror
        if funderObject.get("ror", "not_found") != "not_found":
            openalex_names = get_name_from_openAlex(funderObject.get("ror"))
            openalex_altNames = openalex_names.get("alt_names")
            openalex_acronyms = openalex_names.get("acronyms")
            extFunder_country = openalex_names.get("country_code")
            if openalex_altNames != []:
                extFunder_compareNames = list(set(extFunder_compareNames + openalex_altNames))
            
            if openalex_altNames != []:
                extFunder_acronyms = list(set(openalex_acronyms + extFunder_acronyms))
    else:
        extFunder_country = funderObject.get("country_code")

    # print(extFunder_compareNames)
    # print(extFunder_acronyms)

    for intFunder in internelFunderDict:
        name = intFunder.get("Name")
        #print(name)
        # Name Format: Funder_name (Country, City)
        intFunder_name = name.split("(")[0]
        intFunder_Country, intFunder_City = extract_country_city(name)
        intFunder_acronym =  name.split(") -")[-1].strip() if ") -" in name else "not_found"
        intFunder_acronym_strip = name.split(") -")[-1].strip().replace(" ", "") if ") -" in name else "not_found"

        #  (1) match by funderName and Country
        for compareName in extFunder_compareNames:
            # if the similarity score higher than 90 and country match => matched funder
            if fuzzy_similarity(compareName, intFunder_name) >= 90 and intFunder_Country.lower() == extFunder_country.lower():
                funderObject["matched"] = "Exact" #exact/acronym/parent/not_found
                funderObject["matched_funder"] = intFunder.get("Name")
                funderObject["matched_funder_display_name"] = extFunder_name
                funderObject["code"] = intFunder.get("Code")
                funderObject["matched_funder_country"] = intFunder_Country
                funderObject["matched_funder_city"] = intFunder_City
                return funderObject
        
        # (2) use acronyms to match 
        if intFunder_acronym != "not_found" and intFunder_acronym_strip != "not_found":
            for acronym in extFunder_acronyms:
                if (intFunder_acronym == acronym or intFunder_acronym_strip == acronym) and intFunder_Country.lower() == extFunder_country.lower():
                    funderObject["matched"] = "acronym" #exact/acronym/parent/not_found
                    funderObject["matched_funder"] = intFunder.get("Name")
                    funderObject["matched_funder_display_name"] = extFunder_name
                    funderObject["code"] = intFunder.get("Code")
                    funderObject["matched_funder_country"] = intFunder_Country
                    funderObject["matched_funder_city"] = intFunder_City
                    return funderObject
    funderObject["matched"] = "not_found"
    return funderObject


def get_name_from_openAlex(openAlexId):
     url = f"https://api.ror.org/v2/organizations/{openAlexId}"
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
        "country_code": funder.get("locations")[0].get("geonames_details").get("country_name")
    }
                 

#search for parent of funder
# this method is only used for the funder itself does not have a 41 code
def get_funder_parent(child_ror):
    #extract ror id
    url = f"https://api.ror.org/v2/organizations/{child_ror}"
    response = requests.get(url)
    if response.status_code == 200:
         child = response.json()
         relationships = child.get("relationships", [])
         for relationship in relationships:
             if (relationship.get("type") == "parent"):
                  parent_ror = relationship.get("id").split("org/")[1] if relationship.get("id", "") != "" else "not_found"
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



# print(get_funder_parent("0447fe631"))
# print(get_name_from_openAlex("05072yv34"))
    





# print(get_funder_from_openAlex({"funder_name": "Swedish Cancer Foundation", "openalex": "F4320313607"}))
                


                
# print(fuzzy_similarity("Ministry of Economy, Industry and Competitiveness", "Ministry of Economy, Industry and Competitiveness"))






        








# df = pd.read_csv('resource/country_code.csv')
# country_dict = df.set_index('alpha-2').to_dict(orient='index')

# de = pd.read_csv('resource/internel_funders.csv')
# internelFunder_dict = de.to_dict(orient='records')

# funderObject = {'ror': '02rcrvv70', 'homepage_url': 'https://www.usa.gov/', 'country_code': 'United States', 'display_name': '', 'id': '', 'funder_name': 'Government of the United States of America'}

# result = exact_match(funderObject, internelFunder_dict, country_dict, True)
# print(result)




