from levels import Levels
from listings.apiListing import API
from listings.listing import Listing
from listings.themuseListing import TheMuse
from typesense_actions import TypesenseActions
from listings.greenhouseListing import GreenHouse

level = Levels()
salaries = level.sort_json()
typesense = TypesenseActions()

muse = TheMuse(db=typesense.client, salaries=salaries, proxyOn=True)
muse.run_all()

#listing = Listing(url="https://akunacapital.com/careers?experience=intern&search_term=#careers", db=None, proxyOn=False, headers=headers)
#listing = listing.get_listing()
#print(listing)
#print(len(listing))

#key = client.keys.create({
#  "description": "Sports Quiz Key",
#  "actions": ["*"],
#  "collections": ["quizzes"]
#})

#headers = {
#    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
#}