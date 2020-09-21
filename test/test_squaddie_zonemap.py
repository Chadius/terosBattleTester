import unittest

from squaddie import Squaddie
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

        self.teros = Squaddie()
        self.teros.set_stats({
            "name": "T'eros",
            "maxHP": 5,
            "aim": 1,
            "strength": 1,
            "magic": 2,
            "dodge": 1,
            "armor": 1,
            "deflect": 1,
            "resist": 1,
        })

    def test_add_squaddie(self):
        self.zone_map.add_squaddie(self.teros, "A")
        squaddies_in_zone = self.zone_map.get_squaddies_in_zone("A")
        self.assertSetEqual(squaddies_in_zone, {self.teros})

    def test_move_squaddie(self):
        self.zone_map.add_squaddie(self.teros, "A")
        self.zone_map.move_squaddie_to_zone(self.teros, "B")

        squaddies_in_start_zone = self.zone_map.get_squaddies_in_zone("A")
        self.assertSetEqual(squaddies_in_start_zone, set())

        squaddies_in_destination_zone = self.zone_map.get_squaddies_in_zone("B")
        self.assertSetEqual(squaddies_in_destination_zone, {self.teros})
