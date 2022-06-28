import json
import concurrent.futures
from listings.listing import Listing 
from listings.themuseHelper import MuseHelper 

class TheMuse:
    def __init__(self, db, proxyOn=True, headers=None):
        self.url = "https://www.themuse.com/api/public/jobs?category=Data%20and%20Analytics&category=Data%20Science&category=Mechanic&category=Science%20and%20Engineering&category=Software%20Engineer&category=Software%20Engineering&level=Internship&page=1"
        self.proxyOn = proxyOn
        self.headers = headers
        self.urls = []
        first_page = json.loads(Listing(self.url, proxyOn, headers).get_raw())
        for i in range(1, first_page["page_count"]):
            self.urls.append(self.url[:-1] + str(i))
        self.db = db
    
    def extract(self, url):
        MuseHelper(url=url, db=self.db, proxyOn=self.proxyOn, headers=self.headers)
        return

    def run_all(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.extract, self.urls)
        return

    def get_urls(self):
        return self.urls