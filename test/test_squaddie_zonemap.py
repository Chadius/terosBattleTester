import unittest

from zone_map import ZoneMap


class MapHasZones(unittest.TestCase):
    def setUp(self):
        self.zone_map = ZoneMap("The map")

    def test_map_can_set_name(self):
        self.assertEqual(self.zone_map.get_name(), "The map")

    def test_map_can_add_zones(self):
        self.zone_map.add_zone("A")
        self.zone_map.add_zone("B")
        self.zone_map.add_zone("C")

        self.assertSetEqual(self.zone_map.get_zone_names(), {"A", "B", "C"})

    def test_zone_has_default_size(self):
        self.zone_map.add_zone("5 wide")
        five_wide_zone = self.zone_map.get_zone_by_name("5 wide")

        self.assertEqual(five_wide_zone.get_size(), 5)

    def test_zone_can_specify_size(self):
        self.zone_map.add_zone("6 wide", 6)
        six_wide_zone = self.zone_map.get_zone_by_name("6 wide")

        self.assertEqual(six_wide_zone.get_size(), 6)


class MapCanAddSquaddies(unittest.TestCase):
    def setUp(self):
        self.zone_map = ZoneMap("The map")
        self.zone_map.add_zone("A")
        self.zone_map.add_zone("B")