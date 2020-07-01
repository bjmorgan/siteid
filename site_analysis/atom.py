import itertools
import json
from monty.io import zopen # type: ignore
import numpy as np # type: ignore
from typing import List, Optional, ClassVar, TypeVar, Type, Dict, Any
from pymatgen import Structure # type: ignore

A = TypeVar('A', bound='Atom')

class Atom(object):
    """Represents a single atom from a simulation trajectory.

    Attributes:
        index (int): Unique numeric index identifying this atom.
        in_site (int): Site index for the site this atom
            currently occupies.
        frac_coords (np.array): Numpy array containing the current fractional
            coordinates for this atom.
        trajectory (list): List of site indices occupied at each timestep.

    """

    def __init__(self, index: int, 
                 species_string: Optional[str] = None) -> None:
        """Initialise an Atom object.

        Args:
            index (int): Numerical index for this atom. Used to identify this atom
                in analysed structures.

        Returns:
            None

        """
        self.index: int = index
        self.in_site: Optional[int] = None
        self._frac_coords: Optional[np.ndarray] = None
        self.trajectory: List[Optional[int]] = []

    def __str__(self) -> str:
        """Return a string representation of this atom.

        Args:
            None

        Returns:
            (str)

        """
        string = f"Atom: {self.index}"
        return string

    def __repr__(self) -> str:
        string = (
            "site_analysis.Atom("
            f"index={self.index}, "
            f"in_site={self.in_site}, "
            f"frac_coords={self._frac_coords})"
        )
        return string

    def reset(self) -> None:
        """Reset the state of this Atom.

        Clears the `in_site` and `trajectory` attributes.

        Returns:
            None

        """
        self.in_site = None
        self._frac_coords = None
        self.trajectory = []

    def assign_coords(self, structure: Structure) -> None:
        """Assign fractional coordinates to this atom from a 
        pymatgen Structure.

        Args:
            structure (pymatgen.Structure): The Structure to use for this atom's
                fractional coordinates.

        Returns:
            None

        """
        self._frac_coords = structure[self.index].frac_coords

    @property
    def frac_coords(self) -> np.ndarray:
        """Getter for the fractional coordinates of this atom.

        Raises:
            AttributeError: if the fractional coordinates for this atom have
                not been set.

        """
        if self._frac_coords is None:
            raise AttributeError("Coordinates not set for atom {}".format(self.index))
        else:
            return self._frac_coords

    def as_dict(self) -> Dict['str', Any]:
        d = {
            "index": self.index,
            "in_site": self.in_site,
            "frac_coords": self._frac_coords.tolist() if self._frac_coords else None,
        }
        return d

    @classmethod
    def from_dict(cls: Type[A], d: Dict['str', Any]) -> A:
        atom = cls(index=d["index"])
        atom.in_site = d["in_site"]
        atom._frac_coords = np.array(d["frac_coords"])
        return atom

    def to(self, filename: Optional[str] = None) -> str:
        s = json.dumps(self.as_dict())
        if filename:
            with zopen(filename, "wt") as f:
                f.write("{}".format(s))
        return s

    @classmethod
    def from_str(cls: Type[A], input_string: str) -> A:
        """Initiate an Atom object from a JSON-formatted string.

        Args:
            input_string (str): JSON-formatted string.

        Returns:
            (Atom)

        """
        d = json.loads(input_string)
        return cls.from_dict(d)

    @classmethod
    def from_file(cls: Type[A], filename: str) -> A:
        with zopen(filename, "rt") as f:
            contents = f.read()
        return cls.from_str(contents)

def atoms_from_species_string(structure: Structure, 
                              species_string: str) -> List[Atom]:
    atoms = [Atom(index=i) for i, s in enumerate(structure)
             if s.species_string == species_string]
    return atoms

def atoms_from_indices(indices: List[int]) -> List[Atom]:
    return [Atom(index=i) for i in indices]
