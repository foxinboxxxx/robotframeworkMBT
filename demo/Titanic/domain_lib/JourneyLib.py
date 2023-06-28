#!/usr/bin/env python3
from time import sleep

from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword

from datetime import datetime, timedelta

from domain_lib.MapAnimation import map_animation
from domain_lib.MapLib import MapLib
from simulation.iceberg import Iceberg
from simulation.titanic_in_ocean import TitanicInOcean
from simulation.journey import Journey

class JourneyLib:
    _journey = None

    def __init__(self):
        self.builtin = BuiltIn()
        self.call_count = 0

    @property
    def journey(self) -> Journey:
        if not self._journey:
            self._journey = Journey(self.map_lib.ocean)
        return self._journey

    @property
    def map_lib(self) -> MapLib:
        return self.builtin.get_library_instance("MapLib")

    @keyword("Start Journey on ${date}")
    def start_journey(self, date: str):
        date = datetime.strptime(date, "%Y-%m-%d")
        self.journey.start_date = date
        self.builtin.log(f"The journey has started at {self.journey.start_date.strftime('%Y-%m-%d')}")

    @keyword("Current date of Journey")
    def journey_ondate(self):
        current_date = self.journey.start_date + timedelta(minutes=self.journey.time_in_journey)
        return current_date.strftime('%Y-%m-%d')

    @keyword("play out Journey for a duration of ${minutes} minutes")
    def pass_time(self, minutes: int):
        """
        Progresses the journey by an x amount of minutes
        @param minutes: amount of minutes to progress the journey with.
        """
        self.journey.passed_time(minutes)
        if self.call_count % 100 == 0:
            map_animation.update_floating_objects()
        self.call_count += 1

    @keyword("Move Titanic out of current area")
    def move_titanic_out_of_current_area(self):
        titanic = TitanicInOcean.instance
        current_area = self.builtin.run_keyword("Area of location Titanic's position")
        self.builtin.log(f"Titanic moving out of {current_area}")
        while (new_area := self.map_lib.get_area_of_location(titanic)) == current_area:
            if not titanic.speed > 0:
                self.builtin.log(f"Titanic not moving. Still in area {new_area}")
                break
            self.pass_time(1)
            if titanic.fell_off_the_earth():
                raise Exception("Titanic at least did not sink. But where did it go?")
        else:
            self.builtin.log(f"Titanic moved into {new_area}")
        map_animation.update_floating_objects()
        print(titanic.longitude, titanic.latitude)


# Continue with the main thread...

#
# import matplotlib.pyplot as plt
# from matplotlib.patches import Rectangle
#
#
# def draw_current_situation():
#     ocean = MapLib.ocean
#     floating_objects = ocean.floating_objects
#
#     # Create a new figure
#     fig, ax = plt.subplots()
#
#     # Plot the areas as squares
#     for area_name in MapLib.areas:
#         area = MapLib.areas[area_name]
#         width = abs(area.upper_left_bound.longitude - area.lower_right_bound.longitude)
#         height = abs(area.upper_left_bound.latitude - area.lower_right_bound.latitude)
#         rect = Rectangle((area.lower_right_bound.latitude, area.upper_left_bound.longitude), height, width, alpha=0.4)
#         ax.add_patch(rect)
#         ax.annotate(area_name, (area.lower_right_bound.latitude, area.upper_left_bound.longitude), color='black')
#
#     # Plot the locations
#     for location_name in MapLib.locations:
#         location = MapLib.locations[location_name]
#         ax.plot(location.latitude, location.longitude, 'ro', label=location_name)
#
#     # Plot the floating objects
#     for obj in floating_objects:
#         if isinstance(obj, TitanicInOcean):
#             ax.plot(obj.latitude, obj.longitude, 'bs', label='Titanic')
#         elif isinstance(obj, Iceberg):
#             ax.plot(obj.latitude, obj.longitude, 'c^', label='Iceberg')
#
#     # Set the Atlantic area bounds
#     atlantic_area = MapLib.atlantic_area
#     width = abs(atlantic_area.upper_left_bound.longitude - atlantic_area.lower_right_bound.longitude)
#     height = abs(atlantic_area.upper_left_bound.latitude - atlantic_area.lower_right_bound.latitude)
#     rect = Rectangle((atlantic_area.lower_right_bound.latitude, atlantic_area.upper_left_bound.longitude), height, width, linestyle='--', edgecolor='g', facecolor='none')
#     ax.add_patch(rect)
#     ax.annotate('Atlantic Area', (atlantic_area.lower_right_bound.latitude, atlantic_area.upper_left_bound.longitude), color='g')
#
#     # Set the plot title and labels
#     ax.set_title('Current Situation')
#     ax.set_xlabel('Latitude')
#     ax.set_ylabel('Longitude')
#
#     # Add a legend
#     ax.legend()
#
#     # Set aspect ratio and adjust plot limits
#     aspect_ratio = 1.0  # Adjust as needed
#     x_margin = 0.1  # Adjust as needed
#     y_margin = 0.1  # Adjust as needed
#     ax.set_aspect(aspect_ratio)
#     ax.set_xlim(ax.get_xlim()[0] - x_margin, ax.get_xlim()[1] + x_margin)
#     ax.set_ylim(ax.get_ylim()[0] - y_margin, ax.get_ylim()[1] + y_margin)
#
#     # Show the plot
#     plt.show()