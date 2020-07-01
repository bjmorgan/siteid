from .site import Site
import numpy as np # type: ignore
from typing import Optional, Any, TypeVar, Type, Dict

S = TypeVar('S', bound='VoronoiSite')

class VoronoiSite(Site):
    """Site subclass corresponding to Voronoi cells centered
    on fixed positions.

    Attributes:
        frac_coords (np.array): Fractional coordinates of the site centre.

    """
    
    def __init__(self, 
                 frac_coords: np.ndarray, 
                 label: Optional[str] = None):
        """Create a ``VoronoiSite`` instance.
        
        Args:
            frac_coords (np.array): Fractional coordinates of the site centre.
            label (:str:, optional): Optional label for this site. Default is `None`.

        Returns:
            None

        """
        super(VoronoiSite, self).__init__(label=label)
        self.frac_coords = frac_coords

    def as_dict(self) -> Dict['str', Any]:
        """Json-serializable dict representation of this VoronoiSite.

        Args:
            None

        Returns:
            (dict)

        """
        d = super(VoronoiSite, self).as_dict()
        d['frac_coords'] = self.frac_coords
        return d

    @classmethod
    def from_dict(cls: Type[S], d: Dict['str', Any]) -> S:
        """Create a VoronoiSite object from a dict representation.

        Args:
            d (dict): The dict representation of this Site.

        Returns:
            (VoronoiSite)

        """
        voronoi_site = cls( frac_coords=d['frac_coords'] )
        voronoi_site.label = d.get('label')
        return voronoi_site 

