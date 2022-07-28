# %%
# Setup dataframes and functions
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as sts
import matplotlib as mpl
from pathlib import Path
from collections import namedtuple


resources = Path("resources")
output_path = Path("analysis")
city_data_df = pd.read_csv(resources / "city_data.csv")
ride_data_df = pd.read_csv(resources / "ride_data.csv")

# Declare Constants
COL = namedtuple(
    "Columns",
    "CITY TYPE FARE DRIVERS RIDE",
    defaults=["city", "type", "fare", "driver_count", "ride_id"],
)()
CITY_TYPES = namedtuple(
    "CityTypes",
    "URBAN SUBURBAN RURAL",
    defaults=[
        "Urban",
        "Suburban",
        "Rural",
    ],
)()

# Merge data
pyber_data_df = city_data_df.merge(ride_data_df, on=[COL.CITY, COL.CITY]).set_index(
    COL.CITY
)

# Separate data per city type and group by city
city_types_dict = {
    typ: pyber_data_df[pyber_data_df[COL.TYPE] == typ] for typ in CITY_TYPES
}


def get_count_by_city_by_type(col: str) -> dict:
    """Return dictionary of city types with values of
    series of counts of specified column."""
    return {
        typ: city_types_dict[typ].groupby([COL.CITY]).count()[col]
        for typ in city_types_dict
    }


def get_average_by_city_by_type(col: str) -> dict:
    """Return dictionary of city types with values of
    series of averages of specified column."""
    return {
        typ: city_types_dict[typ].groupby([COL.CITY]).mean()[col]
        for typ in city_types_dict
    }


# Per City Type
ride_count = get_count_by_city_by_type(COL.RIDE)
fares = {typ: city_types_dict[typ][COL.FARE] for typ in CITY_TYPES}
drivers = {typ: city_types_dict[typ][COL.DRIVERS] for typ in CITY_TYPES}
fare_average = get_average_by_city_by_type(COL.FARE)
drivers_average = get_average_by_city_by_type(COL.DRIVERS)


# %%
# Create all the Bubble Plots.
def plot_bubble_chart(ax: plt.Axes, city_type: str, color: str) -> plt.Axes:
    """
    Generate a scatter-bubble chart.
    This depends on previously made dictionaries where
    the key is city type and the value is a pandas series.
    """
    ax.scatter(
        ride_count[city_type],
        fare_average[city_type],
        s=10 * drivers_average[city_type],
        color=color,
        linewidths=1,
        edgecolors="k",
        alpha=0.8,
        label=city_type,
    )
    ax.set_title("PyBer Ride-Sharing Data (2019)")
    ax.set_xlabel("Total Number of Rides (Per City)")
    ax.set_ylabel("Average Fare ($)")
    ax.grid(True)
    legend = ax.legend(
        fontsize="12", mode="Expanded", scatterpoints=1, loc="best", title="City Type"
    )
    for lg in legend.legendHandles:
        lg._sizes = [75]
    legend.get_title().set_fontsize(12)
    return ax


# Setup common arguments
colors = ["coral", "skyblue", "gold"]
text_arguments = {
    "x": 0.92,
    "y": 0.5,
    "s": "Note: Circle size\ncorrelates with\ndriver per country.",
    "fontsize": 10,
    "horizontalalignment": "left",
    "verticalalignment": "center",
    "bbox": dict(facecolor="white", alpha=0.7),
}
# Individual Plots
for typ, color in zip(CITY_TYPES, colors):
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111)
    plot_bubble_chart(ax, typ, color)
    fig.text(**text_arguments)
    fig.savefig(output_path / f"ridesharing_{typ}.jpeg", dpi=300, bbox_inches="tight")

# Combined Plot
fig = plt.figure(figsize=(8, 5))
ax = fig.add_subplot(111)
for typ, color in zip(CITY_TYPES, colors):
    plot_bubble_chart(ax, typ, color)
fig.text(**text_arguments)
fig.savefig(output_path / f"ridesharing.jpeg", dpi=300, bbox_inches="tight")

# %%
# Get stats of all dataframes by city type
quartile_1 = lambda x: np.quantile(x, 0.25)
quartile_3 = lambda x: np.quantile(x, 0.75)


