class Squaddie(object):
    def __init__(self):
        self.name = None
        self.maxHP = 0
        self.expectedMaxHP = 0
        self.expectedCurrentHP = 0

        self.aim = 0
        self.strength = 0
        self.magic = 0
        self.armor = 0
        self.dodge = 0
        self.barrier = 0
        self.resist = 0

        self.abilities = []

    def setStats(self, statUpdates):
        self.name = statUpdates.get("name", self.name)
        self.maxHP = statUpdates.get("maxHP", self.maxHP)
        self.expectedMaxHP = self.maxHP * 36
        self.expectedCurrentHP = self.expectedMaxHP

        self.aim = statUpdates.get("aim", self.aim)
        self.strength = statUpdates.get("strength", self.strength)
        self.magic = statUpdates.get("magic", self.magic)
        self.armor = statUpdates.get("armor", self.armor)
        self.dodge = statUpdates.get("dodge", self.dodge)
        self.barrier = statUpdates.get("barrier", self.barrier)
        self.resist = statUpdates.get("resist", self.resist)

    def getMaxHP(self):
        return self.maxHP

    def getAim(self):
        return self.aim

    def getStrength(self):
        return self.strength

    def getMagic(self):
        return self.magic

    def getArmor(self):
        return self.armor

    def getDodge(self):
        return self.dodge

    def getBarrier(self):
        return self.barrier

    def getResist(self):
        return self.resist

    def getName(self):
        return self.name

    def getExpectedMaxHP(self):
        return self.expectedMaxHP

    def getExpectedCurrentHP(self):
        return self.expectedCurrentHP

    def equipAbility(self, ability):
        self.abilities.append(ability)

    def getAbilities(self):
        return self.abilities

    def getAbilityNames(self):
        return [ability.getName() for ability in self.abilities]

    def useAbility(self, ability, target):
        target.takeExpectedDamage(ability.damage)

    def takeExpectedDamage(self, expectedDamageTaken):
        self.expectedCurrentHP -= expectedDamageTaken
        if self.expectedCurrentHP < 0:
            self.expectedCurrentHP = 0
