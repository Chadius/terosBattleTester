from unittest import TestCase

from ability import Ability, AbilityType, AbilitySpellType, AbilityTarget
from squaddie import Squaddie


class SquaddieStats(TestCase):
    def testCreateSquaddie(self):
        teros = Squaddie()
        teros.setStats({
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
        self.assertEqual(teros.getName(), "T'eros")
        self.assertEqual(teros.getMaxHP(), 5)
        self.assertEqual(teros.getExpectedMaxHP(), 180)
        self.assertEqual(teros.getExpectedCurrentHP(), 180)
        self.assertEqual(teros.getAim(), 1)
        self.assertEqual(teros.getStrength(), 1)
        self.assertEqual(teros.getMagic(), 2)
        self.assertEqual(teros.getArmor(), 1)
        self.assertEqual(teros.getDodge(), 1)
        self.assertEqual(teros.getBarrier(), 1)
        self.assertEqual(teros.getResist(), 1)

    def testSquaddieCanTakeExpectedDamage(self):
        i_am_alive = Squaddie()
        i_am_alive.setStats({
            "name": "I am alive",
            "maxHP": 3,
        })
        self.assertEqual(i_am_alive.getExpectedMaxHP(), 108)
        self.assertEqual(i_am_alive.getExpectedCurrentHP(), 108)

        i_am_alive.takeExpectedDamage(8)

        self.assertEqual(i_am_alive.getExpectedMaxHP(), 108)
        self.assertEqual(i_am_alive.getExpectedCurrentHP(), 100)

        i_am_alive.takeExpectedDamage(108)
        self.assertEqual(i_am_alive.getExpectedCurrentHP(), 0)


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
        blot_spell.setAttributes(attributes_to_test)

        self.assertEqual(blot_spell.getName(), "blot")
        self.assertEqual(blot_spell.getLevel(), 0)
        self.assertEqual(blot_spell.getType(), AbilityType.SPELL)
        self.assertEqual(blot_spell.getSubtype(), AbilitySpellType.ANCIENT)
        self.assertEqual(blot_spell.getMinRange(), 1)
        self.assertEqual(blot_spell.getMaxRange(), 2)
        self.assertEqual(blot_spell.getSplashRadius(), None)
        self.assertEqual(blot_spell.getAimBonus(), 1)
        self.assertEqual(blot_spell.getDamage(), 1)
        self.assertEqual(blot_spell.getMaxDurability(), 10)
        self.assertEqual(blot_spell.canDealCriticalHits(), False)
        self.assertEqual(blot_spell.canCounterAttack(), False)
        self.assertEqual(blot_spell.getCriticalHitNumber(), None)
        self.assertEqual(len(blot_spell.getTargets()), 1)
        self.assertTrue(AbilityTarget.FOE in blot_spell.getTargets())

        sword = Ability()
        sword.setAttributes({**attributes_to_test, 'canCounterAttack': True })
        self.assertTrue(sword.canCounterAttack())


class SquaddieUsesAbilityToAttack(TestCase):
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

        self.bandit = Squaddie()
        self.bandit.setStats({
            "name": "Bandit level 1",
            "maxHP": 3,
            "aim": 0,
            "strength": 1,
            "magic": 0,
            "dodge": 0,
            "armor": 0,
            "barrier": 0,
            "resist": 0,
        })

    def testSquaddieCanEquipAbility(self):
        self.teros.equipAbility(self.blot_spell)

        self.assertEqual(len(self.teros.getAbilities()), 1)
        self.assertTrue("blot" in self.teros.getAbilityNames())

        self.assertEqual(len(self.bandit.getAbilities()), 0)

    def testSquaddieUsesAbilityToDealExpectedDamage(self):
        self.teros.equipAbility(self.blot_spell)
        self.teros.useAbility(self.blot_spell, self.bandit)
        self.assertTrue(self.bandit.getExpectedCurrentHP() < self.bandit.getExpectedMaxHP())