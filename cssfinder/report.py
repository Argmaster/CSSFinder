# Copyright 2023 Krzysztof Wiśniewski <argmaster.world@gmail.com>
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the “Software”), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Utilities for runtime report creation."""

from __future__ import annotations

import base64
import json
import sys
from collections import OrderedDict
from dataclasses import asdict, dataclass
from functools import lru_cache
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Optional

import jinja2
import numpy as np
import weasyprint
from matplotlib import figure as fig
from matplotlib import pyplot as plt

if TYPE_CHECKING:
    import numpy.typing as npt
    import pandas as pd
    from typing_extensions import Self

    from cssfinder.cssfproject import Task


class HTMLReport:
    """HTML based report generator."""

    def __init__(self, props: SlopeProperties, plots: list[Plot], task: Task) -> None:
        self.ctx = _HTMLReportCtx(props, plots, task)
        self.env = jinja2.Environment(
            loader=jinja2.PackageLoader("cssfinder"),
            autoescape=jinja2.select_autoescape(),
        )

    def render(self) -> RenderedReport:
        """Render report.

        Returns
        -------
        RenderedReport
            Report handle providing interface for saving report.

        """
        template = self.env.get_template("report.html.jinja2")

        return RenderedReport(template.render(ctx=self.ctx))


@dataclass
class _HTMLReportCtx:
    props: SlopeProperties
    plots: list[Plot]
    task: Task

    @property
    def title(self) -> str:
        return f"Report {self.task.output.parent.parent.name} / {self.task.name}"

    @property
    def meta(self) -> OrderedDict:
        """Return project metadata."""
        return OrderedDict(
            {
                "Project name": self.task.project.meta.name,
                "Task name": self.task.name,
                "Author": self.task.project.meta.author,
                "Email": self.task.project.meta.email,
                "Description": self.task.project.meta.description,
                "Version": self.task.project.meta.version,
            }
        )

    @property
    def math_props(self) -> OrderedDict:
        """Return mathematical properties."""
        return OrderedDict(
            {
                "Hilbert-Schmidt distance": f"{self.props.optimum:.3f}",
                "Sample correlation coefficient": f"{self.props.r_value:.3f}",
            }
        )


class RenderedReport:
    """Container for rendered report."""

    def __init__(self, content: str) -> None:
        self.content = content

    def save_to(self, dest: Path) -> None:
        """Save report to a file.

        Parameters
        ----------
        dest : Path
            Path to destination file.

        """
        dest.write_text(self.content, "utf-8")

    def save_pdf(self, dest: Path) -> None:
        """Save content as PDF.

        Parameters
        ----------
        dest : Path
            Path to destination file.

        """
        weasyprint.HTML(string=self.content).write_pdf(target=dest.as_posix())


class Plotter:
    """Plot creator class."""

    def __init__(self, corrections: pd.DataFrame) -> None:
        """Initialize plot creator.

        Parameters
        ----------
        corrections : pandas.DataFrame
            A DataFrame containing the distance decay corrections. The DataFrame
            should have an "index" column and a "value" column.

        """
        self.corrections = corrections
        self.slope_props = SlopeProperties.find(self.corrections.to_numpy())

    def plot_corrections(self, axes: Optional[plt.Axes] = None) -> Plot:
        """Create a plot of distance decay corrections.

        Parameters
        ----------
        axes : Optional[plt.Axes], optional
            Optional axes object to reuse, when none is given, new figure is created,
            by default None

        Returns
        -------
        Plot
            Plot object containing plot axes.

        Notes
        -----
        The function creates a line plot of the distance decay corrections,
        with the "index" column on the x-axis and the "value" column on the
        y-axis. The plot includes a grid and axis labels, and a title indicating
        that it shows distance decay.

        The function returns the Plot object granting access to axes for the created
        plot, which can be further customized or saved using the methods of the
        matplotlib API.

        """
        if axes is None:
            plt.figure()
            axes = plt.subplot()

        axes.plot(
            self.corrections[["index"]], self.corrections[["value"]], label="correction"
        )
        axes.hlines(
            [self.slope_props.optimum],
            xmin=-10,
            xmax=self.corrections[["index"]].max(),
            color="red",
            label="H-S distance",
        )
        axes.grid(visible=True)

        axes.set_xlabel("Correction index")
        axes.set_ylabel("Correction value")

        axes.set_title("Distance decay")
        plt.legend(loc="upper right")

        return Plot(axes)

    def plot_corrections_inverse(self, axes: Optional[plt.Axes] = None) -> Plot:
        """Create a plot offsets inverse of distance decay corrections.

        Parameters
        ----------
        axes : Optional[plt.Axes], optional
            Optional axes object to reuse, when none is given, new figure is created,
            by default None

        Returns
        -------
        Plot
            Plot object containing plot axes.

        Notes
        -----
        The function creates a line plot of the inverse of distance decay corrections,
        with the "index" column on the x-axis and the "value" column inverse on the
        y-axis. The plot includes a grid and axis labels, and a title indicating
        that it shows distance decay.

        The function returns the Plot object granting access to axes for the created
        plot, which can be further customized or saved using the methods of the
        matplotlib API.

        """
        if axes is None:
            plt.figure()
            axes = plt.subplot()

        axes.plot(
            self.corrections[["index"]],
            1 / (self.corrections[["value"]] - self.slope_props.optimum),
        )
        axes.grid(visible=True)

        axes.set_xlabel("Correction index")
        axes.set_ylabel("Correction offsetted inverse value")

        axes.set_title("Distance offsetted inverse decay")

        return Plot(axes)

    def plot_iteration(self, axes: Optional[plt.Axes] = None) -> Plot:
        """Create a plot of iteration linear corrections.

        Returns
        -------
        matplotlib.axes.Axes
            The axes object for the created plot.

        Notes
        -----
        The function creates a line plot of the iteration linear corrections,
        with the "iteration" column on the x-axis and the correction values on
        the y-axis. The correction values are calculated using the
        `SlopeProperties` class, which takes the "index" column as input and
        returns the corresponding correction values for each iteration.

        The plot includes a grid and axis labels, but no title. The function returns
        the axes object for the created plot, which can be further customized or
        saved using the methods of the matplotlib API.

        """
        if axes is None:
            plt.figure()
            axes = plt.subplot()

        axes.grid(visible=True)

        axes.set_xlabel("Iteration index")
        axes.set_ylabel("Correction index")

        axes.set_title("Total number of correction")

        axes.plot(
            self.corrections[["iteration"]],
            self.corrections[["index"]],
        )
        axes.plot(
            self.corrections[["iteration"]],
            self.corrections[["index"]],
        )

        return Plot(axes)


@dataclass
class Plot:
    """Container class for plots generated with Plotter class."""

    axes: plt.Axes

    @property
    def figure(self) -> fig.Figure:
        """Axes figure."""
        return self.axes.figure

    def configure(self, width: int = 8, height: int = 6) -> Self:
        """Set the size of the current figure.

        Parameters
        ----------
        width : int, optional
            The width of the figure in inches. Default is 10.
        height : int, optional
            The height of the figure in inches. Default is 10.

        Returns
        -------
        Self
            Returns the instance of the object to allow for method chaining.

        """
        self.axes.figure.set_figwidth(width)
        self.axes.figure.set_figheight(height)
        return self

    def save_plot(
        self,
        dest: Path | BytesIO,
        dpi: int = 300,
        file_format: Optional[str] = None,
    ) -> None:
        """Save figure to file.

        Parameters
        ----------
        dest : Path | BytesIO
            Path to file or writable BytesIO.
        dpi : int, optional
            Plot output dpi, by default 150
        file_format : Optional[str], optional
            File format, when None, deduced from file path, by default None

        """
        self.axes.figure.savefig(
            dest.as_posix() if isinstance(dest, Path) else dest,
            dpi=dpi,
            format=file_format,
        )

    def base64_encode(self, file_format: Optional[str] = None) -> str:
        """Encode plot as base64 string.

        Parameters
        ----------
        file_format : Optional[str], optional
            Preferred file format, by default None

        Returns
        -------
        str
            Encoded image.

        """
        io = BytesIO()
        self.save_plot(io, file_format=file_format)
        io.seek(0)

        return base64.b64encode(io.read()).decode("utf-8")


@dataclass
class SlopeProperties:
    """Class that encapsulates slope properties and provides methods to calculate
    correction values and find slope properties for a given dataset.

    Attributes
    ----------
    optimum: np.float64
        The optimum value found during the slope property calculation.
    r_value: np.float64
        The r-value calculated for the slope properties.
    aa1: np.float64
        The slope of the trend line of the correction index with respect to iteration
        index.
    bb1: np.float64
        The exponential decay coefficient calculated for the slope properties.

    Methods
    -------
    get_correction(x: npt.NDArray[np.float64]) -> np.float64:
        Returns the correction values for a given input array `x`.
    find(data: npt.NDArray[np.float64]) -> 'SlopeProperties':
        Finds the slope properties for a given dataset `data`.

    """

    optimum: np.float64
    r_value: np.float64
    aa1: np.float64
    bb1: np.float64

    def get_correction_count(self, x: np.float64) -> np.float64:
        """Return the correction values for a given input array `x`.

        Parameters
        ----------
        x: npt.NDArray[np.float64]
            Input array for which correction values will be calculated.

        Returns
        -------
        np.float64
            The correction values calculated for the input array `x`.

        """
        return np.multiply(  # type: ignore[no-any-return]
            np.power(x, self.aa1),
            self.bb1,
        )

    @classmethod
    def find(cls, data: npt.NDArray[np.float64]) -> Self:
        """Find the slope properties for a given dataset `data`.

        Parameters
        ----------
        data: npt.NDArray[np.float64]
            The dataset for which slope properties will be calculated.

        Returns
        -------
        SlopeProperties
            An instance of the SlopeProperties class representing the slope properties
            of the input data.

        """
        iteration_index: npt.NDArray[np.float64] = data[:, 0]
        correction_index: npt.NDArray[np.float64] = data[:, 1]
        correction_value: npt.NDArray[np.float64] = data[int(2 * len(data) / 3) :, 2]

        optimum = find_correction_optimum(data[:, 2])

        r_value = R(correction_value, optimum)

        aa1 = trend(iteration_index, correction_index)
        bb1 = np.exp(offset(iteration_index, correction_index))

        return cls(optimum, r_value, aa1, bb1)

    def save_to(self, dest: Path) -> None:
        """Save properties to file."""
        with dest.open("w", encoding="utf-8") as file:
            json.dump(asdict(self), file)


def cov(
    array_1: npt.NDArray[np.float64],
    array_2: npt.NDArray[np.float64],
) -> np.float64:
    """Calculate the covariance between two arrays.

    Parameters
    ----------
    array_1 : numpy.ndarray
        The first array.
    array_2 : numpy.ndarray
        The second array.

    Returns
    -------
    float
        The covariance between the two arrays.

    Notes
    -----
    The covariance is calculated as the mean of the element-wise product of
    the deviation from the mean of `array_1` and `array_2`. In other words,
    the covariance measures how much two variables change together, and it
    is a measure of the linear relationship between them.

    """
    return np.mean(  # type: ignore[no-any-return]
        np.multiply(
            np.subtract(array_1, np.mean(array_1)),
            np.subtract(array_2, np.mean(array_2)),
        ),
    )


def trend(
    array_1: npt.NDArray[np.float64],
    array_2: npt.NDArray[np.float64],
) -> np.float64:
    """Calculate the trend between two arrays.

    Parameters
    ----------
    array_1 : numpy.ndarray
        The first array.
    array_2 : numpy.ndarray
        The second array.

    Returns
    -------
    float
        The trend between the two arrays.

    Notes
    -----
    The trend is calculated as the covariance between the logarithm of
    `array_1` and `array_2` divided by the covariance between the logarithm
    of `array_1` and itself.

    """
    l1a = np.log(array_1)
    l2a = np.log(array_2)

    return cov(l1a, l2a) / cov(l1a, l1a)


def offset(
    array_1: npt.NDArray[np.float64],
    array_2: npt.NDArray[np.float64],
) -> np.float64:
    """Calculate the offset between the two input arrays.

    Offset is based on their logarithmic means and a decay trend.

    Parameters
    ----------
    array_1 : numpy.ndarray[np.float64]
        The first input array.
    array_2 : numpy.ndarray[np.float64]
        The second input array.

    Returns
    -------
    numpy.float64
        The calculated offset between the two input arrays.

    Raises
    ------
    ValueError
        If the input arrays are empty.

    Examples
    --------
    ```
    >>> array_1 = np.array([1.0, 2.0, 3.0])
    >>> array_2 = np.array([4.0, 5.0, 6.0])
    >>> offset(array_1, array_2)
    0.01638058574365686

    ```

    """
    array_1_mean = np.mean(np.log(array_1))
    array_2_mean = np.mean(np.log(array_2))
    decay_trend = trend(array_1, array_2)

    return array_1_mean - array_2_mean * decay_trend  # type: ignore[no-any-return]


def find_correction_optimum(values: npt.NDArray[np.float64]) -> np.float64:
    """Find the optimum correction value for a given input array of values.

    Parameters
    ----------
    values : numpy.ndarray[np.float64]
        The input array of values for which to find the optimum correction.

    Returns
    -------
    numpy.float64
        The optimum correction value for the input array of values.

    """
    values = values
    upper_half = values[len(values) // 2 :]

    optimum = upper_half[-1] - 1e-6
    step1 = optimum / 10000

    while R(upper_half, optimum - step1) > R(upper_half, optimum) and optimum > 0:
        optimum = optimum - step1

    return optimum  # type: ignore[no-any-return]


@lru_cache(16)
def _r_indexes(length: int) -> npt.NDArray[np.float64]:
    indexes = np.arange(length)
    difference = np.mean(np.square(indexes)) - np.square(np.mean(indexes))
    return difference  # type: ignore[no-any-return]


@lru_cache(16)
def _indexes(length: int) -> npt.NDArray[np.float64]:
    return np.arange(length, dtype=np.float64)


def R(values: npt.NDArray[np.float64], a: np.float64) -> np.float64:  # noqa: N802
    """Calculate the R value for a given input array of values and a correction factor.

    Parameters
    ----------
    values : numpy.ndarray[np.float64]
        The input array of values for which to calculate the R value.
    a : numpy.float64
        The correction factor to use when calculating the R value.

    Returns
    -------
    numpy.float64
        The R value for the input array of values and correction factor.

    """
    ll1 = np.divide(1.0, np.subtract(values, a))
    length = len(values)
    indexes = _indexes(length)

    aa1: np.float64 = np.mean(np.multiply(ll1, indexes)) - np.mean(ll1) * np.mean(
        indexes,
    )
    aa2: np.float64 = np.sqrt(
        (np.mean(np.square(ll1)) - np.square(np.mean(ll1))) * _r_indexes(length),
    )

    return np.divide(aa1, aa2, dtype=np.float64)  # type: ignore[no-any-return]


def display_short_report(data: npt.NDArray[np.float64]) -> None:
    """Display short report."""
    slope_properties = SlopeProperties.find(data)

    expr = f"corrections = trail ^ {slope_properties.aa1} * {slope_properties.bb1}"

    sys.stdout.write(
        "Basing on decay, the squared HS distance is estimated to be "
        f"{slope_properties.optimum} (R={slope_properties.r_value})\n",
    )
    sys.stdout.write(
        f"The dependence between correction and trail is approximately: {expr}\n",
    )
