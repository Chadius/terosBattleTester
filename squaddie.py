from typing import Sequence, Union

from ability import Ability


class Squaddie(object):
    def __init__(self):
        self.name = None
        self.maxHP = 0
        self.expectedMaxHP = 0
        self.expectedCurrentHP = 0

        self.aim = 0
        self.strength = 0
        self.magic = 0

        self.dodge = 0
        self.armor = 0

        self.deflect = 0
        self.resist = 0

        self.abilities = []
        self.equippedAbility = None

    def set_stats(self, statUpdates) -> None:
        self.name = statUpdates.get("name", self.name)
        self.maxHP = statUpdates.get("maxHP", self.maxHP)
        self.expectedMaxHP = self.maxHP * 36
        self.expectedCurrentHP = self.expectedMaxHP

        self.aim = statUpdates.get("aim", self.aim)
        self.strength = statUpdates.get("strength", self.strength)
        self.magic = statUpdates.get("magic", self.magic)

        self.dodge = statUpdates.get("dodge", self.dodge)
        self.armor = statUpdates.get("armor", self.armor)

        self.deflect = statUpdates.get("deflect", self.deflect)
        self.resist = statUpdates.get("resist", self.resist)

    def get_max_hp(self) -> int:
        return self.maxHP

    def get_aim(self) -> int:
        return self.aim

    def get_strength(self) -> int:
        return self.strength

    def get_magic(self) -> int:
        return self.magic

    def get_armor(self) -> int:
        return self.armor

    def get_dodge(self) -> int:
        return self.dodge

    def get_deflect(self) -> int:
        return self.deflect

    def get_resist(self) -> int:
        return self.resist

    def get_name(self) -> str:
        return self.name

    def get_expected_max_hp(self) -> int:
        return self.expectedMaxHP

    def get_expected_current_hp(self) -> int:
        return self.expectedCurrentHP

    def add_ability(self, ability) -> None:
        self.abilities.append(ability)

    def get_abilities(self) -> Sequence[Ability]:
        return self.abilities

    def get_ability_names(self) -> Sequence[str]:
        return [ability.get_name() for ability in self.abilities]

    def use_ability(self, ability, target) -> None:
        self.equip_ability(ability)
        target.take_expected_damage(ability.damage)

    def take_expected_damage(self, expectedDamageTaken) -> None:
        self.expectedCurrentHP -= expectedDamageTaken
        if self.expectedCurrentHP < 0:
            self.expectedCurrentHP = 0

    def get_equipped_ability(self) -> Union[Ability, None]:
        return self.equippedAbility

    def equip_ability(self, ability) -> None:
        self.equippedAbility = ability
