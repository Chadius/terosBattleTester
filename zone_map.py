from typing import Set


class Zone(object):
    def __init__(self, size: int):
        self.size = size

    def get_size(self) -> int:
        return self.size


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
