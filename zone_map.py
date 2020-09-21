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


class ZoneMap(object):
    def __init__(self, name: str):
        self.name = name
        self.zone_by_name = {}

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
