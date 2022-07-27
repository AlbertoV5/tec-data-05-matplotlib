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
    # ax.legend()
    legend = ax.legend(fontsize="12", mode="Expanded",
         scatterpoints=1, loc="best", title="City Type")
    for lg in legend.legendHandles:
        lg._sizes = [75]
    legend.get_title().set_fontsize(12)
    return ax

# %%
# Plots
figures = {
    typ: plt.figure(figsize=(8,5)) for i in range(0,3)
    for typ in TYPE
}
colors = ["coral", "skyblue", "gold"]
text_kwargs = {
    "x": 0.92, "y":0.5, 
    "s": "Note: Circle size\ncorrelates with\ndriver per country.", 
    "fontsize": 10,
    "horizontalalignment":'left',
    "verticalalignment":'center', 
    "bbox":dict(facecolor='white', alpha=0.7)
}
for typ, color in zip(figures, colors):
    create_bubble_chart(figures[typ].add_subplot(111), typ, color)
    figures[typ].text(**text_kwargs)
    figures[typ].savefig(f"ridesharing_{typ}.jpeg", dpi=300, bbox_inches='tight')

# %%
# Combined plot
fig = plt.figure(figsize=(8,5))
ax1 = fig.add_subplot(111)
for typ, color in zip(TYPE, colors):
    ax = create_bubble_chart(ax1, typ, color)
fig.text(**text_kwargs)
fig.savefig(f"ridesharing.jpeg", dpi=300, bbox_inches='tight')
