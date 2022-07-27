import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

resources = Path("resources")
city_data_df = pd.read_csv(resources / "city_data.csv")
ride_data_df = pd.read_csv(resources / "ride_data.csv")

CITY = "city"
TYPE = "type"
FARE = "fare"
DRIVERS = "driver_count"
RIDES = "ride_id"

complete_data_df = city_data_df.merge(ride_data_df, on=[CITY, CITY])
complete_data_df = complete_data_df.set_index(CITY)
city_type_group = complete_data_df.groupby(TYPE)
# Per City Type
rides_per_city_type = city_type_group.count()[RIDES]
fare_average_per_city_type = city_type_group.mean()[FARE]
drivers_per_city_type = city_type_group.sum()[DRIVERS]
