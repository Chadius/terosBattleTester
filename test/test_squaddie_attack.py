from unittest import TestCase

from squaddieUseAbilityService import SquaddieUseAbilityService

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


class SquaddieAttackToReduceHitpoints(TestCase):
    def setUp(self):
        self.teros = SquaddieFactory.create_teros()
        self.blot_spell = AbilityFactory.create_blot_spell()
        self.spear = AbilityFactory.create_spear()
        self.bandit = SquaddieFactory.create_bandit()

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
        self.teros = SquaddieFactory.create_teros()
        self.blot_spell = AbilityFactory.create_blot_spell()
        self.spear = AbilityFactory.create_spear()
        self.necromancer = SquaddieFactory.create_necromancer()

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
        self.teros = SquaddieFactory.create_teros()
        self.bandit = SquaddieFactory.create_bandit()
        self.blot_spell = AbilityFactory.create_blot_spell()
        self.spear = AbilityFactory.create_spear()
        self.sword = AbilityFactory.create_sword()
        self.axe = AbilityFactory.create_axe()
        self.bow = AbilityFactory.create_bow()

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

    def test_neutral_if_defender_is_unequipped(self):
        self.assertFalse(SquaddieUseAbilityService.has_advantage_due_to_ability(self.spear, None))
        self.assertFalse(SquaddieUseAbilityService.has_disadvantage_due_to_ability(self.spear, None))

    def test_bows_are_neutral_to_weapons(self):
        self.assertFalse(SquaddieUseAbilityService.has_disadvantage_due_to_ability(self.bow, self.spear))
        self.assertFalse(SquaddieUseAbilityService.has_disadvantage_due_to_ability(self.bow, self.sword))
        self.assertFalse(SquaddieUseAbilityService.has_disadvantage_due_to_ability(self.bow, self.axe))
        self.assertFalse(SquaddieUseAbilityService.has_disadvantage_due_to_ability(self.bow, self.bow))

        self.assertFalse(SquaddieUseAbilityService.has_advantage_due_to_ability(self.bow, self.spear))
        self.assertFalse(SquaddieUseAbilityService.has_advantage_due_to_ability(self.bow, self.sword))
        self.assertFalse(SquaddieUseAbilityService.has_advantage_due_to_ability(self.bow, self.axe))
        self.assertFalse(SquaddieUseAbilityService.has_advantage_due_to_ability(self.bow, self.bow))

    def test_bows_have_advantage_if_initiating(self):
        self.assertTrue(SquaddieUseAbilityService.has_advantage_due_to_initating(self.bow))
        self.assertFalse(SquaddieUseAbilityService.has_advantage_due_to_initating(self.blot_spell))

    def test_bows_have_disadvantage_if_countering(self):
        self.assertTrue(SquaddieUseAbilityService.has_disadvantage_due_to_countering(self.bow))
        self.assertFalse(SquaddieUseAbilityService.has_disadvantage_due_to_countering(self.blot_spell))

    def test_bows_take_penalty_for_firing_up_close(self):
        self.assertTrue(SquaddieUseAbilityService.has_point_blank_penalty(self.bow))
        self.assertFalse(SquaddieUseAbilityService.has_point_blank_penalty(self.blot_spell))


