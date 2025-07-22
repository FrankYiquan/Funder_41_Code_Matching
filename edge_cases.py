# mainly used to handle edge cases for fund provided by European Commision and Chinese government(national, provincial)
def handle_edge_cases(compareNames, country):
    EU_List = ["Horizon 2020", "H2020", "HORIZON EUROPE","seventh framework programme","fp7"]
    MOST_List = ["Key Research and Development", "973", "Recruitment Program of Global Experts", "National Basic Research"]
    MOE_List = ["Central University Basic Research Fund", "Basic Scientific Research Business Expense", "fundamental research fund"]

    for compareName in compareNames:
        matched_funderObject = {}

        if compareName is None:
            continue

        # HORIZON EUROPE funded by European Commission
        if any(eu_name.lower() in compareName.lower() for eu_name in EU_List):
            matched_funderObject["matched_funder"] = "European Commission (Belgium, Brussels) - EC"
            matched_funderObject["code"] = "41___EUROPEAN_COMMISSION_(BRUSSELS)"

        # MOST - Ministry of Science and Technology of the People's Republic of China
        elif any(MOST_name.lower() in compareName.lower() for MOST_name in MOST_List) and country == "China":
            matched_funderObject["matched_funder"] = "Ministry of Science and Technology of the People's Republic of China (China, Beijing) - MOST"
            matched_funderObject["code"] = "41___MINISTRY_OF_SCIENCE_AND_TECHNOLOGY_OF_THE_PEOPLE'S_REPUBLIC_OF_CHINA_(BEIJING)"

        # MOE - Ministry of Education of the People's Republic of China
        elif any(MOE_name.lower() in compareName.lower() for MOE_name in MOE_List) and country == "China": 
            matched_funderObject["matched_funder"] = "Ministry of Education of the People's Republic of China (China, Beijing) - MOE"
            matched_funderObject["code"] = "41___MINISTRY_OF_EDUCATION_OF_THE_PEOPLE'S_REPUBLIC_OF_CHINA_(BEIJING)"

        # "National Office of Philosophy and Social Sciences (China, Beijing)"
        elif "national social science" in compareName.lower() and country == "China":
            matched_funderObject["matched_funder"] = "National Office of Philosophy and Social Sciences (China, Beijing)"
            matched_funderObject["code"] = "41___NATIONAL_PLANNING_OFFICE_OF_PHILOSOPHY_AND_SOCIAL_SCIENCE_(BEIJING)"


        #NSFC - National Natural Science Foundation of China
        elif "national natural science" in compareName.lower() and "province" not in compareName.lower() and country == "China":
            matched_funderObject["matched_funder"] = "National Natural Science Foundation of China (China, Beijing) - NSFC"
            matched_funderObject["code"] = "41___NATIONAL_NATURAL_SCIENCE_FOUNDATION_OF_CHINA_(BEIJING)"
        
        elif "swedish cancer" in compareName.lower() and country == "Sweden":
            matched_funderObject["matched_funder"] = "Swedish Cancer Society (Sweden, Stockholm)"
            matched_funderObject["code"] = "41___SWEDISH_CANCER_SOCIETY_(STOCKHOLM)"
        
        # Sanming Project of Medicine in Shenzhen
        elif "sanming" in compareName.lower() and "shenzhen" in compareName.lower():
            matched_funderObject["matched_funder"] = "Shenzhen Municipal People's Government (China, Shenzhen)"
            matched_funderObject["code"] = "41___SHENZHEN_MUNICIPAL_PEOPLE'S_GOVERNMENT_(SHENZHEN)"


        # Multidisciplinary University Research Initiative
        elif "multidisciplinary university research" in compareName.lower():
            matched_funderObject["matched_funder"] = "United States Department of Defense (United States, Washington) - US DOD"
            matched_funderObject["code"] = "41___UNITED_STATES_DEPARTMENT_OF_DEFENSE_(WASHINGTON_D.C.)"
        
        # Natural Science Foundation of Jiangxi Province
        elif "jiangxi" in compareName.lower() and "natural science foundation" in compareName.lower():
            matched_funderObject["matched_funder"] = "Jiangxi Provincial Department of Science and Technology (China, Nanchang)"
            matched_funderObject["code"] = "41___JIANGXI_PROVINCIAL_DEPARTMENT_OF_SCIENCE_AND_TECHNOLOGY_(NANCHANG)"

        # Ono Pharma Foundation
        elif "ono pharma" in compareName.lower():
            matched_funderObject["matched_funder"] = "Ono Pharmaceutical (United States, Trenton)"
            matched_funderObject["code"] = "41___ONO_PHARMACEUTICAL_(UNITED_STATES)_(TRENTON)"

        # Natural Science Foundation of Guangdong Province
        elif "guangdong" in compareName.lower() and ("natural science foundation" in compareName.lower() or "basic and applied basic research" in compareName.lower()):
            matched_funderObject["matched_funder"] = "Guangdong Science and Technology Department (China, Guangzhou)"
            matched_funderObject["code"] = "41___GUANGDONG_SCIENCE_AND_TECHNOLOGY_DEPARTMENT_(GUANGZHOU)"

        # Natural Science Foundation of Hunan Province
        elif "hunan" in compareName.lower() and "natural science foundation" in compareName.lower():
            matched_funderObject["matched_funder"] = "Hunan Provincial Science and Technology Department (China, Changsha) - HSTD"
            matched_funderObject["code"] = "41___HUNAN_PROVINCIAL_SCIENCE_AND_TECHNOLOGY_DEPARTMENT_(CHANGSHA)"

        # Natural Science Foundation of Shandong Province
        elif "shandong" in compareName.lower() and "natural science foundation" in compareName.lower():
            matched_funderObject["matched_funder"] = "Department of Science and Technology of Shandong Province (China, Jinan)"
            matched_funderObject["code"] = "41___DEPARTMENT_OF_SCIENCE_AND_TECHNOLOGY_OF_SHANDONG_PROVINCE_(JINAN)"

        # Guangxi Key Laboratory of Automatic Detection Technology and Instrument Foundation
        elif "guangxi" in compareName.lower() and "key laboratory" in compareName.lower():
            matched_funderObject["matched_funder"] = "Guangxi Science and Technology Department (China, Nanning)"
            matched_funderObject["code"] = "41___GUANGXI_SCIENCE_AND_TECHNOLOGY_DEPARTMENT_(NANNING)"
        
        # Natural Science Foundation of Beijing Municipality
        elif "beijing" in compareName.lower() and "natural science foundation" in compareName.lower():
            matched_funderObject["matched_funder"] = "Beijing Municipal Government (China, Beijing)"
            matched_funderObject["code"] = "41___BEIJING_MUNICIPAL_GOVERNMENT_(BEIJING)"
        
        # Harvard Catalyst
        elif "harvard catalyst" in compareName.lower():
            matched_funderObject["matched_funder"] = "Harvard University (United States, Cambridge)"
            matched_funderObject["code"] = "41___HARVARD_UNIVERSITY_(CAMBRIDGE)"

        # Materials Research Institute, Penn State
        elif "materials research institute" in compareName.lower() or "pennsylvania state university" in compareName.lower():
            matched_funderObject["matched_funder"] = "Pennsylvania State University (United States, State College) - PSU"
            matched_funderObject["code"] = "41___PENNSYLVANIA_STATE_UNIVERSITY_(STATE_COLLEGE)"

        # Gansu University of Traditional Chinese Medicine
        elif "gansu university of traditional chinese medicine" in compareName.lower():
            matched_funderObject["matched_funder"] = "Gansu University of Traditional Chinese Medicine (China, Lanzhou)"
            matched_funderObject["code"] = "41___GANSU_UNIVERSITY_OF_TRADITIONAL_CHINESE_MEDICINE_(LANZHOU)"

        # Global Challenges Research Fund
        elif "global challenges research fund" in compareName.lower():
            matched_funderObject["matched_funder"] = "Department for Business, Energy and Industrial Strategy (United Kingdom, London) - BEIS"
            matched_funderObject["code"] = "41___DEPARTMENT_FOR_BUSINESS,_ENERGY_AND_INDUSTRIAL_STRATEGY_(LONDON)"
        
        # National Drug Abuse Treatment Clinical Trials Network
        elif "clinical trials network" in compareName.lower() or "drug abuse treatment" in compareName.lower() and country == "United States":
            matched_funderObject["matched_funder"] = "Clinical Trial Network (United States, Houston) - CTN"
            matched_funderObject["code"] = "41___CLINICAL_TRIAL_NETWORK_(HOUSTON)"
        
        elif "maternal and child health bureau" in compareName.lower() and country == "United States":
            matched_funderObject["matched_funder"] = "Health Resources and Services Administration (United States, Rockville) - HRSA"
            matched_funderObject["code"] = "41___HEALTH_RESOURCES_AND_SERVICES_ADMINISTRATION_(ROCKVILLE)"

        elif "iowa science foundation" in compareName.lower() and country == "United States":
             matched_funderObject["matched_funder"] = "Iowa Academy of Science (United States, Cedar Falls) - IAS"
             matched_funderObject["code"] = "41___IOWA_ACADEMY_OF_SCIENCE_(CEDAR_FALLS)"
        
        elif "facebook" in compareName.lower():
             matched_funderObject["matched_funder"] = "Meta (United States, Menlo Park) - FB"
             matched_funderObject["code"] = "41___FACEBOOK_(UNITED_STATES)_(MENLO_PARK)"

        elif "science and technology department"in compareName.lower() and "zhejiang" in compareName.lower():
            matched_funderObject["matched_funder"] = "Science and Technology Department of Zhejiang Province (China, Hangzhou)"
            matched_funderObject["code"] = "41___SCIENCE_AND_TECHNOLOGY_DEPARTMENT_OF_ZHEJIANG_PROVINCE_(HANGZHOU)"



        if matched_funderObject != {}:
            matched_funderObject['matched'] = "EdgeCase"
            return matched_funderObject
        
     
    
   
    matched_funderObject['matched'] = "not_found"
    return matched_funderObject


# compareName = ['EU Framework Programme for Research and Innovation', 'Horizon 2020', 'Horizon 2020 - Research and Innovation Framework Programme', 'European Union Framework Programme for Research and Innovation']
# country = "United States"
# print(handle_edge_cases(compareName, country))