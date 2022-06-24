from listings.listing import Listing

class API(Listing):
    def __init__(self, url, headers):
        super().__init__(url=url, headers=headers)
    
    def get_listing(self):
        urls = set()
        return urls