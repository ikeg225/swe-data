from listings.listing import Listing
from listings.greenhouseListing import GreenHouse
from listings.apiListing import API

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}
listing = GreenHouse(url="https://boards.greenhouse.io/grindr", headers=headers)
listing = listing.get_listing()
print(listing)
print(len(listing))