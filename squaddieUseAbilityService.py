from typing import List, Dict, Union

from ability import AbilityType, Ability, AbilityWeaponType
from squaddie import Squaddie
from zone_map import ZoneMap


class SquaddieUseAbilityService():
    @classmethod
    def calculate_damage_upon_hit(cls, attacker: Squaddie, ability: Ability, target: Squaddie) -> int:

        if ability.get_type() == AbilityType.SPELL:
            attacker_total_damage = attacker.get_magic() + ability.get_damage()
            target_damage_reduction = target.get_resist()
        elif ability.get_type() == AbilityType.WEAPON:
            attacker_total_damage = attacker.get_strength() + ability.get_damage()
            target_damage_reduction = target.get_armor()
        else:
            attacker_total_damage = ability.get_damage()
            target_damage_reduction = 0

        if attacker_total_damage - target_damage_reduction > 0:
            return attacker_total_damage - target_damage_reduction
        return 0

    @classmethod
    def calculate_chance_hit(cls, attacker: Squaddie, ability: Ability, target: Squaddie, modifiers={}) -> int:

        attacker_total_chance_to_hit = attacker.get_aim() + ability.get_aim_bonus()

        if ability.get_type() == AbilityType.SPELL:
            target_total_dodge = target.get_deflect()
        elif ability.get_type() == AbilityType.WEAPON:
            target_total_dodge = target.get_dodge()
        else:
            target_total_dodge = 0

        chance_to_hit = attacker_total_chance_to_hit - target_total_dodge

        if modifiers.get("hasAdvantage", False):
            chance_to_hit += 1

        if modifiers.get("hasDisadvantage", False):
            chance_to_hit -= 1

        if modifiers.get("isCounterAttack", False):
            chance_to_hit += -2

        if modifiers.get("tooClose", False):
            chance_to_hit += -1
        return chance_to_hit

    @classmethod
    def calculate_expected_chance_hit(cls, attacker: Squaddie, ability: Ability, target: Squaddie, modifiers={}) -> int:
        modifiers.update({
            "hasAdvantage": SquaddieUseAbilityService.has_advantage_due_to_ability(ability,
                                                                                   target.get_equipped_ability()),
            "hasDisadvantage": SquaddieUseAbilityService.has_disadvantage_due_to_ability(ability,
                                                                                         target.get_equipped_ability()),
        })

        if modifiers.get("initiating", False):
            modifiers["hasAdvantage"] = SquaddieUseAbilityService.has_advantage_due_to_initating(ability)

        chance_to_hit = SquaddieUseAbilityService.calculate_chance_hit(attacker, ability, target, modifiers)
        if chance_to_hit < -5:
            return 0
        if chance_to_hit > 4:
            return 36

        expected_chance = {
            4: 35,
            3: 33,
            2: 30,
            1: 26,
            0: 21,
            -1: 15,
            -2: 10,
            -3: 6,
            -4: 3,
            -5: 1,
        }

        return expected_chance[chance_to_hit]

    @classmethod
    def calculate_expected_crit_damage(cls, attacker: Squaddie, ability: Ability, target: Squaddie) -> int:
        if not ability.can_deal_critical_hits():
            return 0

        raw_damage = SquaddieUseAbilityService.calculate_damage_upon_hit(attacker, ability, target)
        crit_number = ability.get_critical_hit_number()

        if crit_number < 2:
            return 0
        if crit_number > 11:
            return 36

        expected_chance = {
            11: 35,
            10: 33,
            9: 30,
            8: 26,
            7: 21,
            6: 15,
            5: 10,
            4: 6,
            3: 3,
            2: 1,
        }
        return expected_chance[crit_number] * raw_damage

    @classmethod
    def has_advantage_due_to_ability(cls, attack_ability: Ability, defense_ability: Ability) -> bool:
        if defense_ability is None:
            return False

        advantage_chart = {
            AbilityType.WEAPON: {
                AbilityWeaponType.SWORD: AbilityWeaponType.AXE,
                AbilityWeaponType.SPEAR: AbilityWeaponType.SWORD,
                AbilityWeaponType.AXE: AbilityWeaponType.SPEAR,
            }
        }

        return cls.__does_ability_type_exist_in_chart(attack_ability, defense_ability, advantage_chart)

    @classmethod
    def has_disadvantage_due_to_ability(cls, attack_ability: Ability, defense_ability: Ability) -> bool:
        if defense_ability is None:
            return False

        disadvantage_chart = {
            AbilityType.WEAPON: {
                AbilityWeaponType.SWORD: AbilityWeaponType.SPEAR,
                AbilityWeaponType.SPEAR: AbilityWeaponType.AXE,
                AbilityWeaponType.AXE: AbilityWeaponType.SWORD
            }
        }

        return cls.__does_ability_type_exist_in_chart(attack_ability, defense_ability, disadvantage_chart)

    @classmethod
    def __does_ability_type_exist_in_chart(cls, attack_ability: Ability, defense_ability: Ability, chart) -> bool:
        ability_type = attack_ability.get_type()
        defense_ability_type = attack_ability.get_type()
        attack_subtype = attack_ability.get_subtype()
        defense_subtype = defense_ability.get_subtype()

        if ability_type != defense_ability_type:
            return False

        if ability_type not in chart:
            return False

        if attack_subtype not in chart[ability_type]:
            return False

        return chart[ability_type][attack_subtype] == defense_subtype

    @classmethod
    def has_advantage_due_to_initating(cls, ability):
        if ability.get_type() == AbilityType.WEAPON and ability.get_subtype() == AbilityWeaponType.BOW:
            return True
        return False

    @classmethod
    def has_disadvantage_due_to_countering(cls, ability):
        if ability.get_type() == AbilityType.WEAPON and ability.get_subtype() == AbilityWeaponType.BOW:
            return True
        return False

    @classmethod
    def has_point_blank_penalty(cls, ability):
        if ability.get_type() == AbilityType.WEAPON and ability.get_subtype() == AbilityWeaponType.BOW:
            return True
        return False

    @classmethod
    def calculate_expected_damage(cls, attacker: Squaddie, ability: Ability, target: Squaddie, modifiers={}) -> int:
        expected_chance_to_hit = SquaddieUseAbilityService.calculate_expected_chance_hit(attacker, ability, target,
                                                                                         modifiers)

        damage_upon_hit = SquaddieUseAbilityService.calculate_damage_upon_hit(attacker, ability, target)
        return expected_chance_to_hit * damage_upon_hit

    @classmethod
    def get_modifiers_for_ability_use(cls, zone_map: ZoneMap, attacker: Squaddie, ability: Ability,
                                      defender: Squaddie) -> List[Dict[str, Union[str, bool]]]:
        ability_modifiers = []
        squaddies_are_in_same_zone = zone_map.squaddies_are_in_melee(attacker, defender)

        round_modifiers = {
            "initiating": True
        }
        if cls.has_advantage_due_to_initating(ability):
            round_modifiers["hasAdvantage"] = True
        if cls.has_advantage_due_to_ability(ability, defender.get_equipped_ability()):
            round_modifiers["hasAdvantage"] = True
        if cls.has_disadvantage_due_to_ability(ability, defender.get_equipped_ability()):
            round_modifiers["hasDisadvantage"] = True
        if cls.has_point_blank_penalty(ability) and squaddies_are_in_same_zone:
            round_modifiers["tooClose"] = True
        ability_modifiers.append(round_modifiers)

        if defender.get_equipped_ability() and defender.get_equipped_ability().can_counter_attack():
            counter_attack_modifiers = {
                "isCounterAttack": True
            }
            if cls.has_disadvantage_due_to_countering(defender.get_equipped_ability()):
                counter_attack_modifiers["hasDisadvantage"] = True
            if cls.has_advantage_due_to_ability(defender.get_equipped_ability(), ability):
                counter_attack_modifiers["hasAdvantage"] = True
            if cls.has_disadvantage_due_to_ability(defender.get_equipped_ability(), ability):
                counter_attack_modifiers["hasDisadvantage"] = True
            if cls.has_point_blank_penalty(defender.get_equipped_ability()) and squaddies_are_in_same_zone:
                counter_attack_modifiers["tooClose"] = True
            ability_modifiers.append(counter_attack_modifiers)

        return ability_modifiers
