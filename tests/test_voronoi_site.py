import unittest
from site_analysis.voronoi_site import VoronoiSite
from unittest.mock import patch, MagicMock, Mock
import numpy as np

class VoronoiSiteTestCase(unittest.TestCase):

    def test_voronoi_site_is_initialised(self):
        frac_coords = np.array([0.1, 0.2, 0.3])
        site = VoronoiSite(frac_coords=frac_coords)
        np.testing.assert_array_equal(site.frac_coords, frac_coords)
        self.assertEqual(site.label, None)

    def test_voronoi_site_is_initialised_with_label(self):
        frac_coords = np.array([0.1, 0.2, 0.3])
        site = VoronoiSite(frac_coords=frac_coords, label='foo')
        np.testing.assert_array_equal(site.frac_coords, frac_coords)
        self.assertEqual(site.label, 'foo')

    def test_as_dict(self):
        frac_coords = np.array([0.1, 0.2, 0.3])
        site = VoronoiSite(frac_coords=frac_coords)
        site_dict = site.as_dict()
        np.testing.assert_array_equal(site_dict['frac_coords'], frac_coords)
   
    def test_from_dict(self):
        site_dict = {'frac_coords': np.array([0.1, 0.2, 0.3])}
        with patch('site_analysis.site.Site.from_dict') as mock_from_dict:
            with patch('site_analysis.site.Site.set_attributes_from_dict') as mock_set_attributes_from_dict:
                mock_from_dict.return_value = {}
                site = VoronoiSite.from_dict(site_dict)
        np.testing.assert_array_equal(site.frac_coords, site_dict['frac_coords'])

if __name__ == '__main__':
    unittest.main()
    
