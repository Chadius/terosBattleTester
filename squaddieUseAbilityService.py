from ability import AbilityType


class SquaddieUseAbilityService():
    @classmethod
    def calculate_damage_upon_hit(cls, attacker, ability, target):

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
