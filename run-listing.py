from listings.apiListing import API
from listings.listing import Listing
from listings.greenhouseListing import GreenHouse


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

listing = Listing(url="http://whatsmyuseragent.org/", proxyOn=False, headers=headers)
print(listing.get_posting())
#listing = listing.get_listing()
#print(listing)
#print(len(listing))