class CalculateExpectedDamage(TestCase):
    def setUp(self):
        self.teros = SquaddieFactory.create_teros()

        self.blot_spell = AbilityFactory.create_blot_spell()
        self.spear = AbilityFactory.create_spear()
        self.sword = AbilityFactory.create_sword()
        self.axe = AbilityFactory.create_axe()
        self.bow = AbilityFactory.create_bow()

        self.necromancer = SquaddieFactory.create_necromancer()

        self.bandit = SquaddieFactory.create_bandit()

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

    def test_calculate_expected_damage_inflated_compared_to_normal_hit_points(self):
        expected_damage = SquaddieUseAbilityService.calculate_expected_damage(self.teros, self.blot_spell, self.bandit)
        self.assertEqual(expected_damage, 90)

    def test_weapon_advantage_increases_expected_damage(self):
        self.teros.add_ability(self.sword)
        self.teros.equip_ability(self.sword)

        self.bandit.add_ability(self.axe)
        self.bandit.equip_ability(self.axe)

        expected_damage = SquaddieUseAbilityService.calculate_expected_damage(self.teros, self.sword, self.bandit)
        self.assertEqual(expected_damage, 66)

    def test_weapon_disadvantage_decreased_expected_damage(self):
        self.teros.add_ability(self.spear)
        self.teros.equip_ability(self.spear)

        self.bandit.add_ability(self.axe)
        self.bandit.equip_ability(self.axe)

        expected_damage = SquaddieUseAbilityService.calculate_expected_damage(self.teros, self.spear, self.bandit)
        self.assertEqual(expected_damage, 52)

    def test_bow_initiating_increases_expected_damage(self):
        self.teros.add_ability(self.bow)
        self.teros.equip_ability(self.bow)

        self.bandit.add_ability(self.axe)
        self.bandit.equip_ability(self.axe)

        expected_damage = SquaddieUseAbilityService.calculate_expected_damage(
            self.teros,
            self.bow,
            self.bandit,
            {
                "initiating": True
            }
        )
        self.assertEqual(expected_damage, 66)

    def test_countering_decreases_expected_damage(self):
        self.teros.add_ability(self.spear)
        self.teros.equip_ability(self.spear)

        self.bandit.add_ability(self.spear)
        self.bandit.equip_ability(self.spear)

        expected_damage = SquaddieUseAbilityService.calculate_expected_damage(
            self.teros,
            self.bow,
            self.bandit,
            {
                "isCounterAttack": True
            }
        )
        self.assertEqual(expected_damage, 42)

    def test_bow_countering_decreases_expected_damage(self):
        self.teros.add_ability(self.bow)
        self.teros.equip_ability(self.bow)

        self.bandit.add_ability(self.axe)
        self.bandit.equip_ability(self.axe)

        expected_damage = SquaddieUseAbilityService.calculate_expected_damage(
            self.teros,
            self.bow,
            self.bandit,
            {
                "isCounterAttack": True
            }
        )
        self.assertEqual(expected_damage, 42)

    def test_bow_too_close_decreases_expected_damage(self):
        self.teros.add_ability(self.bow)
        self.teros.equip_ability(self.bow)

        self.bandit.add_ability(self.axe)
        self.bandit.equip_ability(self.axe)

        expected_damage = SquaddieUseAbilityService.calculate_expected_damage(
            self.teros,
            self.bow,
            self.bandit,
            {
                "tooClose": True
            }
        )
        self.assertEqual(expected_damage, 52)


