import unittest
import sys
from lib.geocoding import geocoder

class TestGeocoding(unittest.TestCase):
    
    def test_get_place(self):
        def assertLatLng(place):
            self.assertEqual(place.lat, 37.4418834)
            self.assertEqual(place.lng, -122.1430195)
        
        assertLatLng(geocoder.get_place('palo alto'))
        # using cache:
        assertLatLng(geocoder.get_place('palo alto'))


if __name__ == '__main__':
    unittest.main()
