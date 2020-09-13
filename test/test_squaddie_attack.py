from unittest import TestCase

from squaddieUseAbilityService import SquaddieUseAbilityService

from ability import Ability, AbilityType, AbilitySpellType, AbilityTarget, AbilityWeaponType
from squaddie import Squaddie


class SquaddieAttackToReduceHitpoints(TestCase):
    def setUp(self):
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

        self.blot_spell = Ability()
        self.blot_spell.set_attributes({
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
        self.spear.set_attributes({
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
            "targets": [AbilityTarget.FOE]
        })

        self.bandit = Squaddie()
        self.bandit.set_stats({
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

    def test_calculate_damage_upon_hit(self):
        damage = SquaddieUseAbilityService.calculate_damage_upon_hit(self.teros, self.blot_spell, self.bandit)
        self.assertEqual(damage, 3)

    def test_damage_resistance_applies(self):
        damage = SquaddieUseAbilityService.calculate_damage_upon_hit(self.teros, self.spear, self.bandit)
        self.assertEqual(damage, 2)

    def test_minimal_damage_is_zero(self):
        indestructible = Squaddie()
        indestructible.set_stats({
            "name": "indestructible",
            "maxHP": 3,
            "dodge": 0,
            "armor": 10,
            "deflect": 0,
            "resist": 9001,
        })

        no_damage = SquaddieUseAbilityService.calculate_damage_upon_hit(self.teros, self.blot_spell, indestructible)
        self.assertEqual(no_damage, 0)

        no_damage = SquaddieUseAbilityService.calculate_damage_upon_hit(self.teros, self.spear, indestructible)
        self.assertEqual(no_damage, 0)


class SquaddieCalculateChanceToHit(TestCase):
    def setUp(self):
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

        self.blot_spell = Ability()
        self.blot_spell.set_attributes({
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
        self.spear.set_attributes({
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
            "targets": [AbilityTarget.FOE]
        })

        self.necromancer = Squaddie()
        self.necromancer.set_stats({
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

    def test_calculate_chance_to_dodge(self):
        chance_to_hit = SquaddieUseAbilityService.calculate_chance_hit(self.teros, self.blot_spell, self.necromancer)
        self.assertEqual(chance_to_hit, 1)

    def test_ability_type_affects_chance_to_evade(self):
        chance_to_hit = SquaddieUseAbilityService.calculate_chance_hit(self.teros, self.spear, self.necromancer)
        self.assertEqual(chance_to_hit, 2)

    def test_calculate_chance_to_dodge_with_advantage(self):
        chance_to_hit = SquaddieUseAbilityService.calculate_chance_hit(
            self.teros,
            self.blot_spell,
            self.necromancer,
            {"hasAdvantage": True}
        )
        self.assertEqual(chance_to_hit, 2)

    def test_calculate_chance_to_dodge_with_disadvantage(self):
        chance_to_hit = SquaddieUseAbilityService.calculate_chance_hit(
            self.teros,
            self.blot_spell,
            self.necromancer,
            {"hasDisadvantage": True}
        )
        self.assertEqual(chance_to_hit, 0)

    def test_calculate_chance_to_dodge_with_counter(self):
        chance_to_hit = SquaddieUseAbilityService.calculate_chance_hit(
            self.teros,
            self.blot_spell,
            self.necromancer,
            {"isCounterAttack": True}
        )
        self.assertEqual(chance_to_hit, -1)

    def test_calculate_chance_to_dodge_when_attack_too_close(self):
        chance_to_hit = SquaddieUseAbilityService.calculate_chance_hit(
            self.teros,
            self.blot_spell,
            self.necromancer,
            {"tooClose": True}
        )
        self.assertEqual(chance_to_hit, 0)


class DetectAdvantageBasedOnEquippedWeapons(TestCase):
    def setUp(self) -> None:
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

        self.blot_spell = Ability()
        self.blot_spell.set_attributes({
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
        self.spear.set_attributes({
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
            "targets": [AbilityTarget.FOE]
        })

        self.bandit = Squaddie()
        self.bandit.set_stats({
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

        self.sword = Ability()
        self.sword.set_attributes({
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
            "targets": [AbilityTarget.FOE]
        })

        self.axe = Ability()
        self.axe.set_attributes({
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
            "targets": [AbilityTarget.FOE]
        })

    def test_no_advantage_or_disadvantage_for_different_types(self):
        self.assertFalse(SquaddieUseAbilityService.has_advantage_due_to_ability(self.spear, self.blot_spell))
        self.assertFalse(SquaddieUseAbilityService.has_disadvantage_due_to_ability(self.spear, self.blot_spell))

    def test_advantage_with_weapons(self):
        self.assertTrue(SquaddieUseAbilityService.has_advantage_due_to_ability(self.spear, self.sword))
        self.assertTrue(SquaddieUseAbilityService.has_advantage_due_to_ability(self.sword, self.axe))
        self.assertTrue(SquaddieUseAbilityService.has_advantage_due_to_ability(self.axe, self.spear))

        self.assertFalse(SquaddieUseAbilityService.has_advantage_due_to_ability(self.spear, self.axe))
        self.assertFalse(SquaddieUseAbilityService.has_advantage_due_to_ability(self.sword, self.spear))
        self.assertFalse(SquaddieUseAbilityService.has_advantage_due_to_ability(self.axe, self.sword))

        self.assertFalse(SquaddieUseAbilityService.has_advantage_due_to_ability(self.spear, self.spear))
        self.assertFalse(SquaddieUseAbilityService.has_advantage_due_to_ability(self.sword, self.sword))
        self.assertFalse(SquaddieUseAbilityService.has_advantage_due_to_ability(self.axe, self.axe))

    def test_disadvantage_with_weapons(self):
        self.assertTrue(SquaddieUseAbilityService.has_disadvantage_due_to_ability(self.spear, self.axe))
        self.assertTrue(SquaddieUseAbilityService.has_disadvantage_due_to_ability(self.sword, self.spear))
        self.assertTrue(SquaddieUseAbilityService.has_disadvantage_due_to_ability(self.axe, self.sword))

        self.assertFalse(SquaddieUseAbilityService.has_disadvantage_due_to_ability(self.spear, self.sword))
        self.assertFalse(SquaddieUseAbilityService.has_disadvantage_due_to_ability(self.sword, self.axe))
        self.assertFalse(SquaddieUseAbilityService.has_disadvantage_due_to_ability(self.axe, self.spear))

        self.assertFalse(SquaddieUseAbilityService.has_disadvantage_due_to_ability(self.spear, self.spear))
        self.assertFalse(SquaddieUseAbilityService.has_disadvantage_due_to_ability(self.sword, self.sword))
        self.assertFalse(SquaddieUseAbilityService.has_disadvantage_due_to_ability(self.axe, self.axe))


class CalculateExpectedDamage(TestCase):
    def setUp(self):
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

        self.blot_spell = Ability()
        self.blot_spell.set_attributes({
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
        self.spear.set_attributes({
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
            "targets": [AbilityTarget.FOE]
        })

        self.necromancer = Squaddie()
        self.necromancer.set_stats({
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

        self.bandit = Squaddie()
        self.bandit.set_stats({
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

    def test_calculate_expected_chance_to_hit(self):
        expected_chance_to_hit_with_magic = SquaddieUseAbilityService.calculate_expected_chance_hit(self.teros,
                                                                                                    self.blot_spell,
                                                                                                    self.necromancer)
        self.assertEqual(expected_chance_to_hit_with_magic, 26)

        expected_chance_to_hit_with_physical = SquaddieUseAbilityService.calculate_expected_chance_hit(self.teros,
                                                                                                       self.spear,
                                                                                                       self.necromancer)
        self.assertEqual(expected_chance_to_hit_with_physical, 30)

    def test_calculate_expected_crit_damage(self):
        expected_crit_damage_with_crit_possible = SquaddieUseAbilityService.calculate_expected_crit_damage(self.teros,
                                                                                                           self.spear,
                                                                                                           self.necromancer)
        self.assertEqual(expected_crit_damage_with_crit_possible, 1 * 3)

        expected_crit_damage_with_no_crit_possible = SquaddieUseAbilityService.calculate_expected_crit_damage(
            self.teros, self.blot_spell, self.bandit)
        self.assertEqual(expected_crit_damage_with_no_crit_possible, 0)
