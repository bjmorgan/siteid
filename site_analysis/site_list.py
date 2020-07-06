from typing import TypeVar, Generic, List, Union
from .site import Site
from .polyhedral_site import PolyhedralSite
from .voronoi_site import VoronoiSite
from .spherical_site import SphericalSite
from collections import Sequence

#T = TypeVar('T')
SiteList = Union[List[PolyhedralSite], List[VoronoiSite], List[SphericalSite]]

#class SiteList(List[AnySite]):
#
#    def __init__(self) -> None:
#        self.sites: List[AnySite] = []

