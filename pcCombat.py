import sys, random, collections, copy


class PC:
    def __init__(self, Name, Str, Dex, Con, Intel, Wis, Chr, Class, Level, armor, shield, sizeMod):
        self.Name  = Name
        self.Str   = Str
        self.Dex   = Dex
        self.Con   = Con
        self.Intel = Intel
        self.Wis   = Wis
        self.Chr   = Chr
        self.Class = Class
        self.Level = Level


class PCfighter(PC):
    def __init__(self, Name, Str, Dex, Con, Intel, Wis, Chr, Class, Level, armor, shield, sizeMod):
        PC.__init__(self, Name, Str, Dex, Con, Intel, Wis, Chr, Class, Level, armor, shield, sizeMod)
        self.AC = 10 + armor + shield + sizeMod
        self.HP = 0
        x = 1
        while x <= self.Level:
            addHP = random.randint(1, 10) + StatBonus(self.Con)
            if addHP > 0:
                self.HP += addHP
            else:
                self.HP += 1
            x += 1
            
    def meleeAtk(self, mod = 0):
        return (random.randint(1, 20) + self.Level + StatBonus(self.Str) + mod)

    def meleeDmg(self, numDie = 1, dieType = 8, mod = 0):
        return numDie * random.randint(1, dieType) + mod + StatBonus(self.Str)

Player1 = collections.OrderedDict()
Player1['Name']    = ''
Player1['Str']     = int(12)
Player1['Dex']     = int(12)
Player1['Con']     = int(12)
Player1['Intel']   = int(12)
Player1['Wis']     = int(12)
Player1['Chr']     = int(12)
Player1['Class']   = ''
Player1['Level']   = int(1)
Player1['armor']   = int(0)
Player1['shield']  = int(0)
Player1['sizeMod'] = int(0)

prompts = {
    'Name'    : 'Please enter a name for the character: ',
    'Str'     : "Please enter the character's Strenth: ",
    'Dex'     : 'Dexterity:',
    'Con'     : "Constitution:",
    'Intel'   : 'Intelligence:',
    'Wis'     : 'Wisdom:',
    'Chr'     : "Charisma:",
    'Class'   : "Please enter the Character's class(Only Figther currently available):",
    'Level'   : "Character level: ",
    'armor'.  : 'Armor bonus:',
    'shield'  : 'Shield bonus: ',
    'sizeMod' : 'Size bonus to AC(For small races):'
}

def main():
    static1, static2 = Begin()
    PC1 = copy.deepcopy(static1)
    PC2 = copy.deepcopy(static2)
    Combat(PC1, PC2)
    while True:
        if reTry() == True:
            PC1 = copy.deepcopy(static1)
            PC2 = copy.deepcopy(static2)
            #print(PC1.HP, static1.HP, PC2.HP, static2.HP)
            Combat(PC1, PC2)
        else:
            startOver()

def StatBonus(stat):
    if stat >= 10:
        return (stat - 10) // 2
    elif stat <= 9 and stat >= 1:
        return (-5) + (stat // 2)

def Initiative(pc1, pc2):
    pc1roll = random.randint(1, 20) + StatBonus(pc1.Dex)
    pc2roll = random.randint(1, 20) + StatBonus(pc2.Dex)
    if pc1roll > pc2roll:
        return True
    elif pc1roll == pc2roll:
        Initiative(pc1,pc2)
    else:
        return False


def Combat(firstPC, secondPC):
    if Initiative(firstPC, secondPC) == True:
        pc1 = firstPC
        pc2 = secondPC
    else:
        pc1 = secondPC
        pc2 = firstPC
    print(pc1.Name + ' won the initiative roll!')
    print('\n')                
    rnd = 0
    print('Combat has begun between', pc1.Name, 'and', str(pc2.Name) + '!')
    print(pc1.Name, 'has', pc1.HP, 'hitpoints and', pc2.Name, 'has', pc2.HP, 'hitpoints!')
    print('')
    while pc1.HP > 0 and pc2.HP > 0:
        rnd += 1
        print('Round ' + str(rnd) + '!!')
        print(pc1.Name, 'attacks', pc2.Name + '!')
        roll = pc1.meleeAtk()
        print(pc1.Name, 'rolls a ' + str(roll) + '!')
        if roll > pc2.AC:
            dmg = pc1.meleeDmg()
            pc2.HP -= dmg
            print(pc1.Name, 'hits for', dmg, 'points!', pc2.Name, 'is down to', pc2.HP, 'hit points!')
        else:
            print(pc1.Name, 'missed!')
        try:
            input('Press Enter to Continue...')
            print('')
        except SyntaxError:
            pass
        if pc1.HP > 0 and pc2.HP > 0:
            print(pc2.Name, 'attacks', pc1.Name + '!')
            roll = pc2.meleeAtk()
            print(pc2.Name, 'rolls a ' + str(roll) + '!')
            if roll > pc1.AC:
                dmg = pc2.meleeDmg()
                pc1.HP -= dmg
                print(pc2.Name, 'hits for', dmg, 'points!', pc1.Name, 'is down to', pc1.HP, 'hit points!')
            else:
                print(pc2.Name, 'missed!')
            try:
                input('Press Enter to Continue...')
                print('')
            except SyntaxError:
                pass

def createPC(name):
    for key in name:
        if type(name[key]) == str:
            name[key] = str(input(prompts[key]))
        elif type(name[key]) == int:
            name[key] = int(input(str(prompts[key])))
    result = []
    for key in name:
        result.append(name[key])
    return result


def reTry():
    while True:
        tryAgain = input("Combat is over! Would you like to try with the same combatants again?(Y/N)")
        if tryAgain == 'Y' or tryAgain == 'y':
            return True
        elif tryAgain == 'N' or tryAgain == 'n':
            return False
        else:
            print('I do not recognize your answer!')

def startOver():
    startAgain = input("Would you like to try with new combatants?(Y/N)")
    if startAgain == 'Y' or startAgain == 'y':
        main()
    elif startAgain == 'N' or startAgain == 'n':
        sys.exit()
    else:
        print('I do not recognize your answer!')
        startOver()

def Begin():
    print('\n')
    print("Welcome to Andy's 3.5 Edition AD&D Combat Simulator")
    print("Let's Begin by creating our combatants!")
    print("Please enter the following information on combatant #1!")
    print(' ')
    PC1temp = createPC(Player1)
    PC1 = PCfighter(PC1temp[0], PC1temp[1], PC1temp[2], PC1temp[3], PC1temp[4], PC1temp[5], PC1temp[6], PC1temp[7], PC1temp[8], PC1temp[9], PC1temp[10], PC1temp[11])
    print('\n')
    print("Great! Now enter the information for combatant #2!")
    print(' ')
    PC1temp = createPC(Player1)
    PC2 = PCfighter(PC1temp[0], PC1temp[1], PC1temp[2], PC1temp[3], PC1temp[4], PC1temp[5], PC1temp[6], PC1temp[7], PC1temp[8], PC1temp[9], PC1temp[10], PC1temp[11])
    print("Thank you! Let's begin!")
    print(' ')
    return PC1, PC2
    
Fresh = True

            
main()
