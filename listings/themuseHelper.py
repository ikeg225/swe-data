import re
import json
import requests
from levels import Levels
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
            name = post.get('name', '').lower()
            filtered = list(filter(None, re.split('(?![\+\#])[\W]', name)))
            if Listing.swe_position(filtered):
                position = Listing.clean_title(filtered)

                locations, is_english = [], False
                for location in post.get('locations', []):
                    names = location.get('name', '')
                    for i in re.split('\W+', names):
                        if i.lower() in english:
                            is_english = True
                    locations.append(location.get('name', ''))
                
                if is_english:
                    date = post.get('publication_date', '')
                    if date:
                        date = parser.parse(date)

                    contents = post.get('contents', '')

                    post_id = post.get('id', '')
                    redirect_url = 'https://www.themuse.com/job/redirect/' + str(post_id)
                    post_url = self.get_req(url=redirect_url, headers=self.headers, redirect=False).headers['Location']
                    main_url = re.findall('^https?:\/\/([^#?\/]+)', post_url)[0]

                    posted = self.currentday - date

                    slug = position['position'] + ' ' + position['times'] + ' ' + ' '.join(locations)
                    remove_punc = re.sub('[^A-Za-z0-9\s-]+', '', slug.strip())
                    id = re.sub('[\s]+', '-', remove_punc).lower()

                    name = position['position']
                    company_name = post.get('company', {}).get('name', '')
                    company_short = ''.join(re.findall('(\w+)', company_name)).lower()
                    pay_per_hour = self.salaries.get(company_short, 0)
                    if pay_per_hour != 0:
                        pay_per_hour = Levels.get_job_key(title=name, salaries=pay_per_hour)
                    
                    self.add_to_database(
                        id = id,
                        company=company_name,
                        company_short=company_short,
                        main_url=main_url,
                        name = name, 
                        post_url = post_url, 
                        locations = locations, 
                        date = date.strftime('%m/%d/%Y'), 
                        timeframe = position['times'],
                        contents = contents,
                        currentday = self.currentday.strftime('%m/%d/%Y'),
                        posted = "1 day ago" if posted.days == 1 else str(posted.days) + " days ago",
                        posted_num = posted.days,
                        payhour = pay_per_hour
                    )
                    
                    self.add_company(
                        company=company_name,
                        company_short=company_short,
                        main_url=main_url
                    )