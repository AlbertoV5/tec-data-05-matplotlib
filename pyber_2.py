"""
Pyber
"""
# %%
# Load modules and dataframes
from matplotlib import style
import matplotlib as mpl
import pandas as pd
from pathlib import Path
from pyberlib import Pyber
import matplotlib.pyplot as plt

resources = Path("resources")
output_path = Path("analysis")
city_data_df = pd.read_csv(resources / "city_data.csv")
ride_data_df = pd.read_csv(resources / "ride_data.csv")
# Merge and index
pyber_data_df = city_data_df.merge(
    ride_data_df, on=[Pyber.COL.CITY, Pyber.COL.CITY]
).set_index(Pyber.COL.CITY)
city_data_df = city_data_df.set_index(Pyber.COL.CITY)

# %%
# Create a summary of fares totals and averages
format_comma = lambda x: f"{x:,}"
format_currency = lambda x: f"${x:,.2f}"
total_fares = pyber_data_df.groupby(["type"])[Pyber.COL.FARE].sum()
total_rides = pyber_data_df.groupby(["type"])[Pyber.COL.RIDES].count()
total_drivers = city_data_df.groupby(["type"])[Pyber.COL.DRIVERS].sum()
fare_per_ride = total_fares / total_rides
fare_per_driver = total_fares / total_drivers
fares_summary_df = pd.DataFrame(
    {
        "Total Rides": total_rides.map(format_comma),
        "Total Drivers": total_drivers.map(format_comma),
        "Total Fares": total_fares.map(format_currency),
        "Average Fare per Ride": fare_per_ride.map(format_currency),
        "Average Fare per Driver": fare_per_driver.map(format_currency),
    }
)
fares_summary_df
# %%
# Pivot Dates
dates = pyber_data_df.groupby(["type", "date"])["fare"].sum()
dates = dates.reset_index()
dates_pivot = dates.pivot(index="date", columns="type")
dates_range = dates_pivot.loc[
    (dates_pivot.index >= "2019-01-01") & (dates_pivot.index <= "2019-04-28")
].reset_index()
dates_range["date"] = pd.to_datetime(dates_range["date"])
fares_per_week = dates_range.resample("W", on="date").sum()
fares_per_week
# %%
# Graph the time series
style.use("fivethirtyeight")
mpl.rcParams["font.size"] = 12
dpi = 150
fig = plt.figure(figsize=(1920 / dpi, 612 / dpi), facecolor="white", dpi=dpi)
ax = fig.add_subplot(111)
ax = fares_per_week.plot(
    ax=ax,
    title="Total Fare by City Type",
    ylabel="Fare($USD)",
    xlabel="",
    fontsize="12",
)
legend = ax.legend(
    fontsize="12",
    labels=["Rural", "Suburban", "Urban"],
    mode="Expanded",
    scatterpoints=1,
    loc="center",
    title="City Type",
)
for lg in legend.legendHandles:
    lg._sizes = [75]
legend.get_title().set_fontsize(12)
fig.savefig(output_path / "PyBer_fare_summary.png", dpi=dpi, bbox_inches="tight")
plt.show()
