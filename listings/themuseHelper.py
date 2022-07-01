import re
import json
import requests
from dateutil import parser
from useragent import UserAgent
from listings.listing import Listing 
from locations import english

class MuseHelper(Listing):
    def __init__(self, url, db, currentday, salaries, proxyOn=True, headers=None):
        super().__init__(url=url, db=db, proxyOn=proxyOn, headers=headers)
        self.currentday = currentday
        self.salaries = salaries
    
    def get_listing(self):
        query = json.loads(self.get_raw())
        postings = query.get('results', [])
        for post in postings:
            print('here3')
            name = post.get('name', '').lower()
            filtered = list(filter(None, re.split('(?![\+\#])[\W]', name)))
            print(filtered)
            if Listing.swe_position(filtered):
                print('here4')
                position = Listing.clean_title(filtered)

                locations, is_english = [], False
                for location in post.get('locations', []):
                    names = location.get('name', '')
                    for i in re.split('\W+', names):
                        if i.lower() in english:
                            is_english = True
                    locations.append(location.get('name', ''))
                
                if is_english:
                    print('here5')
                    date = post.get('publication_date', '')
                    if date:
                        date = parser.parse(date)

                    contents = post.get('contents', '')

                    post_id = post.get('id', '')
                    redirect_url = 'https://www.themuse.com/job/redirect/' + str(post_id)
                    post_url = self.get_req(url=redirect_url, headers=self.headers, redirect=False).headers['Location']

                    company_name = post.get('company', {}).get('name', '')
                    pay_per_hour = self.salaries.get(''.join(re.findall('(\w+)', company_name)).lower(), '')

                    posted = self.currentday - date

                    slug = position['position'] + ' ' + position['times'] + ' ' + ' '.join(locations)
                    remove_punc = re.sub('[^A-Za-z0-9\s-]+', '', slug.strip())
                    id = re.sub('[\s]+', '-', remove_punc).lower()

                    self.add_to_database(
                        id = id,
                        name = position['position'], 
                        post_url = post_url, 
                        locations = locations, 
                        date = date, 
                        timeframe = position['times'],
                        contents = contents,
                        currentday = self.currentday,
                        posted = "1 day ago" if posted.days == 1 else str(posted.days) + " days ago",
                        payhour = pay_per_hour
                    )
                    
                    #self.get_favicon(name='espn', url='akunacapital.com')