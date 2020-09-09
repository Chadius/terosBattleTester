from unittest import TestCase

from squaddieUseAbilityService import SquaddieUseAbilityService

from ability import Ability, AbilityType, AbilitySpellType, AbilityTarget, AbilityWeaponType
from squaddie import Squaddie


class SquaddieAttackToReduceHitpoints(TestCase):
    def setUp(self):
        self.teros = Squaddie()
        self.teros.setStats({
            "name": "T'eros",
            "maxHP": 5,
            "aim": 1,
            "strength": 1,
            "magic": 2,
            "dodge": 1,
            "armor": 1,
            "barrier": 1,
            "resist": 1,
        })

        self.blot_spell = Ability()
        self.blot_spell.setAttributes({
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

        self.spear = Ability()
        self.spear.setAttributes({
            "name": "spear",
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
            "targets": [AbilityTarget.FOE]
        })

        self.bandit = Squaddie()
        self.bandit.setStats({
            "name": "Bandit level 1",
            "maxHP": 3,
            "aim": 0,
            "strength": 1,
            "magic": 0,
            "dodge": 0,
            "armor": 1,
            "barrier": 0,
            "resist": 0,
        })

    def test_calculate_damage_upon_hit(self):
        damage = SquaddieUseAbilityService.calculate_damage_upon_hit(self.teros, self.blot_spell, self.bandit)
        self.assertEqual(damage, 3)

    def test_damage_resistance_applies(self):
        damage = SquaddieUseAbilityService.calculate_damage_upon_hit(self.teros, self.spear, self.bandit)
        self.assertEqual(damage, 2)

    def test_minimal_damage_is_zero(self):
        indestructible = Squaddie()
        indestructible.setStats({
            "name": "indestructible",
            "maxHP": 3,
            "dodge": 0,
            "armor": 10,
            "barrier": 0,
            "resist": 9001,
        })

        no_damage = SquaddieUseAbilityService.calculate_damage_upon_hit(self.teros, self.blot_spell, indestructible)
        self.assertEqual(no_damage, 0)

        no_damage = SquaddieUseAbilityService.calculate_damage_upon_hit(self.teros, self.spear, indestructible)
        self.assertEqual(no_damage, 0)