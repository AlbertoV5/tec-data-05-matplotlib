"""
Pyber Plotting Class.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.colors import ListedColormap


class Pyber:
    """Configs and class methods for pre-made charts."""

    dpi = 200
    fontsize = 8
    city_types = ["Rural", "Suburban", "Urban"]
    colors = ["coral", "skyblue", "gold"]
    colormap = ListedColormap(colors, name="PyBer")
    colormap_reversed = colormap.reversed()
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
    def _get_wide_figure(cls) -> plt.Figure:
        return plt.figure(
            figsize=(1920 / cls.dpi, 1200 / cls.dpi), facecolor="white", dpi=cls.dpi
        )

    @classmethod
    def _get_squared_figure(cls) -> plt.Figure:
        return plt.figure(
            figsize=(1080 / cls.dpi, 1080 / cls.dpi), facecolor="white", dpi=cls.dpi
        )

    @classmethod
    def _get_ultra_wide_figure(cls) -> plt.Figure:
        return plt.figure(
            figsize=(1920 / cls.dpi, 612 / cls.dpi), facecolor="white", dpi=cls.dpi
        )

    @classmethod
    def _plot_bubble(
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
    def plot_bubble_many(
        cls, x_axis: pd.DataFrame, y_axis: pd.DataFrame, sizes: pd.DataFrame
    ):
        """Yield bubble charts per city type.

        Example:

            for fig, city_type in Pyber.plot_bubble_many(df_x, df_y, df_s):
                fig.save(f"{city_type}.png", dpi=Pyber.dpi)
        """
        for city_type, color in zip(cls.city_types, cls.colormap_reversed.colors):
            fig = cls._get_wide_figure()
            ax = fig.add_subplot(111)
            cls._plot_bubble(
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
    def plot_bubble_combined(
        cls, x_axis: pd.DataFrame, y_axis: pd.DataFrame, sizes: pd.DataFrame
    ):
        """Return a bubble chart combined from many dataframes."""
        fig = cls._get_wide_figure()
        ax = fig.add_subplot(111)
        for city_type, color in zip(cls.city_types, cls.colormap_reversed.colors):
            cls._plot_bubble(
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
    def plot_box_and_whiskers(
        cls,
        dataset: pd.Series,
        title: str,
        ylabel: str,
    ):
        """Create a Box and Whisker from specified dataset."""
        fig = cls._get_wide_figure()
        ax: plt.Axes = fig.add_subplot(111)
        ax.set_title(title, fontsize=18)
        ax.set_ylabel(ylabel, fontsize=14)
        ax.set_xlabel("City Types", fontsize=14)
        mpl.rcParams["font.size"] = cls.fontsize + 2
        x_labels = [city_type for city_type in reversed(cls.city_types)]
        boxplots = ax.boxplot(
            [dataset[city_type] for city_type in reversed(cls.city_types)],
            labels=x_labels,
            patch_artist=True,
        )
        for box, color in zip(boxplots["boxes"], cls.colors):
            box.set_facecolor(color)
        for line in boxplots["medians"]:
            line.set_color("black")
        upper_lim = np.max([np.max(i) for i in dataset])
        step = 3.0 if upper_lim < 40 else 5.0
        yticks = np.arange(0, upper_lim + step, step)
        ax.set_yticks(yticks)
        ax.grid(True)
        return fig

    @classmethod
    def plot_pie_chart(cls, df: pd.DataFrame, title: str):
        """Create Pie Chart of percentages from DataFrame."""
        fig = cls._get_squared_figure()
        ax: plt.Axes = fig.add_subplot(111)
        ax.pie(
            df,
            labels=cls.city_types,
            colors=cls.colormap_reversed.colors,
            explode=[0, 0, 0.1],
            autopct="%1.1f%%",
            shadow=True,
            startangle=150,
        )
        ax.set_title(title)
        mpl.rcParams["font.size"] = cls.fontsize + 2
        return fig

    @classmethod
    def plot_timeseries(cls, timeseries_df: pd.DataFrame) -> plt.Figure:
        """Create a Total Fare by City Type timeseries chart."""
        style.use("fivethirtyeight")
        mpl.rcParams["font.size"] = cls.fontsize
        fig = cls._get_ultra_wide_figure()
        ax = fig.add_subplot(111)
        ax = timeseries_df.plot(
            ax=ax,
            title="Total Fare by City Type",
            ylabel="Fare($USD)",
            xlabel="",
            fontsize=cls.fontsize,
            colormap=cls.colormap_reversed,
        )
        legend = ax.legend(
            fontsize=cls.fontsize,
            labels=cls.city_types,
            mode="Expanded",
            scatterpoints=1,
            loc="center",
            title="City Type",
        )
        for lg in legend.legendHandles:
            lg._sizes = [75]
        legend.get_title().set_fontsize(cls.fontsize)
        return fig

    @classmethod
    def savefig(cls, fig: plt.Figure, path: str) -> None:
        """Use Pyber config to save figure in given path."""
        fig.savefig(path, dpi=cls.dpi, bbox_inches="tight")
