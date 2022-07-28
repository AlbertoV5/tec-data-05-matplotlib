import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as sts
import matplotlib as mpl
from collections import namedtuple


class Pyber:
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
    COL = namedtuple(
        "Columns",
        "CITY TYPE FARE DRIVERS RIDE",
        defaults=["city", "type", "fare", "driver_count", "ride_id"],
    )()
    city_types = namedtuple(
        "CityTypes", "URBAN SUBURBAN RURAL", defaults=["Urban", "Suburban", "Rural"]
    )()

    @classmethod
    def get_counts(cls, city_types_dict: dict, col: str) -> dict:
        """Return dictionary of city types with values of
        series of counts of specified column."""
        return {
            typ: city_types_dict[typ].groupby([cls.COL.CITY])[col].count()
            for typ in city_types_dict
        }

    @classmethod
    def get_averages(cls, city_types_dict: dict, col: str) -> dict:
        """Return dictionary of city types with values of
        series of averages of specified column."""
        return {
            typ: city_types_dict[typ].groupby([cls.COL.CITY])[col].mean()
            for typ in city_types_dict
        }
    
    @classmethod
    def apply_stats_func(cls, series: pd.Series):
        """Return the results of statistical functions
        applied to the series."""
        stats = ["mean", "median", "mode", "q1", "q3"]
        functions = [np.mean, np.median, sts.mode, 
            lambda x: np.quantile(x, 0.25), lambda x: np.quantile(x, 0.75)]
        return {stat: func(series) for stat, func in zip(stats, functions)}

    @classmethod
    def get_stats(cls, dataset: dict):
        """Get all the statistical data, mean, mode, etc.
        for all the elements in the dataset. Returns a DF."""
        return pd.DataFrame(
            {city_type: cls.apply_stats_func(dataset[city_type]) 
            for city_type in Pyber.city_types}
        )

    @classmethod
    def calculate_outliers(cls, data, stats):
        """Use IQR to locate out of bounds outliers."""
        q1 = stats["q1"]
        q3 = stats["q3"]
        upper_bound = q3 + 1.5 * (q3 - q1)
        lower_boud = q1 - 1.5 * (q3 - q1)
        return data[(data >= upper_bound) | (data <= lower_boud)]

    @classmethod
    def find_outliers(cls, data: dict, stats: dict):
        """Return a dataframe of all outliers in the data."""
        return pd.DataFrame({t: cls.calculate_outliers(data[t], stats[t]) for t in Pyber.city_types})


    @classmethod
    def plot_bubble_chart(
        cls,
        ax: plt.Axes,
        x_axis: pd.Series,
        y_axis: pd.Series,
        sizes: pd.Series,
        label: str,
        color: str,
    ) -> plt.Axes:
        """Generate a scatter-bubble chart.

        Args:
            ax (plt.Axes): Figure's ax.
            x_axis (pd.Series):
            y_axis (pd.Series):
            sizes (pd.Series): Scale it up or down before passing it.
            label (str):
            color (str):

        Returns:
            plt.Axes: Same ax received.
        """
        ax.scatter(
            x_axis,
            y_axis,
            s=sizes,
            color=color,
            linewidths=1,
            edgecolors="k",
            alpha=0.8,
            label=label,
        )
        ax.set_title("PyBer Ride-Sharing Data (2019)")
        ax.set_xlabel("Total Number of Rides (Per City)")
        ax.set_ylabel("Average Fare ($)")
        ax.grid(True)
        legend = ax.legend(
            fontsize="12",
            mode="Expanded",
            scatterpoints=1,
            loc="best",
            title="City Type",
        )
        for lg in legend.legendHandles:
            lg._sizes = [75]
        legend.get_title().set_fontsize(12)
        return ax

    @classmethod
    def bubble_charts(cls, x_axis: dict, y_axis: dict, sizes: dict):
        for city_type, color in zip(cls.city_types, cls.colors):
            fig = plt.figure(figsize=(8, 5))
            ax = fig.add_subplot(111)
            Pyber.plot_bubble_chart(
                ax,
                x_axis[city_type],
                y_axis[city_type],
                10 * sizes[city_type],
                city_type,
                color,
            )
            fig.text(**cls.text_arguments)
            yield fig, city_type

    @classmethod
    def bubble_chart_all(cls, x_axis: dict, y_axis: dict, sizes: dict):
        fig = plt.figure(figsize=(8, 5))
        ax = fig.add_subplot(111)
        for city_type, color in zip(cls.city_types, cls.colors):
            Pyber.plot_bubble_chart(
                ax,
                x_axis[city_type],
                y_axis[city_type],
                10 * sizes[city_type],
                city_type,
                color,
            )
        fig.text(**cls.text_arguments)
        return fig
