#!/usr/bin/env python3

from system.titanic import Titanic
from simulation.iceberg import Iceberg
from simulation.titanic_in_ocean import TitanicInOcean
from simulation.journey import Journey
from simulation.ocean import Ocean
from robot.api.deco import keyword


class JourneyLib:
    def __init__(self):
        self.ocean = Ocean()
        self.journey = Journey(self.ocean)

    @keyword("Spawn titanic at coordinate long ${n} lat ${w} heading ${heading} at speed of ${speed} knots")
    def spawn_titanic(self, long: float, lat: float, heading: str, speed: float):
        """
        Spawns the titanic with given parameters
        @param long: longitude of titanic
        @param lat: latitude of titanic
        @param heading: heading of the titanic (east, west, south, north)
        @param speed: speed in knots of the titanic
        """
        headings = {
            "north": 0,
            "east": 90,
            "south": 180,
            "west": 270,
        }
        t = Titanic(speed, steering_direction=0)
        tio = TitanicInOcean(t, long, lat, speed, headings[heading])
        self.ocean.floating_objects.append(tio)

    @keyword("Spawn iceberg at coordinate long ${long} lat ${lat}")
    def spawn_iceberg(self, long: float, lat: float):
        """
        Spawns an iceberg with given parameters
        @param long: longitude of iceberg
        @param lat: latitude of iceberg
        """
        iceberg = Iceberg(long, lat)
        self.ocean.floating_objects.append(iceberg)

    @keyword("play out Journey for a duration of ${minutes} minutes")
    def pass_time(self, minutes: int):
        """
        Progresses the journey by an x amount of minutes
        @param minutes: amount of minutes to progress the journey with.
        """
        self.journey.passed_time(minutes)
