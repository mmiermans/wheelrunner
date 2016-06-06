import forecastio
import config
from operator import mul
import math
from datetime import timedelta

class Weather(object):

    score_vectors = (
        lambda d: -3*d.humidity + 3,  # relative humidity [0, 1]
        lambda d: 4*d.visibility,  # visibility in miles [0, 10]
        lambda d: -math.log10(d.precipIntensity + 10**-3)/3,  # 0.002 is light precipitation, 0.4 is heavy
    )

    # returns a score in [0, 1] where 1 is great weather
    def get_ridability_score(self, data_point):
        score = 1
        for score_vector in self.score_vectors:
            try:
                score *= max(0, min(1, score_vector(data_point)))
            except forecastio.utils.PropertyUnavailable:
                pass
        return score

    # returns a score depending on how close day is to ideal_day
    def get_day_score(self, day, ideal_day):
        return max(0.7, 1 - 0.1*abs((day - ideal_day).days))

    # TODO: only recommend future dates
    # TODO: use the morning/evening info from user
    # TODO: use hourly weather data where available
    def suggest_time(self, user):
        place = user.place
        forecast = forecastio.load_forecast(config.forecastio['api_key'], place.lat, place.lng)
        data_block = forecast.daily()

        ideal_next_ride = user.last_ride + timedelta(7 / user.frequency)
        best_date = None
        best_score = 0
        best_day_weather = 0
        for data_point in data_block.data:
            ridability_score = self.get_ridability_score(data_point)
            day_score = self.get_day_score(data_point.time.date(), ideal_next_ride)
            score = ridability_score * day_score
            if score > best_score:
                best_date = data_point.time.date()
                best_score = score
                best_day_weather = ridability_score
        return (best_date, best_score, best_day_weather)
