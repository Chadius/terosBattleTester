from unittest import TestCase

from ability import Ability, AbilityType, AbilitySpellType, AbilityTarget
from squaddie import Squaddie


class SquaddieStats(TestCase):
    def testCreateSquaddie(self):
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
        self.assertEqual(teros.get_name(), "T'eros")
        self.assertEqual(teros.get_max_hp(), 5)
        self.assertEqual(teros.get_expected_max_hp(), 180)
        self.assertEqual(teros.get_expected_current_hp(), 180)
        self.assertEqual(teros.get_aim(), 1)
        self.assertEqual(teros.get_strength(), 1)
        self.assertEqual(teros.get_magic(), 2)
        self.assertEqual(teros.get_armor(), 1)
        self.assertEqual(teros.get_dodge(), 1)
        self.assertEqual(teros.get_deflect(), 1)
        self.assertEqual(teros.get_resist(), 1)

    def testSquaddieCanTakeExpectedDamage(self):
        i_am_alive = Squaddie()
        i_am_alive.set_stats({
            "name": "I am alive",
            "maxHP": 3,
        })
        self.assertEqual(i_am_alive.get_expected_max_hp(), 108)
        self.assertEqual(i_am_alive.get_expected_current_hp(), 108)

        i_am_alive.take_expected_damage(8)

        self.assertEqual(i_am_alive.get_expected_max_hp(), 108)
        self.assertEqual(i_am_alive.get_expected_current_hp(), 100)

        i_am_alive.take_expected_damage(108)
        self.assertEqual(i_am_alive.get_expected_current_hp(), 0)


class AbilityCreation(TestCase):
    def testCreateAbility(self):
        attributes_to_test = {
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
        }

        blot_spell = Ability()
        blot_spell.set_attributes(attributes_to_test)

        self.assertEqual(blot_spell.get_name(), "blot")
        self.assertEqual(blot_spell.get_level(), 0)
        self.assertEqual(blot_spell.get_type(), AbilityType.SPELL)
        self.assertEqual(blot_spell.get_subtype(), AbilitySpellType.ANCIENT)
        self.assertEqual(blot_spell.get_min_range(), 1)
        self.assertEqual(blot_spell.get_max_range(), 2)
        self.assertEqual(blot_spell.get_splash_radius(), None)
        self.assertEqual(blot_spell.get_aim_bonus(), 1)
        self.assertEqual(blot_spell.get_damage(), 1)
        self.assertEqual(blot_spell.get_max_durability(), 10)
        self.assertEqual(blot_spell.can_deal_critical_hits(), False)
        self.assertEqual(blot_spell.can_counter_attack(), False)
        self.assertEqual(blot_spell.get_critical_hit_number(), None)
        self.assertEqual(len(blot_spell.get_targets()), 1)
        self.assertTrue(AbilityTarget.FOE in blot_spell.get_targets())

        sword = Ability()
        sword.set_attributes({**attributes_to_test, 'canCounterAttack': True})
        self.assertTrue(sword.can_counter_attack())


class SquaddieCanEquipAndUseAbility(TestCase):
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

        self.bandit = Squaddie()
        self.bandit.set_stats({
            "name": "Bandit level 1",
            "maxHP": 3,
            "aim": 0,
            "strength": 1,
            "magic": 0,
            "dodge": 0,
            "armor": 0,
            "deflect": 0,
            "resist": 0,
        })

    def testSquaddieCanAddAbility(self):
        self.teros.add_ability(self.blot_spell)

        self.assertEqual(len(self.teros.get_abilities()), 1)
        self.assertTrue("blot" in self.teros.get_ability_names())

        self.assertEqual(len(self.bandit.get_abilities()), 0)

    def testSquaddieUsesAbilityToDealExpectedDamage(self):
        self.teros.add_ability(self.blot_spell)
        self.teros.use_ability(self.blot_spell, self.bandit)
        self.assertTrue(self.bandit.get_expected_current_hp() < self.bandit.get_expected_max_hp())

    def testSquaddieCanEquipAbility(self):
        self.teros.add_ability(self.blot_spell)
        self.teros.equip_ability(self.blot_spell)
        self.assertEqual("blot", self.teros.get_equipped_ability().get_name())

    def testSquaddieUsingAnAbilityEquipsIt(self):
        self.teros.add_ability(self.blot_spell)
        self.assertIsNone(self.teros.get_equipped_ability())
        self.teros.use_ability(self.blot_spell, self.bandit)
        self.assertEqual("blot", self.teros.get_equipped_ability().get_name())
