from typing import Set

from squaddie import Squaddie


class Zone(object):
    def __init__(self, size: int):
        self.size = size
        self.squaddies = set()

    def get_size(self) -> int:
        return self.size

    def add_squaddie_to_zone(self, squaddie_to_add: Squaddie) -> None:
        self.squaddies.add(squaddie_to_add)

    def get_squaddies(self) -> Set[Squaddie]:
        return self.squaddies

    def remove_squaddie(self, squaddie_to_remove: Squaddie) -> None:
        self.squaddies.discard(squaddie_to_remove)

    def has_squaddie(self, squaddie_to_find: Squaddie) -> bool:
        return squaddie_to_find in self.squaddies


class ZoneMap(object):
    def __init__(self, name: str):
        self.name = name
        self.zone_by_name = {}
        self.adjacent_zones = {}

    def get_name(self) -> str:
        return self.name

    def add_zone(self, name: str, zone_size: int = 5) -> None:
        self.zone_by_name[name] = Zone(zone_size)

    def get_zone_names(self) -> Set[str]:
        return set(self.zone_by_name.keys())

    def get_zone_by_name(self, name: str) -> Zone:
        return self.zone_by_name.get(name, None)

    def add_squaddie(self, squaddie_to_add: Squaddie, zone_name: str) -> None:
        zone = self.zone_by_name[zone_name]
        zone.add_squaddie_to_zone(squaddie_to_add)

    def get_squaddies_in_zone(self, zone_name: str) -> Set[Squaddie]:
        zone = self.zone_by_name[zone_name]
        return zone.get_squaddies()

    def move_squaddie_to_zone(self, squaddie_to_move: Squaddie, destination_zone_name: str) -> None:
        for zone in self.zone_by_name.values():
            zone.remove_squaddie(squaddie_to_move)
        destination_zone = self.zone_by_name[destination_zone_name]
        destination_zone.add_squaddie_to_zone(squaddie_to_move)

    def get_zone_by_name(self, zone_name: str) -> Zone:
        return self.zone_by_name[zone_name]

    def get_adjacent_zones(self, zone_nane_to_search_from: str) -> Set[Zone]:
        zone = self.get_zone_by_name(zone_nane_to_search_from)
        return self.adjacent_zones.get(zone, set())

    def link_adjacent_zones(self, zone1_name: str, zone2_name: str) -> None:
        zone1 = self.get_zone_by_name(zone1_name)
        zone2 = self.get_zone_by_name(zone2_name)
        if not (zone2 and zone1):
            return

        if not zone1 in self.adjacent_zones:
            self.adjacent_zones[zone1] = set()
        self.adjacent_zones[zone1].add(zone2)

        if not zone2 in self.adjacent_zones:
            self.adjacent_zones[zone2] = set()
        self.adjacent_zones[zone2].add(zone1)

    def get_zone_squaddie_is_in(self, squaddie_to_find: Squaddie) -> Zone:
        for zone in self.zone_by_name.values():
            if zone.has_squaddie(squaddie_to_find):
                return zone
        return None

    def squaddies_are_in_melee(self, squaddie_a: Squaddie, squaddie_b: Squaddie) -> bool:
        zone_squaddie_a_is_in = self.get_zone_squaddie_is_in(squaddie_a)
        zone_squaddie_b_is_in = self.get_zone_squaddie_is_in(squaddie_b)

        if not (zone_squaddie_a_is_in and zone_squaddie_b_is_in):
            return False
        return zone_squaddie_a_is_in == zone_squaddie_b_is_in

    def squaddies_are_at_ranged(self, squaddie_a: Squaddie, squaddie_b: Squaddie) -> bool:
        zone_squaddie_a_is_in = self.get_zone_squaddie_is_in(squaddie_a)
        zone_squaddie_b_is_in = self.get_zone_squaddie_is_in(squaddie_b)

        if not (zone_squaddie_a_is_in and zone_squaddie_b_is_in):
            return False

        return self.are_zones_adjacent(zone_squaddie_a_is_in, zone_squaddie_b_is_in)

    def are_zones_adjacent(self, zone_a: Zone, zone_b: Zone) -> bool:
        zones_adjacent_to_zone_a = self.adjacent_zones.get(zone_a, set())
        return zone_b in zones_adjacent_to_zone_a
