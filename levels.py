import re
import json
import requests

class Levels:
    def __init__(self):
        self.url = 'https://www.levels.fyi/js/internshipData.json'

        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }

        self.req = requests.get(self.url, headers=headers)
    
    def sort_json(self):
        postings = json.loads(self.req.content)
        new_postings = {}
        season = {
            'spring': 0,
            'summer': 1,
            'fall': 2,
            'winter': 3,
            '': -1
        }
        for posting in postings:
            company = ''.join(re.findall('(\w+)', posting['company'])).lower()
            position = ''.join(re.findall('(\w+)', posting['title'])).lower()
            hourlysalary = posting['hourlySalary'] if 'hourlySalary' in posting else ''
            year = re.findall('(\d+)', posting['yr'])[0]
            
            if company in new_postings:
                if position in new_postings[company]:
                    if int(new_postings[company][position]['year']) < int(year):
                        new_postings[company][position]['year'] = year
                        new_postings[company][position]['season'] = posting['season']
                        new_postings[company][position]['hourlysalary'] = hourlysalary
                    elif int(new_postings[company][position]['year']) == int(year):
                        if season[new_postings[company][position]['season'].lower()] < season[posting['season'].lower()]:
                            new_postings[company][position]['year'] = year
                            new_postings[company][position]['season'] = posting['season']
                            new_postings[company][position]['hourlysalary'] = hourlysalary
                else:
                    new_postings[company][position] = {
                        'year': year,
                        'season': posting['season'],
                        'hourlysalary': hourlysalary
                    }
            else:
                new_postings[company] = {
                    position: {
                        'year': year,
                        'season': posting['season'],
                        'hourlysalary': hourlysalary
                    }
                }
        return new_postings