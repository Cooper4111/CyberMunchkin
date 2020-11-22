import sys
import csv
import numpy as np
import pandas as pd
import time

class Munchkin:

    def __init__(self, munchDict):
        self.name   = munchDict['Name']
        self.hp     = munchDict['HP']
        self.dmg    = munchDict['DMG']
        self.cd     = munchDict['CD']
        self.rng    = munchDict['RNG']
        self.ms     = munchDict['MS']
        self.alive  = True

        #self.str    = munchDict['STR']
        #self.agi    = munchDict['AGI']
        #self.vit    = munchDict['VIT']
        self.inl    = munchDict['INT']
        
        self.items  = {}

# Try make item system using dict, where key = itemName, val = itemObject

    def addItem(self, item):
        if item.name in self.items:
            return False
        else:
            self.items.update({item.name, item})
            for stt in item['stats']:
                self[stt] += item['stats'][stt]
            return True

    def delItem(self, item):
        if item.name in self.items:
            self.items.pop(item.name)
            for stt in item['stats']:
                self[stt] -= item['stats'][stt]           
            return True
        else:
            return False
        
        
    def updateStatsItem(self, itemstats, sign):
        if 'STR' in itemstats:
            self.str += itemstats['STR']*sign
        if 'AGI' in itemstats:
            self.agi += itemstats['AGI']*sign
        if 'INT' in itemstats:
            self.inl += itemstats['INT']*sign
        if 'VIT' in itemstats:
            self.str += itemstats['VIT']*sign
        if 'HP' in itemstats:
            self.hp += itemstats['HP']*sign
        if 'DMG' in itemstats:
            self.dmg += itemstats['DMG']*sign
        if 'CD' in itemstats:
            self.cd = round(self.cd*(1+(itemstats['CD']/100))**sign, 2)
        if 'RNG' in itemstats:
            self.rng += itemstats['RNG']*sign
        if 'MS' in itemstats:
            self.ms += itemstats['MS']*sign            
        
    def getDmg(self):
        return self.dmg
    
    def hitProc(self):
        pass
    
    def hit(self, target):
        target.getHit(self.getDmg())
        self.hitProc()
    
    def getHit(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.alive = False
            
    def whois(self):
        return {'Name':self.name,'HP':self.hp, 'DMG':self.dmg, 'CD':self.cd, 'alive':self.alive, 'ITEMS':self.items}

class Item:
    
    def __init__(self, itemData):
        self.name  = itemData['Name']
        self.stats = itemData['Stats']

##############################################################################
#####################                FUNCS               ##################### 
##############################################################################

def battle(munch):
    print(munch[0].name + ' encounters ' + munch[1].name + '!')
    print(munch[0].name + ' health: ', munch[0].hp, '\n' +
        munch[1].name + ' health: ', munch[1].hp, '\n')
    tickerA = int(munch[0].cd * 100)
    tickerB = int(munch[1].cd * 100)
    Atick = tickerA
    Btick = tickerB
    t = int(0)
    tA = int(0)
    tB = int(0)
    Aphase = 0
    Bphase = 0
    
    dist = max(munch[0].rng, munch[1].rng)
    
    intDeltaAB = (munch[0].inl - munch[1].inl)
    print('intDeltaAB: ', intDeltaAB)
    timeIncr = int(10)

    while(munch[0].alive and munch[1].alive):
    
    
# inlLICENCE ADVANTAGE
        if(Aphase == 0 and tA > -intDeltaAB):
            print(munch[0].name + ' wakes up at ', t/100)
            Aphase = 1
            tA = 0
        elif(Aphase == 0):
            pass
            #print(munch[0].name + ' sleeps...')
        if(Bphase == 0 and tB > intDeltaAB):
            print(munch[1].name + ' wakes up at ', t/100, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            Bphase = 1
            tB = 0
        elif(Bphase == 0):
            pass
            #print(munch[1].name + ' sleeps...')
        
# MOVING

        if(Aphase == 1 and munch[0].rng <= dist):
            dist -= 1 * munch[0].ms
        elif(Aphase == 1):
            Aphase = 2
            tA = 0
        if(Bphase == 1 and munch[1].rng <= dist):
            dist -= 1 * munch[1].ms
        elif(Bphase == 1):
            Bphase = 2
            tB = 0           
            

# ATTAKING
            
        if(Aphase == 2 and Atick - tA == 0):
            Atick += tickerA
            munch[0].hit(munch[1])
            print(munch[0].name + ' strikes ' + munch[1].name + ' for', munch[0].dmg)
            print(munch[1].name + ' health: ', munch[1].hp)
            print('t =', t/100)
        if(Aphase == 2 and Btick - tB == 0):
            Btick += tickerB
            munch[1].hit(munch[0])
            print(munch[1].name + ' strikes ' + munch[0].name + ' for', munch[1].dmg)
            print(munch[0].name + ' health: ', munch[0].hp)
            print('t =', t/100)
        #print('Aphase: ', Aphase, 'Bphase: ', Bphase, 't:', t/100, 'tA:', tA/100, 'tB:', tB/100)
        time.sleep(timeIncr/1000)
        tA += timeIncr
        tB += timeIncr
        t  += timeIncr
    if(not munch[0].alive):
        print(munch[0].name + ' is dead!')
    if(not munch[1].alive):
        print(munch[1].name + ' is dead!')

def nameGenerator():
    name = ''
    vow = 'aeiouy'
    con = 'bcdfghjklmnpqrstvwxz'
    
    return name

def createCsv():
    dfname = 'char_pool.sav'
    cols = ('Name','HP','DMG','CD')
    data = (np.random.randn(10, len(cols))+1)**2
    wTab = pd.DataFrame(data, columns = cols)
    wTab['Name'].astype(int)
    wTab.to_csv(dfname, index = True, sep = '\t')                           # WRITE DATA, INCLUDING INDEX
    


def crap():

    cols = {'Name','HP','DMG','CD'}
    df = pd.DataFrame(columns = cols)

    akey = ('A', 'B', 'C', 'D', 'E', 'F')
    Names = ['Nazjar', 'Azatoth', 'Kazubo', 'N\'rax', 'Amun-Ra', 'Ctulhu', 'Yog-Sototh']

    myDict = {}
    for i in range(0,len(akey)):
        myDict[akey[i]] = Names [i]
    #print(myDict)

    cols = {'Name','HP','DMG','CD'}
    entry0 = {'Name':'Ctulhu','HP':10000, 'DMG':500, 'CD':5}
    entry1 = {'Name':'Azatoth','HP':10500, 'DMG':225, 'CD':3}

    '''
    names = np.array(['Ctulhu','Azatoth','DummyGuy'])
    hp =    np.array([10500, 9000, 1000])
    dmg =   np.array([616, 225, 100])
    cd =    np.array([6, 2, 1])
    '''
    names = ['Ctulhu','Azatoth','DummyGuy']
    hp =    [10500, 9000, 1000]
    dmg =   [616, 225, 100]
    cd =    [6., 2., 1.]

    chData = {'Name':names,'HP':hp, 'DMG':dmg, 'CD':cd}
    chData['Name'] += ['GAZEBO']
    chData['HP'] += [9000]
    chData['DMG'] += [100500]
    chData['CD'] += [10.]

    df = pd.DataFrame(chData, columns = cols)
    print('\n', df)

##############################################################################
#####################                MAIN                ##################### 
##############################################################################

createCsv()

# ITEMS



# CHAR

cols =  {'Name','HP','DMG','CD','INT','RNG','MS'}
names = ['Paladin','Gazebo']
hp =    [10500, 1000]
dmg =   [144, 9000]
cd =    [.80, 2]
inl = [100, 100]
rng = [1, 1]
ms = [1, 1]  
chData = {'Name':names,'HP':hp, 'DMG':dmg, 'CD':cd, 'INT':inl,'MS':ms,'RNG':rng}

df = pd.DataFrame(chData, columns = cols)
print('\n', df, '\n\n')

Pal = Munchkin(df.loc[0])
Gaz = Munchkin(df.loc[1])

print(Pal.whois())
#print(Gaz.whois())

#battle([Pal, Gaz])




##############################################################################
###################                DEV NOTES               ################### 
##############################################################################

"""
TO-DO LIST:

@ Class munchkin
- Name generator (first simple, then complex)
@ Combat engine ( class C (munch, munch))
    - Class -> func. Rly, man. No bullshit.
- Arena engine (UI)
- Character save/load
- Charlist save/load
- Format+interface for itemsDB
- Format+interface for monsterDB


Zero Player Game. You own a Nigga. Make bets. He fights. You watch.
After a win get your bet and maybe a loot. If you loose -- your nigga is dead. Get a new one. For some gold, obviously.
Items avalible. Soulbound and common. Common are lost with nigga.
When your balance is zero -- you lost.

COMBAT MECHANICS:

Open a door. See descriprion of an enemy. Fight or Flee (lose bet)

BASIC STATS:

Name
HP ~1000.            float
Cooldown ~1000ms     int
BaseDamage ~100.     float      (Gauss allpied each hit)

POSSIBLE STATS:

Vitality:       +HP
Strength:       +BaseDmg
Agility:        +Reduces Cooldown
inlligence:   +N sec earlier start for delta(int1,int2)

Range:          if melee, -> HP++
MS:             Movement speed
Armor:          Hmmm... Percentage or const?

RACE:   ~Human  ~Elf    ~Dwarf  ~Undead     ~Halfling   ~Orc    ~Troll  ~Demon ~Mechanoid ~Great Old Ones 
CLASS:  ~Warrior    ~Rogue      ~Wizzard

Special passives: 0) Vampirism 1) Evasion 2) Crit 3) Slow 4) Berserk [(+%)++ each hit]

SOME ITEMS:
- One Ring: increases all stats + double increase maximal stat. Drops from Golum. Increases meetChance for Sauron.
- Excalibur: buried in a stone. Takes A LOT of strength to take out. Drops from Merlin.
- Laser NullPointer: Anihilates enemy on attack. Some chance (significant) to crash a programm.
- Hansol Kim: Immortal. Low damage. Can commit suicide on each hit.

SOME ENEMIES
- Gorynych Serpent: For each "head lost" (1/3hp) increases CD for 100%


SPECIAL MECHANICS:

Certain items increase chanse to meet unique enemies.


"""