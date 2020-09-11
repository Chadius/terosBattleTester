from enum import Enum
from typing import Union


class AbilityType(Enum):
    UNKNOWN = 0
    SPELL = 1
    WEAPON = 2


class AbilitySpellType(Enum):
    UNKNOWN = 0
    ANCIENT = 1


class AbilityWeaponType(Enum):
    UNKNOWN = 0
    AXE = 1


class AbilityTarget(Enum):
    UNKNOWN = 0
    FOE = 1


class Ability(object):
    def __init__(self):
        self.name = ""
        self.level = 0
        self.type = AbilityType.UNKNOWN
        self.subtype = None
        self.minRange = 0
        self.maxRange = 0
        self.splashRadius = 0
        self.aim = 0
        self.damage = 0
        self.durability = 0
        self.criticalHitNumber = None
        self.targets = []
        self.counterAttacksPossible = False

    def setAttributes(self, attributeUpdates) -> None:
        self.name = attributeUpdates.get("name", self.name)
        self.level = attributeUpdates.get("level", self.level)
        self.type = attributeUpdates.get("type", self.type)
        self.subtype = attributeUpdates.get("subtype", self.subtype)
        self.minRange = attributeUpdates.get("minRange", self.minRange)
        self.maxRange = attributeUpdates.get("maxRange", self.maxRange)
        self.splashRadius = attributeUpdates.get("splashRadius", self.splashRadius)
        self.aim = attributeUpdates.get("aim", self.aim)
        self.damage = attributeUpdates.get("damage", self.damage)
        self.durability = attributeUpdates.get("durability", self.durability)
        self.criticalHitNumber = attributeUpdates.get("criticalHitNumber", self.criticalHitNumber)
        self.targets = attributeUpdates.get("targets", self.targets)
        self.counterAttacksPossible = attributeUpdates.get("canCounterAttack", self.counterAttacksPossible)

    def getName(self) -> str:
        return self.name

    def getLevel(self) -> int:
        return self.level

    def getType(self) -> AbilityType:
        return self.type

    def getSubtype(self) -> Union[AbilitySpellType, AbilityWeaponType]:
        return self.subtype

    def getMinRange(self) -> int:
        return self.minRange

    def getMaxRange(self) -> int:
        return self.maxRange

    def getSplashRadius(self) -> int:
        return self.splashRadius

    def getAimBonus(self) -> int:
        return self.aim

    def getDamage(self) -> int:
        return self.damage

    def getMaxDurability(self) -> int:
        return self.durability

    def canDealCriticalHits(self) -> bool:
        return self.criticalHitNumber is not None

    def canCounterAttack(self) -> bool:
        return self.counterAttacksPossible

    def getCriticalHitNumber(self) -> int:
        return self.criticalHitNumber

    def getTargets(self) -> str:
        return self.targets

