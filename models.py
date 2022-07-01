"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from datetime import datetime

# from math import isnan
from typing import Union

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation: str = info.get("pdes")
        self.name: Union[str, None] = (
            info.get("name") if info.get("name") != "" else None
        )
        self.diameter: float = (
            float(info.get("diameter"))
            if info.get("diameter") != ""
            else float("nan")
        )
        self.hazardous: bool = True if info.get("pha") == "Y" else False
        self.approaches = []

    @property
    def fullname(self) -> str:
        """Return a representation of the full name of this NEO."""
        if self.name:
            return f"{self.designation} ({self.name})"
        return f"{self.designation}"

    def __str__(self):
        """Return `str(self)`."""
        return (
            f"A NearEarthObject {self.fullname} is {'' if self.hazardous else 'not '} potentially hazardous "
            f"and it's diameter is {str(self.diameter)+'km' if self.diameter != float('nan') else 'unknown'}."
        )

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"
        )

    def serialize(self) -> dict:
        """Convert class data to a dictionary with its attributes."""
        output = {}
        output["designation"] = self.designation
        output["name"] = self.name if self.name else ""
        output[
            "diameter_km"
        ] = self.diameter  # if not isnan(self.diameter) else "nan"
        output["potentially_hazardous"] = self.hazardous
        return output


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation: str = info.get("neo_id")
        self.time: datetime = cd_to_datetime(info.get("time"))
        self.distance: float = float(info.get("distance"))
        self.velocity: float = float(info.get("velocity"))
        self.neo: NearEarthObject = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return (
            f"At {self.time_str}, '{self.neo.fullname}' approaches Earth at a distance of {self.distance:.2f} "
            f"au and a velocity of {self.velocity:.2f} km/s."
        )

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
        )

    @property
    def neo_id(self) -> str:
        """Return designation of NearEarthObject."""
        return self._designation

    def serialize(self) -> dict:
        """Convert class data to a dictionary with its attributes."""
        return {
            "datetime_utc": self.time_str,
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
        }
