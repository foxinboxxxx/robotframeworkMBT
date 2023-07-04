import numpy as np

try:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
except ModuleNotFoundError:
    # Fallback in case matplotlib does not exist
    import sys

    class MapAnimation:
        def plot_static_elements(self):
            pass

        def update_floating_objects(self):
            pass

    # Create the empty MapAnimation instance
    map_animation = MapAnimation()
    sys.exit(0)

from simulation.iceberg import Iceberg
from simulation.titanic_in_ocean import TitanicInOcean


class MapAnimation:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.plot_initialized = False

    def plot_static_elements(self, areas, locations):
        # Plot the areas as squares
        for area_name, area in areas.items():
            width = abs(area.upper_left_bound.longitude - area.lower_right_bound.longitude)
            height = abs(area.upper_left_bound.latitude - area.lower_right_bound.latitude)
            rect = Rectangle((area.lower_right_bound.latitude, area.upper_left_bound.longitude), height, width, alpha=0.4)
            self.ax.add_patch(rect)
            self.ax.annotate(area_name, (area.lower_right_bound.latitude, area.upper_left_bound.longitude), color='black')

        # Plot the locations
        colors = [
            'ro',
            'bo',
            'go',
            'mo',
            'r*',
            'b*',
            'g*',
            'm*',
        ]
        ci = 0
        for location_name, location in locations.items():
            self.ax.plot(location.latitude, location.longitude, colors[ci % len(colors)], label=location_name)
            ci += 1

        # # Set the Atlantic area bounds atlantic_area = MapLib.atlantic_area width = abs(
        # atlantic_area.upper_left_bound.longitude - atlantic_area.lower_right_bound.longitude) height = abs(
        # atlantic_area.upper_left_bound.latitude - atlantic_area.lower_right_bound.latitude) rect = Rectangle((
        # atlantic_area.lower_right_bound.latitude, atlantic_area.upper_left_bound.longitude), height, width,
        # linestyle='--', edgecolor='g', facecolor='none') self.ax.add_patch(rect) self.ax.annotate('Atlantic Area',
        # (atlantic_area.lower_right_bound.latitude, atlantic_area.upper_left_bound.longitude), color='g')

        # Set the plot title and labels
        self.ax.set_title('Current Situation')
        self.ax.set_xlabel('Latitude')
        self.ax.set_ylabel('Longitude')

        # Add a legend
        self.ax.legend()

        # Show the plot
        if not self.plot_initialized:
            plt.ion()
            plt.show(block=False)
            self.plot_initialized = True
        else:
            plt.draw()
            plt.pause(0.001)

    def update_floating_objects(self, floating_objects):

        # Clear the floating objects plot
        for artist in self.ax.lines:
            if isinstance(artist.get_gid(), str) and 'floating_object' in artist.get_gid():
                artist.remove()
        # Clear the floating objects plot
        for artist in self.ax.texts:
            if isinstance(artist.get_gid(), str) and 'floating_object' in artist.get_gid():
                artist.remove()

        # Plot the floating objects
        for obj in floating_objects:
            if isinstance(obj, TitanicInOcean):# Set the rotation angle in degrees
                angle_degrees = obj.direction

                # Convert angle to radians
                angle_radians = np.deg2rad(angle_degrees)
                aspect_ratio = self.ax.get_data_ratio()

                # Compute the arrow components
                dx = np.sin(angle_radians)
                dy = np.cos(angle_radians)

                # Draw the arrow
                self.ax.annotate("", xy=(obj.latitude + dx, obj.longitude + dy), xytext=(obj.latitude, obj.longitude),
                    arrowprops=dict(arrowstyle="->"), gid='floating_object')

                if obj.sunk:
                    icon = 'rs'  # red square
                else:
                    icon = 'ys'  # yellow square
                    # Draw the arrow
                    self.ax.annotate("", xy=(obj.latitude + dx, obj.longitude + dy), xytext=(obj.latitude, obj.longitude),
                        arrowprops=dict(arrowstyle='->'), gid='floating_object')
                self.ax.plot(obj.latitude, obj.longitude, icon, label='Titanic', gid='floating_object')
            elif isinstance(obj, Iceberg):
                self.ax.plot(obj.latitude, obj.longitude, 'c^', label='Iceberg', gid='floating_object')

        # Redraw the plot
        plt.draw()
        plt.pause(0.001)


# Create the MapAnimation instance
map_animation = MapAnimation()
