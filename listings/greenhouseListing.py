from listings.listing import Listing
import re

class GreenHouse(Listing):
    def __init__(self, url, db, proxyOn=True, headers=None):
        super().__init__(url=url, db=db, proxyOn=proxyOn, headers=headers)
    
    def get_listing(self):
        urls = set()
        for url in self.posting.find_all('div', {'class': 'opening'}):
            title = url.a.get_text().strip().lower().replace("\n", " ")
            filtered = list(filter(None, re.split('(?![\+\#])[\W]', title)))
            if GreenHouse.swe_position(filtered):
                position = GreenHouse.clean_title(filtered)
                urls.add((self.add_base_url(url.a['href']), position["position"], url.span.get_text(), position["times"]))
        return urls