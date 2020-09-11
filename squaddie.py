from typing import Sequence

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

    def setStats(self, statUpdates) -> None:
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

    def getMaxHP(self) -> int:
        return self.maxHP

    def getAim(self) -> int:
        return self.aim

    def getStrength(self) -> int:
        return self.strength

    def getMagic(self) -> int:
        return self.magic

    def getArmor(self) -> int:
        return self.armor

    def getDodge(self) -> int:
        return self.dodge

    def getDeflect(self) -> int:
        return self.deflect

    def getResist(self) -> int:
        return self.resist

    def getName(self) -> str:
        return self.name

    def getExpectedMaxHP(self) -> int:
        return self.expectedMaxHP

    def getExpectedCurrentHP(self) -> int:
        return self.expectedCurrentHP

    def equipAbility(self, ability) -> None:
        self.abilities.append(ability)

    def getAbilities(self) -> Sequence[Ability]:
        return self.abilities

    def getAbilityNames(self) -> Sequence[str]:
        return [ability.getName() for ability in self.abilities]

    def useAbility(self, ability, target) -> None:
        target.takeExpectedDamage(ability.damage)

    def takeExpectedDamage(self, expectedDamageTaken) -> None:
        self.expectedCurrentHP -= expectedDamageTaken
        if self.expectedCurrentHP < 0:
            self.expectedCurrentHP = 0
