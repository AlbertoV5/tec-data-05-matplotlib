"""
Pyber
"""
# %%
# Setup dataframes and functions
import pandas as pd
from pathlib import Path
from pyberlib import Pyber

# %%
# Load data and merge data
resources = Path("resources")
output_path = Path("analysis")
city_data_df = pd.read_csv(resources / "city_data.csv")
ride_data_df = pd.read_csv(resources / "ride_data.csv")
pyber_data_df = city_data_df.merge(ride_data_df, on=[Pyber.COL.CITY, Pyber.COL.CITY])
pyber_data_df = pyber_data_df.set_index(Pyber.COL.CITY)

# %%
# Separate data per City Type
city_types_dict = {
    typ: pyber_data_df[pyber_data_df[Pyber.COL.TYPE] == typ] 
    for typ in Pyber.city_types
}
ride_count = Pyber.get_counts(city_types_dict, Pyber.COL.RIDE)
fare_count = {typ: city_types_dict[typ][Pyber.COL.FARE] for typ in Pyber.city_types}
driver_count = {typ: city_types_dict[typ][Pyber.COL.DRIVERS] for typ in Pyber.city_types}
fare_average = Pyber.get_averages(city_types_dict, Pyber.COL.FARE)
drivers_average = Pyber.get_averages(city_types_dict, Pyber.COL.DRIVERS)

# %%
# Get stats
ride_count_stats = Pyber.get_stats(ride_count)
fare_stats = Pyber.get_stats(fare_count)
drivers_stats = Pyber.get_stats(driver_count)

# %%
# Find outliers
ride_count_outliers = Pyber.find_outliers(ride_count, ride_count_stats)
fares_outliers = Pyber.find_outliers(fare_count, fare_stats)
drivers_outliers = Pyber.find_outliers(driver_count, drivers_stats)

# %% 
# Plotting
# # Bubble charts many
# for fig, city_type in Pyber.bubble_charts(ride_count, fare_average, drivers_average):
#     fig.savefig(output_path / f"ridesharing_{city_type}.jpeg", 
#         dpi=300, bbox_inches="tight")
# # Bubble charts combined
# fig = Pyber.bubble_chart_all(ride_count, fare_average, drivers_average)
# fig.savefig(output_path / f"ridesharing.jpeg", dpi=300, bbox_inches="tight")