import requests
from bs4 import BeautifulSoup
import concurrent.futures
import pandas as pd
import csv

authorities = ['albury',
'armidale',
'ballina',
'bathurst',
'bayside',
'bega',
'bellingen',
'berrigan',
'blacktown',
'blue_mountains',
'bogan',
'broken_hill',
'burwood',
'byron',
'camden',
'campbelltown',
'bankstown',
'gosford',
'wyong',
'cessnock',
'canada_bay',
'lismore',
'ryde',
'sydney',
'wagga_wagga',
'coffs_harbour',
'cootamundra_gundagai',
'cowra',
'cumberland',
'dubbo',
'eurobodalla',
'fairfield',
'forbes',
'georgesriver',
'goulburn',
'greater_hume',
'griffith',
'gunnedah',
'hawkesbury',
'hornsby',
'ashfield',
'leichhardt',
'marrickville',
'inverell',
'kiama',
'kuringgai',
'kyogle',
'lake_macquarie',
'lane_cove',
'leeton',
'lithgow',
'liverpool',
'liverpool_plains',
'maitland',
'great_lakes',
'greater_taree',
'midwestern',
'mosman',
'muswellbrook',
'nambucca',
'north_sydney',
'northern_beaches',
'nsw_dop',
'nsw_olgr',
'nsw_jrpp',
'orange',
'parkes',
'parramatta',
'penrith',
'port_macquarie_hastings',
'port_stephens',
'qprc',
'randwick',
'richmond_valley',
'shellharbour',
'shoalhaven',
'singleton',
'strathfield',
'sutherland',
'tamworth',
'newcastle',
'the_hills',
'tweed_shire',
'upper_hunter',
'uralla',
'walcha',
'walgett',
'warrumbungle',
'waverley',
'weddin',
'willoughby',
'wingecarribee',
'wollondilly_shire',
'wollongong',
'woollahra',
'yass']


csv_file = open('nsw.csv', 'w+')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['reference', 'address', 'description', 'link', 'authority'])

def getData(url):
    print(f'Getting page {url}')
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    table = soup.find('ol', class_='applications')
    applications = table.find_all('article', class_='application')
    page = url.split('page=')[1]
    for application in applications:
        print('Getting application...')
        address = application.find('div', class_='address').text.strip()
        description = application.find('p', class_='description').text.strip()
        link = 'https://www.planningalerts.org.au' + str(application.find('a')).split('"')[1]
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'lxml')
        reference = soup.find('p', class_='source').text.split('reference ')[1].split(')')[0].strip()
        authority = url.split('authorities/')[1].split('/')[0]
        with open('nsw.csv', 'a+'):
            csv_writer.writerow([reference, address, description, link, authority])

with concurrent.futures.ThreadPoolExecutor() as executor:
    urls = [f'https://www.planningalerts.org.au/authorities/{authority}/applications?page=1' for authority in authorities]
    for url in urls:
        executor.submit(getData, url)



csv_file.close()

