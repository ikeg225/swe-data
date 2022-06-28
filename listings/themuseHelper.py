import re
import json
import requests
from dateutil import parser
from useragent import UserAgent
from listings.listing import Listing 

class MuseHelper(Listing):
    def __init__(self, url, db, proxyOn=True, headers=None):
        super().__init__(url=url, db=db, proxyOn=proxyOn, headers=headers)
    
    def get_listing(self):
        query = json.loads(self.get_raw())
        postings = query.get('results', [])
        for post in postings:
            name = post.get('name', '')
            filtered = list(filter(None, re.split('(?![\+\#])[\W]', name)))
            if Listing.swe_position(filtered):
                position = Listing.clean_title(filtered)

                locations = []
                for location in post.get('locations', []):
                    locations.append(location.get('name', ''))

                date = post.get('publication_date', '')
                if date:
                    date = parser.parse(date)
                
                id = post.get('id', '')
                redirect_url = 'https://www.themuse.com/job/redirect/' + id
                post_url = self.get_req(url=redirect_url, headers=self.headers, redirect=False).headers['Location']
                base_url = re.match('^https?:\/\/([^#?\/]+)', post_url)[0]

                self.add_to_database(name=position['position'], base_url=base_url, post_url=post_url, locations=locations, date=date, timeframe=position['times'])