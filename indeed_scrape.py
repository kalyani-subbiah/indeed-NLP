import json
from random import uniform
from time import sleep

import requests
from bs4 import BeautifulSoup

INDEED_URL = "https://www.indeed.com"
NUM_PAGES = 100
OUTPUT_FILE = '/Users/kalyani/01ColumbiaQMSS/01Semester2/NLP/Homework_1/ks3626_indeed_job_descs.json'

request_params = {
    'q': 'python',
    'l': 'New York State',
    'jt': 'contract'}

job_descs = []
for i in range(NUM_PAGES):
    
    # Step 1, get the search page results
    request_params.update({'start': i * 10})
    indeed_response = requests.get(url=INDEED_URL + '/jobs',
                                   params=request_params)
    if indeed_response.status_code != 200:
        print('(1)non-200 response for search page, skipping')
        continue

    indeed_search_html = indeed_response.text
    parsed_job_searches = BeautifulSoup(indeed_search_html, 'html.parser')
    posting_divs = parsed_job_searches.find_all(
        'div',
        attrs={"class": ["row", "result", "clickcard"]})
    #print([div.attrs for div in posting_divs])
    job_ids = []
    
    #job_ids = [div.attrs['data-jk'] for div in posting_divs]
    for div in posting_divs:
    	try:
    		job_ids.append(div.attrs['data-jk'])
    		print("passed")
    	except KeyError as error:
    		print("KeyError")

    # Get the individual job descriptions
    for job_id in job_ids:
        posting_response = requests.get(url=INDEED_URL + '/viewjob',
                                        params={'jk': job_id})
        print(posting_response.url)
        indeed_job_html = posting_response.text
        if posting_response.status_code != 200:
            print('(2)non-200 response for job description page, skipping')
            continue
        parsed_job_post = BeautifulSoup(indeed_job_html, 'html.parser')
        job_div = parsed_job_post.find(
            'div',
            attrs={'class': 'jobsearch-JobComponent-description'})
        # Checks if there's data at all
        if job_div:
            job_descs.append(job_div.get_text())
        print(len(job_descs))
        if len(job_descs) >= 100:
            break

        # DO NOT REMOVE THIS!
        # You're scraping, this slows down your request so you
        # do not overwhelm the site
        sleep(uniform(1, 5))
    if len(job_descs) >= 100:
        break

json.dump({'request_params': request_params,
           'job_descriptions': job_descs},
          open(OUTPUT_FILE, 'w'))