class DetermineAttacksAndModifiers(TestCase):
    def setUp(self) -> None:
        self.zone_map = ZoneMap("The map")
        self.zone_map.add_zone("A")
        self.zone_map.add_zone("B")
        self.zone_map.add_zone("C")

        self.zone_map.link_adjacent_zones("A", "B")
        self.zone_map.link_adjacent_zones("B", "C")

        self.teros = SquaddieFactory.create_teros()
        self.bandit = SquaddieFactory.create_bandit()
        self.necromancer = SquaddieFactory.create_necromancer()

        self.blot_spell = AbilityFactory.create_blot_spell()
        self.spear = AbilityFactory.create_spear()
        self.sword = AbilityFactory.create_sword()
        self.axe = AbilityFactory.create_axe()
        self.bow = AbilityFactory.create_bow()

    def test_weapon_attacks_create_counterattacks(self):
        self.teros.add_ability(self.spear)
        self.teros.equip_ability(self.spear)

        self.bandit.add_ability(self.spear)
        self.bandit.equip_ability(self.spear)

        self.zone_map.add_squaddie(self.teros, "A")
        self.zone_map.add_squaddie(self.bandit, "A")

        attack_modifiers = SquaddieUseAbilityService.get_modifiers_for_ability_use(
            self.zone_map,
            self.teros,
            self.spear,
            self.bandit
        )

        self.assertEqual(
            [
                {
                    "initiating": True
                },
                {
                    "isCounterAttack": True
                },
            ],
            attack_modifiers
        )

    def test_spell_attacks_do_not_create_counterattacks(self):
        self.teros.add_ability(self.blot_spell)
        self.teros.equip_ability(self.blot_spell)

        self.bandit.add_ability(self.spear)
        self.bandit.equip_ability(self.spear)

        self.zone_map.add_squaddie(self.teros, "A")
        self.zone_map.add_squaddie(self.bandit, "A")

        attack_modifiers = SquaddieUseAbilityService.get_modifiers_for_ability_use(
            self.zone_map,
            self.bandit,
            self.spear,
            self.teros
        )

        self.assertEqual(
            [
                {
                    "initiating": True
                }
            ],
            attack_modifiers
        )

    def test_unequipped_defenders_do_not_counter(self):
        self.teros.add_ability(self.spear)
        self.teros.equip_ability(self.spear)

        self.zone_map.add_squaddie(self.teros, "A")
        self.zone_map.add_squaddie(self.bandit, "A")

        attack_modifiers = SquaddieUseAbilityService.get_modifiers_for_ability_use(
            self.zone_map,
            self.teros,
            self.spear,
            self.bandit
        )

        self.assertEqual(
            [
                {
                    "initiating": True
                },
            ],
            attack_modifiers
        )

    def test_weapon_subtypes_create_advantage_and_disadvantage(self):
        self.teros.add_ability(self.spear)
        self.bandit.equip_ability(self.axe)

        self.zone_map.add_squaddie(self.teros, "A")
        self.zone_map.add_squaddie(self.bandit, "A")

        attack_modifiers = SquaddieUseAbilityService.get_modifiers_for_ability_use(
            self.zone_map,
            self.teros,
            self.spear,
            self.bandit
        )

        self.assertEqual(2, len(attack_modifiers))
        self.assertDictEqual(
            {
                "initiating": True,
                "hasDisadvantage": True,
            },
            attack_modifiers[0]
        )

        self.assertDictEqual(
            {
                "isCounterAttack": True,
                "hasAdvantage": True,
            },
            attack_modifiers[1]
        )

    def test_bows_create_advantage_and_disadvantage_based_on_initiate_and_counter(self):
        self.teros.add_ability(self.bow)
        self.teros.equip_ability(self.bow)

        self.bandit.add_ability(self.bow)
        self.bandit.equip_ability(self.bow)

        self.zone_map.add_squaddie(self.teros, "A")
        self.zone_map.add_squaddie(self.bandit, "B")

        attack_modifiers = SquaddieUseAbilityService.get_modifiers_for_ability_use(
            self.zone_map,
            self.bandit,
            self.bow,
            self.teros
        )

        self.assertEqual(2, len(attack_modifiers))
        self.assertDictEqual(
            {
                "initiating": True,
                "hasAdvantage": True,
            },
            attack_modifiers[0]
        )

        self.assertDictEqual(
            {
                "isCounterAttack": True,
                "hasDisadvantage": True,
            },
            attack_modifiers[1]
        )

    def test_bows_take_penalties_for_being_too_close(self):
        self.teros.add_ability(self.bow)
        self.teros.equip_ability(self.bow)

        self.bandit.add_ability(self.bow)
        self.bandit.equip_ability(self.bow)

        self.zone_map.add_squaddie(self.teros, "A")
        self.zone_map.add_squaddie(self.bandit, "A")

        attack_modifiers = SquaddieUseAbilityService.get_modifiers_for_ability_use(
            self.zone_map,
            self.bandit,
            self.bow,
            self.teros
        )

        self.assertEqual(2, len(attack_modifiers))
        self.assertDictEqual(
            {
                "initiating": True,
                "hasAdvantage": True,
                "tooClose": True,
            },
            attack_modifiers[0]
        )

        self.assertDictEqual(
            {
                "isCounterAttack": True,
                "hasDisadvantage": True,
                "tooClose": True,
            },
            attack_modifiers[1]
        )
