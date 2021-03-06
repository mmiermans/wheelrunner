import config
import time
import requests
from models.place import Place

class Geocoding(object):
    
    def __init__(self):
        self.cache = dict()

    def get_place(self, query):
        # normalize query
        query = query.lower().strip()

        # try to use cache first
        if query in self.cache:
            return self.cache[query]

        # use Google Geocoding API
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(
            query, config.google['server_key'])
        r = requests.get(url)
        data = r.json()
        results = data.get('results')
        if results:
            result = results[0]
            self.cache[query] = place = Place(result)
            return place

# singleton
geocoder = Geocoding()
