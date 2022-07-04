import re
import json
import requests

class Levels:
    def __init__(self):
        self.url = 'https://www.levels.fyi/js/internshipData.json'

        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }

        self.req = requests.get(self.url, headers=headers, timeout=10)
        self.postings = {}
    
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
        self.postings = new_postings
        return new_postings
    
    def get_job_titles(self):
        jobs = set()
        for i in self.postings:
            for b in self.postings[i].keys():
                jobs.add(b)
        return jobs
    
    @staticmethod
    def get_job_key(title, salaries):
        title = title.lower()
        print(title)
        if 'data' in title and 'engineer' in title:
            ing = salaries.get('dataengineering', {}).get('hourlysalary', 0)
            engineer = salaries.get('dataengineer', {}).get('hourlysalary', 0)
            if ing != 0:
                return ing
            elif engineer != 0:
                return engineer
            else:
                return 0
        elif 'software' in title and ('engineer' in title or 'develop' in title):
            return salaries.get('softwareengineer', {}).get('hourlysalary', 0)
        elif 'quant' in title and 'trade' in title:
            return salaries.get('quantitativetrader', {}).get('hourlysalary', 0)
        elif 'market' in title:
            return salaries.get('marketing', {}).get('hourlysalary', 0)
        elif 'hardware' in title and 'engineer' in title:
            return salaries.get('hardwareengineer', {}).get('hourlysalary', 0)
        elif 'mechanical' in title and 'engineer' in title:
            return salaries.get('mechanicalengineer', {}).get('hourlysalary', 0)
        elif 'product' in title and 'design' in title:
            return salaries.get('productdesigner', {}).get('hourlysalary', 0)
        elif 'business' in title and 'analyst' in title:
            return salaries.get('businessanalyst', {}).get('hourlysalary', 0)
        elif 'human' in title and 'resource' in title:
            return salaries.get('humanresources', {}).get('hourlysalary', 0)
        elif 'data' in title and 'scien' in title:
            tist = salaries.get('datascientist', {}).get('hourlysalary', 0)
            science = salaries.get('datascience', {}).get('hourlysalary', 0)
            if tist != 0:
                return tist
            elif science != 0:
                return science
            else:
                return 0
        elif 'quant' in title and 'research' in title:
            return salaries.get('quantitativeresearcher', {}).get('hourlysalary', 0)
        elif 'product' in title and 'manager' in title:
            return salaries.get('productmanager', {}).get('hourlysalary', 0)
        elif 'research' in title:
            return salaries.get('research', {}).get('hourlysalary', 0)
        elif 'tech' in title and 'program' in title and 'manager' in title:
            return salaries.get('technicalprogrammanager', {}).get('hourlysalary', 0)
        elif 'sale' in title:
            return salaries.get('sales', {}).get('hourlysalary', 0)
        elif 'data' in title and 'analy' in title:
            return salaries.get('dataanalyst', {}).get('hourlysalary', 0)
        else:
            return 0