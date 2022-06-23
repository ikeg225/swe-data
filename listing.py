from bs4 import BeautifulSoup
import requests
import re

class Listing:
    def __init__(self, url, headers):
        self.posting = BeautifulSoup(requests.get(url, headers=headers).content, 'lxml')
        print(self.posting)
        self.url = url
    
    @staticmethod
    def clean_title(title):
        remove = set(['summer', 'fall', 'winter', 'spring'])
        return ' '.join([word.capitalize() for word in title if not (word in remove or word.isnumeric())])
    
    @staticmethod
    def swe_position(title):
        intern_check, field_check = False, False
        intern_keywords = set(['intern', 'internship'])
        field_keywords = set(['software', 'data', 'trading', 'trade', 'web', 'development', 'python', 'java', 'javascript', 'ruby',
        'user', 'interface', 'quantitative', 'full', 'stack', 'front', 'end', 'back', 'react', 'swift', 'ios', 'engineer',
        'engineering', 'technology', 'android', 'analyst'])
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
            filtered = list(filter(None, re.split('\W+', title)))
            if Listing.swe_position(filtered):
                position = Listing.clean_title(filtered)
                urls.add((url.get('href'), position))
        return urls

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}
listing = Listing(url="https://boards.greenhouse.io/bridgewater89", headers=headers)
lis = listing.get_listing()
print(lis)
print(len(lis))