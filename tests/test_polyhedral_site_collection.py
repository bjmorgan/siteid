import unittest
from site_analysis.polyhedral_site_collection import PolyhedralSiteCollection
from site_analysis.polyhedral_site import PolyhedralSite
from unittest.mock import patch, Mock

class PolyhedralSiteCollectionTestCase(unittest.TestCase):

    def test_site_collection_is_initialised(self):
        sites = [Mock(spec=PolyhedralSite), Mock(spec=PolyhedralSite)]
        with patch('site_analysis.polyhedral_site_collection.PolyhedralSiteCollection'
                   '.construct_neighbouring_sites', autospec=True) as mock_construct_neighbouring_sites:
            mock_construct_neighbouring_sites.return_value = 'foo'
            site_collection = PolyhedralSiteCollection(sites=sites)
            self.assertEqual(site_collection.sites, sites)
            self.assertEqual(mock_construct_neighbouring_sites.call_count, 1)
            self.assertEqual(site_collection._neighbouring_sites, 'foo')
       
if __name__ == '__main__':
    unittest.main()
    
