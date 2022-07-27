# %%
from collections import namedtuple
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

resources = Path("resources")
city_data_df = pd.read_csv(resources / "city_data.csv")
ride_data_df = pd.read_csv(resources / "ride_data.csv")

# Declare Constants
COL = namedtuple(
    "Columns", "CITY TYPE FARE DRIVERS RIDE",
    defaults=["city", "type", "fare", "driver_count", "ride_id"]
)()
TYPE = namedtuple(
    "CityTypes", "URBAN SUBURBAN RURAL", 
    defaults=["Urban", "Suburban", "Rural"]
)()

# Merge data
pyber_data_df = city_data_df.merge(ride_data_df, on=[COL.CITY, COL.CITY]).set_index(COL.CITY)

# Separate data per city type and group by city
type_groups = {
    typ: pyber_data_df[pyber_data_df[COL.TYPE] == typ].groupby([COL.CITY])
    for typ in TYPE
}
def get_count_by_city_by_type(col: str) -> dict:
    """Return dictionary of city types with values of
    series of counts of specified column."""
    return {typ: type_groups[typ].count()[col] for typ in type_groups}
            
def get_average_by_city_by_type(col: str) -> dict:
    """Return dictionary of city types with values of
    series of averages of specified column."""
    return {typ: type_groups[typ].mean()[col] for typ in type_groups}

# Per City Type
ride_count = get_count_by_city_by_type(COL.RIDE)
fare_average = get_average_by_city_by_type(COL.FARE)
drivers_average = get_average_by_city_by_type(COL.DRIVERS)

def create_bubble_chart(ax: plt.Axes, city_type: str, color: str):
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
    ax.legend()
    return ax

# %%
# Plots
# Urban
urban_fig = plt.figure(figsize=(8,5))
create_bubble_chart(urban_fig.add_subplot(111), TYPE.URBAN, "coral", save=True)
urban_fig.savefig("ridesharing_urban.png", dpi=144)
# Suburban
suburban_fig = plt.figure(figsize=(8,5))
create_bubble_chart(suburban_fig.add_subplot(111), TYPE.SUBURBAN, "skyblue", save=True)
suburban_fig.savefig("ridesharing_suburban.png", dpi=144)
# Rural
rural_fig = plt.figure(figsize=(8,5))
create_bubble_chart(rural_fig.add_subplot(111), TYPE.RURAL, "gold", save=True)
rural_fig.savefig("ridesharing_rural.png", dpi=144)

# %%
fig = plt.figure(figsize=(8,5))
ax1 = fig.add_subplot(111)
create_bubble_chart(ax1, TYPE.URBAN, "coral")
create_bubble_chart(ax1, TYPE.SUBURBAN, "skyblue")
create_bubble_chart(ax1, TYPE.RURAL, "gold")
fig.savefig(f"ridesharing.png", dpi=144)
