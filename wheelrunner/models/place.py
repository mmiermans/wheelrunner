class Place(object):

    def __init__(self, data):
        self.data = data

    @property
    def lat(self):
        return self.data['geometry']['location']['lat']

    @property
    def lng(self):
        return self.data['geometry']['location']['lng']

    def __repr__(self):
        return self.data['formatted_address']


class DummyPlace(object):
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
