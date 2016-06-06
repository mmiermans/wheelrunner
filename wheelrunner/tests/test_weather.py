import unittest
import sys
from lib.weather import Weather
from forecastio.models import ForecastioDataPoint
from models.user import User
from models.place import DummyPlace

class TestWeather(unittest.TestCase):

    def get_weather_types(self):
        dry = ForecastioDataPoint()
        dry.humidity = 0.5
        dry.visibility = 10
        dry.precipIntensity = 0

        light_rain = ForecastioDataPoint()
        light_rain.humidity = 0.5
        light_rain.visibility = 10
        light_rain.precipIntensity = 0.05

        storm = ForecastioDataPoint()
        storm.humidity = 0.5
        storm.visibility = 10
        storm.precipIntensity = 0.5

        fog = ForecastioDataPoint()
        fog.humidity = 0.5
        fog.visibility = 0.1
        fog.precipIntensity = 0

        humid = ForecastioDataPoint()
        humid.humidity = 0.8
        humid.visibility = 10
        humid.precipIntensity = 0

        return (dry, light_rain, storm, fog, humid)
    
    def test_get_ridability_score(self):
        dry, light_rain, storm, fog, humid = self.get_weather_types()

        weather = Weather()

        light_rain_score = weather.get_ridability_score(light_rain)
        storm_score = weather.get_ridability_score(storm)
        humid_score = weather.get_ridability_score(humid)
        fog_score = weather.get_ridability_score(fog)
        dry_score = weather.get_ridability_score(dry)

        self.assertGreater(dry_score, light_rain_score)
        self.assertGreater(light_rain_score, storm_score)
        self.assertGreater(dry_score, fog_score)
        self.assertGreater(dry_score, humid_score)
        self.assertGreater(humid_score, storm_score)
        self.assertGreater(fog_score, storm_score)

    def test_suggest_time(self):
        place = DummyPlace(37.4418834, -122.1430195)
        weather = Weather()
        user = User(place=place, can_ride_morning=True, frequency=2)
        day, score, weather_score = weather.suggest_time(user)

if __name__ == '__main__':
    unittest.main()
