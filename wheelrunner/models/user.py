from datetime import date, timedelta

class User(object):

    def __init__(self, place=None, can_ride_evening=False, can_ride_morning=False, frequency=1):
        self.place = place
        self.can_ride_morning = can_ride_morning
        self.can_ride_evening = can_ride_evening
        self.frequency = frequency
        self.last_ride = date.today() - timedelta(2)
