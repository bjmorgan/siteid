from .site_collection import SiteCollection
import numpy as np # type: ignore
from pymatgen import Structure # type: ignore
from typing import List
from .atom import Atom

class SphericalSiteCollection(SiteCollection):

    def analyse_structure(self, 
                          atoms: List[Atom], 
                          structure: Structure) -> None:
        for a in atoms:
            a.assign_coords(structure)
        self.assign_site_occupations(atoms, structure)

    def assign_site_occupations(self, 
                                atoms: List[Atom], 
                                structure: Structure) -> None:
        self.reset_site_occupations()
        for atom in atoms:
            if atom.in_site:
                # first check the site last occupied
                previous_site = next(s for s in self.sites if s.index == atom.in_site)
                if previous_site.contains_atom(atom, structure.lattice):
                    self.update_occupation( previous_site, atom )
                    continue # atom has not moved
                else: # default is atom does not occupy any sites
                    atom.in_site = None
            for s in self.sites:
                if s.contains_atom(atom, structure.lattice):
                    self.update_occupation( s, atom )
                    break

 
