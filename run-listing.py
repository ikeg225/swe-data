from listings.apiListing import API
from listings.listing import Listing
from listings.greenhouseListing import GreenHouse
from listings.themuseListing import TheMuse
from pymongo_test_insert import get_database

db = get_database()

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

#muse = TheMuse(db=db, proxyOn=False, headers=headers)
#rint(muse.get_urls())

#listing = Listing(url="https://akunacapital.com/careers?experience=intern&search_term=#careers", proxyOn=False, headers=headers)
#listing = listing.get_listing()
#print(listing)
#print(len(listing))