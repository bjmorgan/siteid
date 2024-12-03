"""site_analysis.tools module

This module contains tools for [TODO]

"""
import numpy as np

from typing import Optional, List, Union, Tuple
from pymatgen.core import Structure
from .atom import Atom
from .site import Site

def get_nearest_neighbour_indices(
        structure: Structure,
        ref_structure: Structure,
        vertex_species: List[str],
        n_coord: int) -> List[List[int]]:
    """
    Returns the atom indices for the N nearest neighbours to each site in a reference
    structure.

    Args:
        structure (`pymatgen.Structure`): A pymatgen Structure object, used to select
            the nearest neighbour indices.
        ref_structure (`pymatgen.Structure`): A pymatgen Structure object. Each site
            is used to find the set of N nearest neighbours (of the specified atomic species)
            in ``structure``.
        vertex_species (list(str)): List of strings specifying the atomic species of
            the vertex atoms, e.g. ``[ 'S', 'I' ]``.
        n_coord (int): Number of matching nearest neighbours to return for each site in 
            ``ref_structure``.

    Returns:
        (list(list(int)): N_sites x N_neighbours nested list of vertex atom indices.

    """
    vertex_indices = [i for i, s in enumerate(structure)
            if s.species_string in vertex_species]
    struc1_coords = np.array([structure[i].frac_coords for i in vertex_indices])
    struc2_coords = ref_structure.frac_coords
    lattice = structure[0].lattice
    dr_ij = lattice.get_all_distances(struc1_coords, struc2_coords).T
    nn_indices = []
    for dr_i in dr_ij:
        idx = np.argpartition(dr_i, n_coord)
        nn_indices.append( sorted([ vertex_indices[i] for i in idx[:n_coord] ]) )
    return nn_indices

def get_vertex_indices(
        structure: Structure,
        centre_species: str,
        vertex_species: Union[str, List[str]],
        cutoff: float=4.5,
        n_vertices: Union[int, List[int]]=6) -> List[List[int]]:
    """
    Find the atom indices for atoms defining the vertices of coordination polyhedra, from 
    a pymatgen Structure object.

    Given the elemental species of a set of central atoms, A, 
    and of the polyhedral vertices, B, this function finds:
    for each A, then N closest neighbours B (within some cutoff).
    The number of neighbours found per central atom can be a single
    value for all A, or can be provided as a list of values for each A.

    Args:
        structure (`pymatgen.Structure`): A pymatgen Structure object, used to
            find the coordination polyhedra vertices..
        centre_species (str): Species string identifying the atoms at the centres
            of each coordination environment, e.g. "Na".
        vertex_species (str or list(str)): Species string identifying the atoms at the vertices
            of each coordination environment, e.g. "S"., or a list of strings, e.g. ``["S", "I"]``.
        cutoff (float): Distance cutoff for neighbour search.
        n_vertices (int or list(int)): Number(s) of nearest neighbours to return
            for each set of vertices. If a list is passed, this should be the same
            length as the number of atoms of centre species A.

    Returns:
        list(list(int)): Nested list of integers, giving the atom indices for each
            coordination environment.

    """
    central_sites = [ s for s in structure if s.species_string == centre_species ]
    if isinstance(n_vertices, int):
        n_vertices = [n_vertices] * len(central_sites)
    if isinstance(vertex_species, str):
        vertex_species = [ vertex_species ]
    vertex_indices = []
    for site, n_vert in zip(central_sites, n_vertices):
        neighbours = [ s for s in structure.get_neighbors(site, r=cutoff, include_index=True) 
                       if s[0].species_string in vertex_species ]
        neighbours.sort(key=lambda x: x[1])
        atom_indices = [ n[2] for n in neighbours[:n_vert] ]
        vertex_indices.append( atom_indices )
    return vertex_indices

def x_pbc(x: np.ndarray):
    """Return an array of fractional coordinates mapped into all positive neighbouring 
    periodic cells.

    Args:
        x (np.array): Input fractional coordinates.

    Returns:
        np.array: (9,3) numpy array of all mapped fractional coordinates, including the
                  original coordinates in the origin calculation cell.

    Example:
        >>> x = np.array([0.1, 0.2, 0.3])
        >>> x_pbc(x)
        array([[0.1, 0.2, 0.3],
               [1.1, 0.2, 0.3],
               [0.1, 1.2, 0.3],
               [0.1, 0.2, 1.3],
               [1.1, 1.2, 0.3],
               [1.1, 0.2, 1.3],
               [0.1, 1.2, 1.3],
               [1.1, 1.2, 1.3]])

    """       
    all_x =  np.array([[0,0,0],
                       [1,0,0],
                       [0,1,0],
                       [0,0,1],
                       [1,1,0],
                       [1,0,1],
                       [0,1,1],
                       [1,1,1]]) + x
    return all_x