def get_stats(series):
    """Return the results of statistical functions
    applied to the series."""
    stats = ["mean", "median", "mode", "q1", "q3"]
    functions = [np.mean, np.median, sts.mode, quartile_1, quartile_3]
    return {stat: func(series) for stat, func in zip(stats, functions)}


def get_stats_by_city_types(dataset):
    """Get all the statistical data, mean, mode, etc.
    for all the elements in the dataset. Returns a DF."""
    return pd.DataFrame(
        {city_type: get_stats(dataset[city_type]) for city_type in CITY_TYPES}
    )


# Execute for the data we want
ride_count_stats = get_stats_by_city_types(ride_count)
fare_stats = get_stats_by_city_types(fares)
drivers_stats = get_stats_by_city_types(drivers)
ride_count_stats

# %%
# Find outliers by city type
def find_outliers(data, stats):
    """Use IQR to locate out of bounds outliers."""
    q1 = stats["q1"]
    q3 = stats["q3"]
    upper_bound = q3 + 1.5 * (q3 - q1)
    lower_boud = q1 - 1.5 * (q3 - q1)
    return data[data >= upper_bound]


def find_outliers_by_city_types(data, stats):
    """Return a dataframe of all outliers in the data."""
    return pd.DataFrame({t: find_outliers(data[t], stats[t]) for t in CITY_TYPES})


ride_count_outliers = find_outliers_by_city_types(ride_count, ride_count_stats)
fares_outliers = find_outliers_by_city_types(fares, fare_stats)
drivers_outliers = find_outliers_by_city_types(drivers, drivers_stats)
ride_count_outliers
# %%
# Create Box and Whiskers plots
def plot_box_and_whisker(
    fig: plt.Figure,
    dataset: dict,
    title: str,
    ylabel: str,
    file_name: str,
    yticks: range,
):
    """Create a Box and Whisker from specified dataset."""
    ax: plt.Axes = fig.add_subplot(111)
    x_labels = [i for i in CITY_TYPES]
    ax.set_title(title, fontsize=20)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.set_xlabel("City Types", fontsize=14)
    ax.boxplot(dataset.values(), labels=x_labels)
    ax.set_yticks(yticks)
    ax.grid()
    fig.savefig(output_path / file_name, dpi=300)
    return fig


# Ride Count
plot_box_and_whisker(
    plt.figure(figsize=(8, 5)),
    ride_count,
    "Ride Count Data (2019)",
    "Number of Rides",
    "ride_count_data.jpeg",
    np.arange(0, 45, step=3.0),
)
# Fares
plot_box_and_whisker(
    plt.figure(figsize=(8, 5)),
    fares,
    "Ride Fare Data (2019)",
    "Fare($USD)",
    "ride_fare_data.jpeg",
    np.arange(0, 65, step=5.0),
)
# Drivers
plot_box_and_whisker(
    plt.figure(figsize=(8, 5)),
    drivers,
    "Drivers Data (2019)",
    "Drivers count",
    "ride_drivers_data.jpeg",
    np.arange(0, 80, step=5.0),
)
# %%
# Create Pie Charts
def plot_pie_chart(fig: plt.Figure, column: str, title: str, file_name: str):
    """Create Pie Chart of percentages from column name."""
    type_percents = (
        100
        * pyber_data_df.groupby(["type"]).sum()[column]
        / pyber_data_df[column].sum()
    )
    ax: plt.Axes = fig.add_subplot(111)
    ax.pie(
        type_percents,
        labels=["Rural", "Suburban", "Urban"],
        colors=["gold", "lightskyblue", "lightcoral"],
        explode=[0, 0, 0.1],
        autopct="%1.1f%%",
        shadow=True,
        startangle=150,
    )
    ax.set_title(title)
    mpl.rcParams["font.size"] = 14
    fig.savefig(output_path / file_name, dpi=300)


# Fares
plot_pie_chart(
    plt.figure(figsize=(8, 5)),
    COL.FARE,
    "% of Total Fares by City Type",
    "percentage_total_fares.jpeg",
)
# Ride counts
plot_pie_chart(
    plt.figure(figsize=(8, 5)),
    COL.RIDE,
    "% of Total Rides by City Type",
    "percentage_total_rides.jpeg",
)
# Drivers
plot_pie_chart(
    plt.figure(figsize=(8, 5)),
    COL.DRIVERS,
    "% of Total Drivers by City Type",
    "percentage_total_drivers.jpeg",
)
