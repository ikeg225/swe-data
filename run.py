import os
import typesense
from levels import Levels
from dotenv import load_dotenv
from listings.apiListing import API
from listings.listing import Listing
from listings.greenhouseListing import GreenHouse
from listings.themuseListing import TheMuse

load_dotenv()
level = Levels()
salaries = level.sort_json()


#client = typesense.Client({
#  'nodes': [{
#    'host': os.getenv("TYPESENSE_HOST"),
#    'port': os.getenv("PORT"),
#    'protocol': 'http'
#  }],
#  'api_key': os.getenv("TYPESENSE_API"),
#  'connection_timeout_seconds': 2
#})

#schema = {
#  "name": "postings",  
#  "fields": [
#    {"name": ".*", "type": "auto" }
#  ]
#}

#client.collections.create(schema)

#db = get_database()


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

#muse = TheMuse(db=None, salaries=salaries, proxyOn=False, headers=headers)
#muse.run_all()

#listing = Listing(url="https://akunacapital.com/careers?experience=intern&search_term=#careers", db=None, proxyOn=False, headers=headers)
#listing = listing.get_listing()
#print(listing)
#print(len(listing))

#key = client.keys.create({
#  "description": "Sports Quiz Key",
#  "actions": ["*"],
#  "collections": ["quizzes"]
#})