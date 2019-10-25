import itertools
import json
from monty.io import zopen
import numpy as np
from .tools import species_string_from_site

class Atom(object):
    """Represents a single persistent atom during a simulation.

    Attributes:
        species_string (str): String for this atom speceis, e.g. 'Li'.
        index (int): Unique numeric index identifying this atom.
        in_site (int): Site index for the site this atom
            currently occupies.
        frac_coords (np.array): Numpy array containing the current fractional
            coordinates for this atom.
        trajectory (list): List of site indices occupied at each timestep.

    """
    
    newid = itertools.count(1)
    
    def __init__(self, species_string, fixed_structure_index=True):
        """Initialise an Atom object.

        Args:
            species_string (str): String for this atom species, e.g. 'Li'.
            fixed_structure_index (:obj:bool, optional): Set whether this atom will have the same
                index in all structures to be parsed. Default is True.
           
        Returns:
            None

        """
        self.species_string = species_string
        self.index = next(Atom.newid)
        self.in_site = None
        self._frac_coords = None
        self.trajectory = []
        self.fixed_structure_index = fixed_structure_index
        self.structure_index = None

    def reset(self):
        """Reset the state of this Atom.

        Clears the `in_site` and `trajectory` attributes.

        Returns:
            None

        """
        self.in_site = None
        self._frac_coords = None
        self.trajectory = []

    def get_coords(self, structure):
        """TODO"""
        if not self.fixed_structure_index or not self.structure_index:
            self.structure_index = [ i for i, s in enumerate(structure)
                if species_string_from_site(s) is self.species_string ][self.index-1]
        self._frac_coords = structure[self.structure_index].frac_coords
        
    @property
    def frac_coords(self):
        if self._frac_coords is None:
            raise AttributeError('Coordinates not set for atom {}'.format(self.index))
        else:
            return self._frac_coords

    def as_dict(self):
        d = {'species_string': self.species_string,
             'index': self.index,
             'in_site': self.in_site,
             'frac_coords': self._frac_coords.tolist()}
        return d

    @classmethod
    def from_dict(cls, d):
        atom = cls(species_string=d['species_string'])
        atom.index = d['index']
        atom.in_site = d['in_site']
        atom._frac_coords = np.array(d['frac_coords'])
        return atom

    def to(self, filename=None):
        s = json.dumps(self.as_dict())
        if filename:
            with zopen(filename, "wt") as f:
                f.write('{}'.format(s))
        return s

    @classmethod
    def from_str(cls, input_string):
        d = json.loads(input_string)
        return cls.from_dict(d)

    @classmethod
    def from_file(cls, filename):
        with zopen(filename, "rt") as f:
            contents = f.read()
        return cls.from_str(contents)

    @classmethod
    def reset_index(cls):
        cls.newid = itertools.count(1)
