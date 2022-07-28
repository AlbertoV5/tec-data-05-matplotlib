"""
Pyber Plotting Library.

Custom plotting configurations for Pyber data.
"""
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.colors import ListedColormap


class Pyber:
    dpi = 200
    fontsize = 8
    city_types = ["Rural", "Suburban", "Urban"]
    colors = ["coral", "skyblue", "gold"]
    colormap = ListedColormap(colors, name="PyBer")
    bubble_text_args = {
        "x": 0.92,
        "y": 0.5,
        "s": "Note: Circle size\ncorrelates with\ndriver per country.",
        "fontsize": 10,
        "horizontalalignment": "left",
        "verticalalignment": "center",
        "bbox": dict(facecolor="white", alpha=0.7),
    }

    @classmethod
    def _chart_bubble(
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
    def chart_bubble_many(cls, x_axis: dict, y_axis: dict, sizes: dict):
        """Yield many bubble charts.
        
        Example:
            for fig, city_type in Pyber.chart_bubble_many(df_x, df_y, df_s):
                fig.save(f"{city_type}.png", dpi=Pyber.dpi)
        """
        for city_type, color in zip(cls.city_types, cls.colors):
            fig = plt.figure(figsize=(8, 5))
            ax = fig.add_subplot(111)
            Pyber._chart_bubble(
                ax,
                x_axis[city_type],
                y_axis[city_type],
                10 * sizes[city_type],
                city_type,
                color,
            )
            fig.text(**cls.bubble_text_args)
            yield fig, city_type

    @classmethod
    def chart_bubble_combined(cls, x_axis: dict, y_axis: dict, sizes: dict):
        """Return a bubble chart combined from many dataframes."""
        fig = plt.figure(figsize=(8, 5))
        ax = fig.add_subplot(111)
        for city_type, color in zip(cls.city_types, cls.colors):
            Pyber._chart_bubble(
                ax,
                x_axis[city_type],
                y_axis[city_type],
                10 * sizes[city_type],
                city_type,
                color,
            )
        fig.text(**cls.bubble_text_args)
        return fig

    @classmethod
    def chart_timeseries(cls, timeseries_df: pd.DataFrame):
        style.use('fivethirtyeight')
        mpl.rcParams["font.size"] = cls.fontsize
        fig = plt.figure(
            figsize=(1920/cls.dpi, 612/cls.dpi), 
            facecolor="white",
            dpi=cls.dpi)
        ax = fig.add_subplot(111)
        ax = timeseries_df.plot(
            ax = ax,
            title="Total Fare by City Type",
            ylabel="Fare($USD)",
            xlabel="",
            fontsize=cls.fontsize,
            colormap = cls.colormap
        )
        legend = ax.legend(
            fontsize=cls.fontsize,
            labels = cls.city_types,
            mode="Expanded", 
            scatterpoints=1, 
            loc="center", 
            title="City Type"
        )
        for lg in legend.legendHandles:
            lg._sizes = [75]
        legend.get_title().set_fontsize(cls.fontsize)
        return fig