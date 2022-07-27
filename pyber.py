# %%
# Setup cell to define dataframes and functions
from collections import namedtuple
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import scipy.stats as sts

resources = Path("resources")
city_data_df = pd.read_csv(resources / "city_data.csv")
ride_data_df = pd.read_csv(resources / "ride_data.csv")

# Declare Constants
COL = namedtuple(
    "Columns", "CITY TYPE FARE DRIVERS RIDE",
    defaults=["city", "type", "fare", "driver_count", "ride_id"]
)()
CITY_TYPES = namedtuple(
    "CityTypes", "URBAN SUBURBAN RURAL", 
    defaults=["Urban", "Suburban", "Rural"]
)()

# Merge data
pyber_data_df = city_data_df.merge(ride_data_df, on=[COL.CITY, COL.CITY]).set_index(COL.CITY)

# Separate data per city type and group by city
city_types_dict = {
    typ: pyber_data_df[pyber_data_df[COL.TYPE] == typ]
    for typ in CITY_TYPES
}
def get_count_by_city_by_type(col: str) -> dict:
    """Return dictionary of city types with values of
    series of counts of specified column."""
    return {typ: city_types_dict[typ].groupby([COL.CITY]).count()[col] for typ in city_types_dict}
            
def get_average_by_city_by_type(col: str) -> dict:
    """Return dictionary of city types with values of
    series of averages of specified column."""
    return {typ: city_types_dict[typ].groupby([COL.CITY]).mean()[col] for typ in city_types_dict}

# Per City Type
ride_count = get_count_by_city_by_type(COL.RIDE)
fare_average = get_average_by_city_by_type(COL.FARE)
fares = {typ: city_types_dict[typ][COL.FARE] for typ in CITY_TYPES}
drivers = {typ: city_types_dict[typ][COL.DRIVERS] for typ in CITY_TYPES}
drivers_average = get_average_by_city_by_type(COL.DRIVERS)

def create_bubble_chart(ax: plt.Axes, city_type: str, color: str) -> plt.Axes:
    """
    Generate a scatter-bubble chart in the specified axis.
    This depends on previously made dictionaries where
    the key is city type and the value is a pandas series.

    Each pandas series will contain the data for the x, y, s
    scatter plot arguments.

    Args:
        ax (plt.Axes): Axis on which to generate the plot.
        city_type (str): Key for dictionary.
        color (str): Chosen color for this plot.

    Returns:
        plt.Axes: The same axis reference.
    """
    ax.scatter(
        ride_count[city_type], 
        fare_average[city_type],
        s=10*drivers_average[city_type],
        color=color,
        linewidths=1,
        edgecolors="k",
        alpha=0.8,
        label=city_type
    )
    ax.set_title("PyBer Ride-Sharing Data (2019)")
    ax.set_xlabel("Total Number of Rides (Per City)")
    ax.set_ylabel("Average Fare ($)")
    ax.grid(True)
    legend = ax.legend(fontsize="12", mode="Expanded",
         scatterpoints=1, loc="best", title="City Type")
    for lg in legend.legendHandles:
        lg._sizes = [75]
    legend.get_title().set_fontsize(12)
    return ax

colors = ["coral", "skyblue", "gold"]
text_kwargs = {
    "x": 0.92, "y":0.5, 
    "s": "Note: Circle size\ncorrelates with\ndriver per country.", 
    "fontsize": 10,
    "horizontalalignment":'left',
    "verticalalignment":'center', 
    "bbox":dict(facecolor='white', alpha=0.7)
}

# %%
# Creating multiple figures to save various plots.
# Each figure uses a different city type and color.
# We create a new axis per figure everytime, add text to it
# and finally save to disk.
figures = {
    typ: plt.figure(figsize=(8,5)) for i in range(0,3)
    for typ in CITY_TYPES
}
for typ, color in zip(figures, colors):
    create_bubble_chart(figures[typ].add_subplot(111), typ, color)
    figures[typ].text(**text_kwargs)
    figures[typ].savefig(f"ridesharing_{typ}.jpeg", dpi=300, bbox_inches='tight')

# %%
# Generating multiple plots in the same axis,
# The variatons are city types and colors.
# Once created, write text to figure and save.
fig = plt.figure(figsize=(8,5))
ax = fig.add_subplot(111)
for typ, color in zip(CITY_TYPES, colors):
    create_bubble_chart(ax, typ, color)
fig.text(**text_kwargs)
fig.savefig(f"ridesharing.jpeg", dpi=300, bbox_inches='tight')

# %%
# Creating Box and Whisker

def get_params(func):
    def wrapped(dataset):
        return pd.DataFrame({param: func(dataset, method)
                for param, method in zip(
                    ["mean", "median", "mode"],
                    [np.mean, np.median, sts.mode])})
    return wrapped
    
@get_params
def get_stats_from(dataset, func):
    return {city_type: func(dataset[city_type])
        for city_type in CITY_TYPES}

ride_count_stats = get_stats_from(ride_count)
fare_stats = get_stats_from(fares)
drivers_stats = get_stats_from(drivers)
drivers_stats