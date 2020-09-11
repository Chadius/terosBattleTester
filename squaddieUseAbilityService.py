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
        return 26
