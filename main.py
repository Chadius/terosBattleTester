from ability import Ability, AbilityType, AbilitySpellType, AbilityTarget, AbilityWeaponType
from squaddie import Squaddie
from zone_map import ZoneMap


class SquaddieFactory:
    @classmethod
    def create_teros(cls):
        teros = Squaddie()
        teros.set_stats({
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
        return teros

    @classmethod
    def create_necromancer(cls):
        necromancer = Squaddie()
        necromancer.set_stats({
            "name": "Necromancer level 1",
            "maxHP": 3,
            "aim": 0,
            "strength": 1,
            "magic": 0,
            "dodge": 0,
            "armor": 0,
            "deflect": 1,
            "resist": 0,
        })
        return necromancer

    @classmethod
    def create_bandit(cls):
        bandit = Squaddie()
        bandit.set_stats({
            "name": "Bandit level 1",
            "maxHP": 3,
            "aim": 0,
            "strength": 1,
            "magic": 0,
            "dodge": 0,
            "armor": 1,
            "deflect": 0,
            "resist": 0,
        })
        return bandit


class AbilityFactory:
    @classmethod
    def create_blot_spell(cls):
        blot_spell = Ability()
        blot_spell.set_attributes({
            "name": "blot",
            "level": 0,
            "type": AbilityType.SPELL,
            "subtype": AbilitySpellType.ANCIENT,
            "minRange": 1,
            "maxRange": 2,
            "splashRadius": None,
            "aim": 1,
            "damage": 1,
            "durability": 10,
            "canDealCriticalHits": False,
            "criticalHitNumber": None,
            "targets": [AbilityTarget.FOE]
        })
        return blot_spell

    @classmethod
    def create_spear(cls):
        spear = Ability()
        spear.set_attributes({
            "name": "spear",
            "level": 0,
            "type": AbilityType.WEAPON,
            "subtype": AbilityWeaponType.SPEAR,
            "minRange": 1,
            "maxRange": 2,
            "splashRadius": None,
            "aim": 1,
            "damage": 2,
            "durability": 10,
            "canDealCriticalHits": True,
            "criticalHitNumber": 2,
            "canCounterAttack": True,
            "targets": [AbilityTarget.FOE]
        })
        return spear

    @classmethod
    def create_sword(cls):
        sword = Ability()
        sword.set_attributes({
            "name": "sword",
            "level": 0,
            "type": AbilityType.WEAPON,
            "subtype": AbilityWeaponType.SWORD,
            "minRange": 1,
            "maxRange": 2,
            "splashRadius": None,
            "aim": 1,
            "damage": 2,
            "durability": 10,
            "canDealCriticalHits": True,
            "criticalHitNumber": 2,
            "canCounterAttack": True,
            "targets": [AbilityTarget.FOE]
        })
        return sword

    @classmethod
    def create_axe(cls):
        axe = Ability()
        axe.set_attributes({
            "name": "axe",
            "level": 0,
            "type": AbilityType.WEAPON,
            "subtype": AbilityWeaponType.AXE,
            "minRange": 1,
            "maxRange": 2,
            "splashRadius": None,
            "aim": 1,
            "damage": 2,
            "durability": 10,
            "canDealCriticalHits": True,
            "criticalHitNumber": 2,
            "canCounterAttack": True,
            "targets": [AbilityTarget.FOE]
        })
        return axe

    @classmethod
    def create_bow(cls):
        bow = Ability()
        bow.set_attributes({
            "name": "bow",
            "level": 0,
            "type": AbilityType.WEAPON,
            "subtype": AbilityWeaponType.BOW,
            "minRange": 1,
            "maxRange": 3,
            "splashRadius": None,
            "aim": 1,
            "damage": 2,
            "durability": 10,
            "canDealCriticalHits": True,
            "criticalHitNumber": 2,
            "canCounterAttack": True,
            "targets": [AbilityTarget.FOE]
        })
        return bow


class MissionRunner():
    def __init__(self):
        self.zone_map: ZoneMap = None
        self.teros: Squaddie = None
        self.bandit: Squaddie = None
        self.blot_spell: Ability = None
        self.axe: Ability = None

    def set_up_map(self):
        self.zone_map = ZoneMap("The map")
        self.zone_map.add_zone("A")
        self.zone_map.add_zone("B")
        self.zone_map.add_zone("C")

        self.zone_map.link_adjacent_zones("A", "B")
        self.zone_map.link_adjacent_zones("B", "C")

        self.teros = SquaddieFactory.create_teros()
        self.bandit = SquaddieFactory.create_bandit()

        self.blot_spell = AbilityFactory.create_blot_spell()
        self.spear = AbilityFactory.create_spear()
        self.teros.add_ability(self.blot_spell)
        self.teros.equip_ability(self.blot_spell)

        self.bandit.add_ability(self.spear)
        self.bandit.equip_ability(self.spear)

        self.zone_map.add_squaddie(self.teros, "A")
        self.zone_map.add_squaddie(self.bandit, "A")

    def print_map(self):
        log("The Map:")
        for zone_name in self.zone_map.get_zone_names():
            log("")
            zone = self.zone_map.get_zone_by_name(zone_name)
            squaddies_in_zone = zone.get_squaddies()
            log(f"{zone_name} Number of Squaddies in zone: {len(squaddies_in_zone)}")
            for squaddie in squaddies_in_zone:
                log(f"{squaddie.get_name()}: {squaddie.get_expected_current_hp()}")
            log(f"Neighboring zones: {self.zone_map.get_adjacent_zones(zone_name)}")


def log(message):
    print(message)


def main():
    mission = MissionRunner()
    mission.set_up_map()
    mission.print_map()


if __name__ == '__main__':
    main()