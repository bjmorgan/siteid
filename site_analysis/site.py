from collections import Counter
from abc import ABC, abstractmethod

from typing import Optional, List, TypeVar, Any, Type, Dict
from typing import Counter as CounterType
from site_analysis.atom import Atom
import numpy as np # type: ignore
from pymatgen import Structure, Lattice # type: ignore

S = TypeVar('S', bound='Site')

class Site(ABC):
    """Parent class for defining sites.

    A Site is a bounded volume that can contain none, one, or more atoms.
    This class defines the attributes and methods expected for specific
    Site subclasses.

    Attributes:
        index (int): Numerical ID, intended to be unique to each site.
        label (`str`: optional): Optional string given as a label for this site.
            Default is `None`.
        contains_atoms (list): List of atom indices of the atoms contained by this site in the
            structure last processed.
        trajectory (list): Nested list of indices of atoms that have visited this site at each timestep.
        points (list): List of fractional coordinates for atoms assigned as
            occupying this site.
        transitions (collections.Counter): Stores observed transitions from this
            site to other sites. Format is {index: count} with ``index`` giving
            the index of each destination site, and ``count`` giving the number 
            of observed transitions to this site.
 
    """

    _newid = 0
    # Site._newid provides a counter that is incremented each time a 
    # new site is initialised. This allows each site to have a 
    # unique numerical index.
    # Site._newid can be reset to 0 by calling Site.reset_index()
    # with the default arguments.
    
    def __init__(self, label: Optional[str] = None) -> None:
        """Initialise a Site object.

        Args:
            label (`str`: optional): Optional string used to label this site.

        Retuns:
            None

        """
        self.index: int = Site._newid
        Site._newid += 1
        self.label = label
        self.contains_atoms: List[int] = []
        self.trajectory: List[List[int]] = []
        self.points: List[np.ndarray] = []
        self.transitions: CounterType[int] = Counter()

    def reset(self) -> None:
        """Reset the trajectory for this site.

        Returns the contains_atoms and trajectory attributes
        to empty lists.

        Args:
            None

        Returns:
            None

        """
        self.contains_atoms = []
        self.trajectory = []
        self.transitions = Counter()

    @abstractmethod 
    def contains_point(self, 
                       x: np.ndarray,
                       lattice: Optional[Lattice] = None) -> bool:
        """Test whether the fractional coordinate x is contained by this site.

        This method should be implemented in the inherited subclass

        Args:
            x (np.array): Fractional coordinate.

        Returns:
            (bool)

        Note:
            Specific Site subclasses may require additional arguments to be passed.

        """
        raise NotImplementedError('contains_point should be implemented '
                                  'in the inherited class')

    def contains_atom(self, 
                      atom: Atom, 
                      lattice: Optional[Lattice] = None, 
                      algo: Optional[str] = None) -> bool:
        """Test whether this site contains a specific atom.

        Args:
            atom (Atom): The atom to test.

        Returns:
            (bool)

        """
        return self.contains_point(atom.frac_coords)

    def as_dict(self) -> Dict[str, Any]:
        """Json-serializable dict representation of this Site.

        Args:
            None

        Returns:
            (dict)

        """
        d = {'index': self.index,
             'contains_atoms': self.contains_atoms,
             'trajectory': self.trajectory,
             'points': self.points,
             'transitions': self.transitions}
        if self.label:
            d['label'] = self.label
        return d

    @classmethod
    def from_dict(cls: Type[S], d: Dict['str', Any]) -> S:
        """Create a Site object from a dict representation.

        Args:
            d (dict): The dict representation of this Site.

        Returns:
            (Site)

        """
        site = cls()
        site.index = d['index']
        site.trajectory = d['trajectory']
        site.contains_atoms = d['contains_atoms']
        site.points = d['points']
        site.transitions = d['transitions']
        site.label = d.get('label')
        return site 

    @abstractmethod
    def centre(self) -> np.ndarray:
        """Returns the centre point of this site.

        This method should be implemented in the inherited subclass.

        Args:
            None

        Returns:
            (np.array): (3,) numpy array.

        """ 
        raise NotImplementedError('centre should be implemeneted '
                                  'in the inherited class')

    @abstractmethod
    @property
    def coordination_number(self) -> int:
        """Returns the coordination number of each site.

        This method should be implemented in the inhereted subclass.
        The implementation details will depend on the site type definition.

        Args:
            None

        Returns:
            None

        """
        raise NotImplementedError('coordination_number should be implemented '
                                  'in the inhereted class')

#    def assign_vertex_coords(self, structure: Structure) -> None:
#        """If appropriate, assigns fractional coordinates to the site "vertices"
#        using the corresponding atom positions in a pymatgen Structure.
#   
#        This method should be implemented in the inhereted subclass.
#
#        Args:
#            structure (Structure): The pymatgen Structure used to assign
#                the vertices fractional coordinates.
#
#        Returns:
#            None
#        """
#        raise NotImplementedError('assign_vertex_coords is only implemented'
#                                  'in the PolyhedralSite class')

#    @property
#    def vertex_indices(self) -> List[int]:
#        """If appropriate, returns the list of atom indices for the vertex atoms.
#    
#        This property should be implemented in the inhereted subclass.
#
#        Args:
#            None
#
#        Returns:
#            (list(int))
#
#        """
#        raise NotImplementedError('vertex_indices is only implemented in the'
#                                  'PolyhedralSite class')
 
    @classmethod
    def reset_index(cls, newid: int = 0) -> None:
        """Reset the site index counter.

        Args:
            newid (`int`: optional): New starting index. Default is 1.

        Returns:
            None

        """ 
        Site._newid = newid
