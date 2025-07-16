#this script is to get data from OpenAlex API for Brandeis University grants

import requests
import json
import math
import os


class get_data_openAlex:
#Brandeis institution id: i6902469

#this url is for Brandeis 2024
#api for get only 2024 grants: https://api.openalex.org/works?filter=institutions.id:https://openalex.org/I6902469,publication_year:2024&sort=publication_date:desc

    def __init__(self, base_url, file_name):
        self.base_url = base_url
        self.file_name = file_name


#base_url = 'https://api.openalex.org/works?filter=institutions.id:https://openalex.org/I6902469,publication_year:2023&sort=publication_date:desc'
    def get_data_openAlex(self):
        all_results = []
        base_url = self.base_url  # without page parameter
        per_page = 25  # as indicated by your meta
        page = 1

        # Ensure the directory exists before writing the file
        output_dir = os.path.dirname(self.file_name)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # First request to get count and per_page
        response = requests.get(f"{base_url}&page={page}")
        if response.status_code != 200:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return
        
        data = response.json()
        all_results.extend(data.get('results', []))

        count = data.get('meta', {}).get('count', 0)
        per_page = data.get('meta', {}).get('per_page', 25)
        total_pages = math.ceil(count / per_page)

        # Fetch rest of the pages
        for page in range(2, total_pages + 1):
            response = requests.get(f"{base_url}&page={page}")
            if response.status_code != 200:
                print(f"Failed to fetch page {page}. Status code: {response.status_code}")
                break
            data = response.json()
            all_results.extend(data.get('results', []))

        with open(self.file_name, 'w') as json_file:
            json.dump(all_results, json_file, indent=4)

# if __name__ == "__main__":
#     base_url = 'https://api.openalex.org/works?filter=institutions.id:https://openalex.org/I6902469,publication_year:2020&sort=publication_date:desc'
#     file_name = 'brandeis_2024.json'

#     fetcher = get_data_openAlex(base_url, file_name)
#     fetcher.get_data_openAlex()
