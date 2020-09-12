from ability import AbilityType, Ability
from squaddie import Squaddie


class SquaddieUseAbilityService():
    @classmethod
    def calculate_damage_upon_hit(cls, attacker: Squaddie, ability: Ability, target: Squaddie) -> int:

        if ability.getType() == AbilityType.SPELL:
            attacker_total_damage = attacker.getMagic() + ability.getDamage()
            target_damage_reduction = target.getResist()
        elif ability.getType() == AbilityType.WEAPON:
            attacker_total_damage = attacker.getStrength() + ability.getDamage()
            target_damage_reduction = target.getArmor()
        else:
            attacker_total_damage = ability.getDamage()
            target_damage_reduction = 0

        if attacker_total_damage - target_damage_reduction > 0:
            return attacker_total_damage - target_damage_reduction
        return 0

    @classmethod
    def calculate_chance_hit(cls, attacker: Squaddie, ability: Ability, target: Squaddie) -> int:

        attacker_total_chance_to_hit = attacker.getAim() + ability.getAimBonus()

        if ability.getType() == AbilityType.SPELL:
            target_total_dodge = target.getDeflect()
        elif ability.getType() == AbilityType.WEAPON:
            target_total_dodge = target.getDodge()
        else:
            target_total_dodge = 0

        return attacker_total_chance_to_hit - target_total_dodge

    @classmethod
    def calculate_expected_chance_hit(cls, attacker: Squaddie, ability: Ability, target: Squaddie) -> int:
        chance_to_hit = SquaddieUseAbilityService.calculate_chance_hit(attacker, ability, target)

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
        if not ability.canDealCriticalHits():
            return 0
        
        raw_damage = SquaddieUseAbilityService.calculate_damage_upon_hit(attacker, ability, target)
        crit_number = ability.getCriticalHitNumber()

        crit_chance_out_of_36 = 0
        if crit_number < 2:
            crit_chance_out_of_36 = 0
        if crit_number > 11:
            crit_chance_out_of_36 = 36

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
