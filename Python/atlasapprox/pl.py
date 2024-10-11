"""Plotting functions for the atlasapprox API Python package."""

from typing import Sequence, Union
import numpy as np
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import seaborn as sns


def heatmap(
    api,
    organism: str,
    organ: str,
    features: Sequence[str],
    measurement_type: str = "gene_expression",
    kind: str = "average",
    ax: Union[Axes, None] = None,
    tight_layout: bool = True,
    log1p=True,
    transpose=False,
    **kwargs,
):
    """Plot a heatmap of atlasapprox data.

    Args:
        organism: The organism to query.
        organ: The organ to query.
        features: The features (e.g. genes) to query.
        measurement_type: The measurement type to query.
        kind (average or fraction_detected): The kind of data to plot.
        ax: The axes to plot on. If None, a new figure is created.
        tight_layout: Whether to call plt.tight_layout() before returning.
        log1p: Whether to take the log1p of the averages before plotting.
        transpose: Whether to transpose the plot (features as columns).
        **kwargs: Keyword arguments passed to seaborn.heatmap.

    Return: A dictionary with figure, axes, and data frame with the plotted data.

    """

    if kind == "average":
        dataframe = api.average(
            organism=organism,
            organ=organ,
            features=features,
            measurement_type=measurement_type,
        )
    elif kind == "fraction_detected":
        dataframe = api.fraction_detected(
            organism=organism,
            organ=organ,
            features=features,
            measurement_type=measurement_type,
        )
    else:
        raise ValueError("kind must be 'average' or 'fraction_detected'")

    if transpose:
        datafame = dataframe.T

    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 4))

    if log1p:
        dataframe = np.log1p(dataframe)

    sns.heatmap(dataframe, ax=ax, **kwargs)

    # Feature names are canonically on top
    if transpose:
        ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)

    if tight_layout:
        ax.figure.tight_layout()

    return {
        "dataframe": dataframe,
        "fig": ax.figure,
        "ax": ax,
    }


def dotplot(
    api,
    organism: str,
    organ: str,
    features: Sequence[str],
    measurement_type: str = "gene_expression",
    ax: Union[Axes, None] = None,
    tight_layout: bool = True,
    log1p=True,
    transpose=False,
    **kwargs,
):
    """Plot a dot plot of atlasapprox data.

    Args:
        organism: The organism to query.
        organ: The organ to query.
        features: The features (e.g. genes) to query.
        measurement_type: The measurement type to query.
        ax: The axes to plot on. If None, a new figure is created.
        tight_layout: Whether to call plt.tight_layout() before returning.
        log1p: Whether to take the log1p of the averages before plotting.
        transpose: Whether to transpose the plot (features as columns).
        **kwargs: Keyword arguments passed to seaborn.heatmap.

    Return: A dictionary with figure, axes, and data frame with the plotted data.

    """

    result = api.dotplot(
        organism=organism,
        organ=organ,
        features=features,
        measurement_type=measurement_type,
    )
    if transpose:
        result["fraction_detected"] = result["fraction_detected"].T
        result["average"] = result["average"].T

    nrows, ncols = result["average"].shape

    if ax is None:
        fig, ax = plt.subplots(figsize=(2 + 0.3 * ncols, 2.2 + 0.28 * nrows))

    y, x = np.meshgrid(np.arange(nrows), np.arange(ncols), indexing="ij")
    x = x.ravel()
    y = y.ravel()
    s = 100 * np.sqrt(result["fraction_detected"].values.ravel())
    c = result["average"].values.ravel()
    if log1p:
        c = np.log1p(c)

    # Normalize the color intensity
    vmin = c.min()
    vmax = c.max() + 1e-5
    c = 1.0 * (c - vmin) / (vmax - vmin)

    cmap = plt.get_cmap(kwargs.get("cmap", "viridis"))
    c = cmap(c)

    ax.scatter(x, y, s=s, c=c)
    ax.set(
        xticks=np.arange(ncols),
        yticks=np.arange(nrows),
        xlim=(-0.5, ncols - 0.5),
        ylim=(-0.5, nrows - 0.5),
    )
    ax.set_xticklabels(result["average"].columns, rotation=90)
    ax.set_yticklabels(result["average"].index)

    # Feature names are canonically on top
    if transpose:
        ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)

    # colorbar
    ax.figure.colorbar(
        plt.cm.ScalarMappable(
            norm=plt.Normalize(vmin=vmin, vmax=vmax),
            cmap=cmap,
        ),
        ax=ax,
    )

    if tight_layout:
        ax.figure.tight_layout()

    return {
        "fraction_detected": result["fraction_detected"],
        "average": result["average"],
        "fig": ax.figure,
        "ax": ax,
    }
