import unittest
from site_analysis.site import Site
from site_analysis.atom import Atom
from unittest.mock import patch, MagicMock, Mock
import numpy as np
from collections import Counter

class SiteTestCase(unittest.TestCase):

    @patch.multiple(Site, __abstractmethods__=set())
    def setUp(self):
        Site._newid = 0
        self.site = Site()

    def test_site_is_initialised(self):
        site = self.site
        self.assertEqual(site.index, 0)
        self.assertEqual(site.label, None)
        self.assertEqual(site.contains_atoms, [])
        self.assertEqual(site.trajectory, [])
        self.assertEqual(site.points, [])
        self.assertEqual(site.transitions, {})

    @patch.multiple(Site, __abstractmethods__=set())
    def test_site_is_initialised_with_label(self):
        site = Site(label='foo')
        self.assertEqual(site.label, 'foo')

    @patch.multiple(Site, __abstractmethods__=set())
    def test_site_index_autoincrements(self):
        site1 = Site()
        site2 = Site()
        self.assertEqual(site2.index, site1.index + 1)

    def test_reset(self):
        site = self.site
        site.contains_atoms = ['foo']
        site.trajectory = ['bar']
        site.transitions = Counter([4])
        site.reset()
        self.assertEqual(site.trajectory, [])
        self.assertEqual(site.contains_atoms, [])
        self.assertEqual(site.transitions, {})

    def test_centre_raises_not_implemented_error(self):
        site = self.site
        with self.assertRaises(NotImplementedError):
            site.centre()

    @patch.multiple(Site, __abstractmethods__=set())
    def test_as_dict(self):
        site = self.site
        site.index = 7
        site.contains_atoms = [3]
        site.trajectory = [10,11,12]
        site.points = [np.array([0,0,0])]
        site.label = 'foo'
        site.transitions = Counter([3,3,2])
        site_dict = site.as_dict()
        expected_dict = {'index': 7,
                         'contains_atoms': [3],
                         'trajectory': [10,11,12],
                         'points': [np.array([0,0,0])],
                         'label': 'foo',
                         'transitions': Counter([3,3,2])}
        self.assertEqual(site.index, expected_dict['index'])
        self.assertEqual(site.contains_atoms, expected_dict['contains_atoms'])
        self.assertEqual(site.trajectory, expected_dict['trajectory'])
        np.testing.assert_array_equal(site.points, expected_dict['points'])
        self.assertEqual(site.label, expected_dict['label'])
        self.assertEqual(site.transitions, expected_dict['transitions'])

    @patch.multiple(Site, __abstractmethods__=set())
    def test_reset_index(self):
        Site._newid = 7
        site = Site()
        self.assertEqual(site.index, 7)
        Site.reset_index()
        site = Site()
        self.assertEqual(site.index, 0)
        
    @patch.multiple(Site, __abstractmethods__=set())
    def test_reset_index_to_defined_index(self):
        Site._newid = 7
        site = Site()
        self.assertEqual(site.index, 7)
        Site.reset_index(newid=12)
        site = Site()
        self.assertEqual(site.index, 12)
   
    @patch.multiple(Site, __abstractmethods__=set())
    def test_from_dict(self):
        site_dict = {'index': 7,
                     'contains_atoms': [3],
                     'trajectory': [10,11,12],
                     'points': [np.array([0,0,0])],
                     'label': 'foo',
                     'transitions': Counter([3,3,2])}
        site = Site.from_dict(site_dict)
        self.assertEqual(site.index, site_dict['index'])
        self.assertEqual(site.contains_atoms, site_dict['contains_atoms'])
        self.assertEqual(site.trajectory, site_dict['trajectory'])
        np.testing.assert_array_equal(site.points, site_dict['points'])
        self.assertEqual(site.label, site_dict['label'])
        self.assertEqual(site.transitions, site_dict['transitions'])
     
if __name__ == '__main__':
    unittest.main()
    