def fractional_min_pbc_distance(coord1: np.ndarray, coord2: np.ndarray) -> float:
    """
    Calculate the minimum distance between two points in fractional coordinates considering PBC.

    Args:
        coord1 (np.ndarray): Fractional coordinates of the first point.
        coord2 (np.ndarray): Fractional coordinates of the second point.

    Returns:
        float: The minimum distance between the two points in fractional space considering PBC.
    """
    delta = coord2 - coord1
    delta -= np.round(delta)  # Apply PBC: shift to [-0.5, 0.5]

    # Calculate the distance in fractional coordinates
    distance = np.linalg.norm(delta)

    return distance


def species_string_from_site(site: Site):
    return [k.__str__() for k in site._species.keys()][0]

def generate_site_atom_distance_matrix(sites: List[Site], atoms: List[Atom]) -> np.ndarray:
    """
    Generate a distance matrix between all sites and all atoms.

    Args:
        sites (List[Site]): List of sites.
        atoms (List[Atom]): List of atoms.

    Returns:
        np.ndarray: A 2D distance matrix where each element [i, j] is the distance
        between the i-th site and the j-th atom.
    """
    # Extract fractional coordinates for sites and atoms
    site_coords = np.array([site.centre() for site in sites])
    atom_coords = np.array([atom.frac_coords for atom in atoms])

    # Apply PBC and calculate distances
    delta = atom_coords - site_coords[:, np.newaxis]
    delta -= np.round(delta)
    distance_matrix = np.sqrt(np.einsum('ijk,ijk->ij', delta, delta))

    return distance_matrix

def generate_structure_distance_matrix(structure: Structure,
                                    return_cartesian: bool = True) -> np.ndarray:
    """
    Generate a distance matrix for all sites within the structure,
    considering periodic boundary conditions.

    Args:
        structure (Structure): The structure to generate a distance matrix for.
        return_cartesian (bool): If True, uses Cartesian distances for mapping; 
                                otherwise, fractional distances are returned.

    Returns:
        np.ndarray: A 2D distance matrix where each element [i, j] is the distance 
                    between the i-th and j-th site, respecting PBC.
    """
    frac_coords = structure.frac_coords

    delta = frac_coords[np.newaxis, :] - frac_coords[:, np.newaxis]
    delta -= np.round(delta)  

    if return_cartesian:
        # Convert to Cartesian coordinates
        lattice_matrix = structure.lattice.matrix
        delta_cart = np.einsum('ijk,kl->ijl', delta, lattice_matrix)
        distance_matrix = np.sqrt(np.einsum('ijk,ijk->ij', delta_cart, delta_cart))
    else:
        # Use fractional coordinates directly
        distance_matrix = np.sqrt(np.einsum('ijk,ijk->ij', delta, delta))

    return distance_matrix

def site_index_mapping(structure1: Structure, 
                       structure2: Structure,
                       species1: Optional[Union[str, List[str]]] = None,
                       species2: Optional[Union[str, List[str]]] = None,
                       one_to_one_mapping: Optional[bool] = True,
                       return_mapping_distances: Optional[bool] = False) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
    """Compute the site index mapping between two structures based on the closest corresponding site in
    structure2 to each selected site in structure1.
    
    Args:
        structure1 (pymatgen.Structure): The structure to map from.
        structure2 (pymatgen.Structure): The structure to map to.
        species1 (optional, str or list(str)): Optional argument to select a subset of atomic species
            to map site indices from.
        species2 (optional, str of list(str)): Optional argument to specify a subset of atomic species
            to map site indices to.
        one_to_one_mapping (optional, bool): Optional argument to check that a one-to-one mapping is found
            between the relevant subsets of sites in structure1 and structure2. Default is `True`.
            
    Returns:
        np.ndarray
        
    Raises:
        ValueError: if `one_to_one_mapping = True` and a one-to-one mapping is not found.
 
    """
    # Ensure species1 and species2 are lists of site species strings.
    if species1 is None:
        species1 = list(set([site.species_string for site in structure1]))
    if isinstance(species1, str):
        species1 = [species1]
    if isinstance(species2, str):
        species2 = [species2]
    if species2 is None:
        species2 = list(set([site.species_string for site in structure2]))
    assert(isinstance(species1, list))
    assert(isinstance(species2, list))
    
    structure2_mask = np.array([site.species_string in species2 for site in structure2])
    lattice = structure1.lattice
    dr_ij = np.array(lattice.get_all_distances(structure1.frac_coords, structure2.frac_coords))
    to_return = []
    dr_ij_to_return = []
    for site1, dr_i in zip(structure1, dr_ij):
        if site1.species_string in species1:
                subset_idx = np.argmin(dr_i[structure2_mask])
                parent_idx = np.arange(len(dr_i))[structure2_mask][subset_idx] 
                to_return.append(parent_idx)
                dr_ij_to_return.append(dr_i[parent_idx])
    if one_to_one_mapping:
        if len(to_return) != len(set(to_return)):
            raise ValueError("One-to-one mapping between structures not found.")   
    if return_mapping_distances:
        return np.array(to_return), np.array(dr_ij_to_return)     
    else:
        return np.array(to_return)
