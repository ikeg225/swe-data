from bs4 import BeautifulSoup
from locations import places
import requests
import re

class Listing:
    def __init__(self, url, headers):
        self.posting = BeautifulSoup(requests.get(url, headers=headers).content, 'lxml')
        #print(self.posting)
        self.url = url
        self.baseurl = re.match('^https?:\/\/[^#?\/]+', url)[0]
    
    @staticmethod
    def clean_title(title):
        time = set(['summer', 'fall', 'winter', 'spring'])
        upper = set(['ios', 'ui'])
        new_title, locations, times = [], [], []
        for word in title:
            if word in time or word.isnumeric() or word in places:
                if word in places:
                    locations.append(word.capitalize())
                else:
                    times.append(word.capitalize())
            else:
                if word in upper:
                    new_title.append(word.upper())
                else:
                    new_title.append(word.capitalize())
                
        return { "position": ' '.join(new_title), "locations": ','.join(locations), "times": ' '.join(times) }
    
    @staticmethod
    def swe_position(title):
        intern_check, field_check = False, False
        intern_keywords = set(['intern', 'internship'])
        field_keywords = set(['software', 'data', 'trading', 'trade', 'web', 'development', 'python', 'java', 'javascript', 'ruby',
        'user', 'interface', 'quantitative', 'full', 'stack', 'front', 'end', 'back', 'react', 'swift', 'ios', 'engineer',
        'engineering', 'technology', 'android', 'analyst', 'c++', 'c#'])
        for word in title:
            if word in field_keywords:
                field_check = True
            elif word in intern_keywords:
                intern_check = True
            if intern_check and field_check:
                return True
        return False

    def get_listing(self):
        urls = set()
        for url in self.posting.find_all('a', href=True):
            title = url.get_text().strip().lower().replace("\n", " ")
            filtered = list(filter(None, re.split('(?![\+\#])[\W]', title)))
            if Listing.swe_position(filtered):
                position = Listing.clean_title(filtered)
                urls.add((self.add_base_url(url.get('href')), position["position"], position["locations"], position["times"]))
        return urls
    
    def add_base_url(self, slug):
        if not self.baseurl in slug:
            slug = self.baseurl + slug
        return slug