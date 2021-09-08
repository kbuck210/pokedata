import re
import requests
import sqlite3
import os.path
import json
from os import path
from os import listdir
from os import rename
from bs4 import BeautifulSoup

# Downloaded HTML Directory & DB Path (check mac then windows)
dataDir = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/DexPages/'
if not path.exists(dataDir):
    dataDir = 'G:\\Android Development\\Database Stuff\\PokeRef\\PythonDev\\pokedata\\DexPages\\'

dbPath = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/BattleDex.db'
if not path.exists(dbPath):
    dbPath = 'C:\\Users\\kbuck\\AndroidStudioProjects\\PokeRef\\app\\src\\main\\assets\\databases\\BattleDex.db'

# =================
# TABLE: Ability
INSERT_ABILITY = 'INSERT INTO Ability(abName,abDesc,abDetails) VALUES (?,?,?)'
UPDATE_ABILITY = 'UPDATE Ability SET abName=?, abDesc=?, abDetails=? WHERE abId=?'
SELECT_AB_BY_NAME = 'SELECT * FROM Ability WHERE abName=? COLLATE NOCASE'
# =================
# TABLE: Attack
INSERT_ATTACK = 'INSERT INTO Attack(atkName) VALUES (?)'
UPDATE_ATTACK = 'UPDATE Attack SET atkName=? WHERE atkId=?'
SELECT_ATTACK = 'SELECT * FROM Attack WHERE atkName=? COLLATE NOCASE'
# =================
# TABLE: AttackByGen
INSERT_ATK_BYGEN = """INSERT INTO AttackByGen(
                        atkCategory,atkDesc,
                        atkEffect,bp,acc,pp,effPercent,
                        critRate,target,maxMove,maxPower,
                        priority,breaksProtect,contacting,
                        soundMove,bitingMove,punchMove,
                        copyable,thaws,reflectable,
                        gravityAffected,snatchable,
                        typeId,atkId,genId) 
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
UPDATE_ATK_BYGEN = """UPDATE AttackByGen SET atkCategory=?, atkDesc=?,
                        atkEffect=?,bp=?,acc=?,pp=?,effPercent=?,
                        critRate=?,target=?,maxMove=?,maxPower=?,
                        priority=?,breaksProtect=?,contacting=?,
                        soundMove=?,bitingMove=?,punchMove=?,
                        copyable=?,thaws=?,reflectable=?,
                        gravityAffected=?,snatchable=?,
                        typeId=?,atkId=?,genId=? 
                    WHERE atkFormId=?"""
SELECT_ATK_BYGEN = """SELECT * FROM AttackByGen
                        WHERE atkId=(SELECT atkId FROM Attack WHERE atkName=?)
                        AND genId=?"""
# =================
# TABLE: Item
INSERT_ITEM = 'INSERT INTO Item(itemName,itemDesc,itemEffect,itemIcon) VALUES (?,?,?,?)'
UPDATE_ITEM = 'UPDATE Item SET itemName=?, itemDesc=?, itemEffect=?, itemIcon=? WHERE itemId=?'
SELECT_ITEM_BY_NAME = 'SELECT * FROM Item WHERE itemName=? COLLATE NOCASE'
# =================
# TABLE: ItemsInDex
INSERT_ITEMSINDEX = 'INSERT INTO ItemsInDex(genId,itemId) VALUES (?,?)'
DELETE_ITEMSINDEX = 'DELETE FROM ItemsInDex WHERE genId=? AND itemId=?'
SELECT_ITEM_IN_DEX = 'SELECT * FROM ItemsInDex WHERE genId=? AND itemId=?'
# =================
# TABLE: PokeMovesByGen
INSERT_MOVESBYGEN = 'INSERT INTO PokeMovesByGen(genId,pokeFormId,atkFormId,groupDesc) VALUES (?,?,?,?)'
DELETE_MOVESBYGEN = 'DELETE FROM PokeMovesByGen WHERE genId=? AND pokeFormId=? AND atkFormId=?'
SELECT_MOVESBYGEN = 'SELECT * FROM PokeMovesByGen WHERE genId=? AND pokeFormId=? AND atkFormId=?'
# =================
# TABLE: Pokedex
INSERT_POKEDEX = 'INSERT INTO Pokedex(genId,genDescription) VALUES (?,?)'
UPDATE_POKEDEX = 'UPDATE Pokedex SET genDescription=? WHERE genId=?'
SELECT_DEX_BY_GEN = 'SELECT * FROM Pokedex WHERE genId=?'
# =================
# TABLE: Pokemon
INSERT_POKEMON = 'INSERT INTO Pokemon(nat_id,name) VALUES (?,?)'
UPDATE_POKEMON = 'UPDATE Pokemon SET nat_id=?, name=? WHERE pokeId=?'
SELECT_POKE_BY_NATID = 'SELECT * FROM Pokemon WHERE nat_id=?'
# =================
# TABLE: PokemonForm
INSERT_POKE_FORM = """INSERT INTO PokemonForm(formName,isBase,gender,
                        sprite,icon,shinySprite,
                        height,weight,baseHp,baseAtk,baseDef,
                        baseSpatk,baseSpdef,baseSpeed,evsEarned,
                        can_dmax,has_gmax,legendary,sub_legend,mythic,
                        type1,type2,ability1,ability2,abilityH,pokeId) 
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
UPDATE_POKE_FORM = """UPDATE PokemonForm SET formName=?, isBase=?, gender=?,
                        sprite=?,icon=?,shinySprite=?,
                        height=?,weight=?,baseHp=?,baseAtk=?,baseDef=?,
                        baseSpatk=?,baseSpdef=?,baseSpeed=?,evsEarned=?,
                        can_dmax=?,has_gmax=?,legendary=?,sub_legend=?,mythic=?,
                        type1=?,type2=?,ability1=?,ability2=?,abilityH=?,pokeId=?
                    WHERE pokeFormId=?"""
SELECT_BY_FORM_AND_DEXID = """SELECT * FROM PokemonForm
                            WHERE formName=?
                            AND pokeId=
                            (SELECT pokeId FROM Pokemon WHERE nat_id=?)"""
SELECT_PFORM_BY_DEXID = """SELECT * FROM PokemonForm
                            WHERE pokeId=(SELECT pokeId FROM Pokemon WHERE nat_id=?)"""
# =================
# TABLE: PokemonInDex
INSERT_POKEINDEX = 'INSERT INTO PokemonInDex(genId,pokeFormId) VALUES (?,?)'
DELETE_POKEINDEX = 'DELETE FROM PokemonInDex WHERE genId=? AND pokeFormId=?'
SELECT_POKEINDEX = 'SELECT * FROM PokemonInDex WHERE genId=? AND pokeFormId=?'
# =================
# TABLE: Team
INSERT_TEAM = 'INSERT INTO Team(teamName,targetGen) VALUES (?,?)'
UPDATE_TEAM = 'UPDATE Team SET teamName=?, targetGen=? WHERE teamId=?'
DELETE_TEAM = 'DELETE FROM Team WHERE teamId=?'
# =================
# TABLE: TeamPokemon
INSERT_TEAM_POKE = """INSERT INTO TeamPokemon(level,gender,shiny,
                        hpIV,atkIV,defIV,spatkIV,spdefIV,speedIV,
                        hpEV,atkEV,defEV,spatkEV,spdefEV,speedEV,
                        nature,pokeForm,heldItem,ability,
                        attack1,attack2,attack3,attack4,teamId) 
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
UPDATE_TEAM_POKE = """UPDATE TeamPokemon SET level=?,gender=?,shiny=?,
                        hpIV=?,atkIV=?,defIV=?,spatkIV=?,spdefIV=?,speedIV=?,
                        hpEV=?,atkEV=?,defEV=?,spatkEV=?,spdefEV=?,speedEV=?,
                        nature=?,pokeForm=?,heldItem=?,ability=?,
                        attack1=?,attack2=?,attack3=?,attack4=?,teamId=?
                    WHERE teamPokeId=?"""
DELETE_TEAM_POKE = 'DELETE FROM TeamPokemon WHERE teamPokeId=?'
# =================
# TABLE: Type
INSERT_TYPE = 'INSERT INTO Type(typeName) VALUES (?)'
DELETE_TYPE = 'DELETE FROM Type WHERE typeId=?'
SELECT_TYPE_BY_NAME = 'SELECT * FROM Type WHERE typeName=? COLLATE NOCASE'

# Connect to database
con = sqlite3.connect(dbPath)

# Placeholder for legendary pokemon tables (only initiate 1 request)
legTables = []

# Tables instantiated every time (pre-declared for testing
allTables = []
statTables = []
megaTables = []
allAbilities = []

# ============================
# Default Initialization
def initialize():
    buildGens()
    buildTypes()

# ==========================
# Initialize Static Data (Gens, Types)
def buildGens():
    cur = con.cursor()
    for gen in range(1,9):
        cur.execute('SELECT EXISTS('+SELECT_DEX_BY_GEN+')',[gen])
        if not cur.fetchone()[0]:
            cur.execute(INSERT_POKEDEX, [ gen, getRoman(gen) ])
            con.commit()
    return
            
def getRoman( num ):
    if num == 1:
        return 'I'
    elif num == 2:
        return 'II'
    elif num == 3:
        return 'III'
    elif num == 4:
        return 'IV'
    elif num == 5:
        return 'V'
    elif num == 6:
        return 'VI'
    elif num == 7:
        return 'VII'
    elif num == 8:
        return 'VIII'
    else:
        return None

def buildTypes():
    cur = con.cursor()
    # BUG
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Bug'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Bug'])
        con.commit()
    # DARK
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Dark'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Dark'])
        con.commit()
    # DRAGON
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Dragon'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Dragon'])
        con.commit()
    # ELECTRIC
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Electric'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Electric'])
        con.commit()
    # FAIRY
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Fairy'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Fairy'])
        con.commit()
    # FIGHTING
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Fighting'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Fighting'])
        con.commit()
    # FIRE
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Fire'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Fire'])
        con.commit()
    # FLYING
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Flying'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Flying'])
        con.commit()
    # GHOST
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Ghost'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Ghost'])
        con.commit()
    # GRASS
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Grass'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Grass'])
        con.commit()
    # GROUND
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Ground'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Ground'])
        con.commit()
    # ICE
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Ice'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Ice'])
        con.commit()
    # NORMAL
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Normal'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Normal'])
        con.commit()
    # POISON
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Poison'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Poison'])
        con.commit()
    # PSYCHIC
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Psychic'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Psychic'])
        con.commit()
    # ROCK
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Rock'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Rock'])
        con.commit()
    # STEEL
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Steel'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Steel'])
        con.commit()
    # WATER
    cur.execute('SELECT EXISTS('+SELECT_TYPE_BY_NAME+')',['Water'])
    if not cur.fetchone()[0]:
        cur.execute(INSERT_TYPE, ['Water'])
        con.commit()
    return

# ====================
# Insert/Update ability data based on the HTML
def updateAbility( soup ):
    abilityTables = getAllTables( soup )
    table = abilityTables[1]
    trs = table.find_all('tr')
    abNameRow = None
    abDescRow = None
    abEffectRow = None
    for r in range(0, len(trs)):
        td = trs[r].find('td').text
        if td and td == 'Name' and not abNameRow:
            abNameRow = trs[r+1]
        elif td and td == 'Game\'s Text:' and not abDescRow:
            abDescRow = trs[r+1]
        elif td and td == 'In-Depth Effect:' and not abEffectRow:
            abEffectRow = trs[r+1]
    abName = None
    abDesc = None
    abEffect = None
    if abNameRow:
        abName = abNameRow.find('td').text
        if abName:
            abName = abName.strip()
    if abDescRow:
        abDesc = abDescRow.find('td').text
        if abDesc:
            abDesc = abDesc.strip()
    if abEffectRow:
        abEffect = abEffectRow.find('td').text
        if abEffect:
            abEffect = abEffect.strip()

    # check that a good result populated
    if abName and abDesc:
        cur = con.cursor()
        cur.execute('SELECT EXISTS('+SELECT_AB_BY_NAME+')',[abName])
        if not cur.fetchone()[0]:
            cur.execute(INSERT_ABILITY, [abName, abDesc, abEffect])
            con.commit()
            print('Inserted: ' + abName)
        else:
            cur.execute(SELECT_AB_BY_NAME,[abName])
            ability = cur.fetchone()
            if abName != ability[1] or abDesc != ability[2] or abEffect != ability[3]:
                abId = ability[0]
                cur.execute(UPDATE_ABILITY,[abName, abDesc, abEffet, abId])
                print('Updated: ' + abName)
    else:
        print('Failed to get/update ability for ' + html)

# ====================
# Insert/Update Item and ItemForGen based on the HTML
def updateItem( itemName, soup, write ):
    tableContainer = soup.find('table', class_='dextable').parent
    itemTables = tableContainer.find_all('table', class_='dextable', recursive=False)
    table = itemTables[2]
    trs = table.find_all('tr')
    gameRow1Cols = trs[2].find_all('td')
    singlerow = False
    if len(trs) > 4:
        gameRow2Cols = trs[4].find_all('td')
    else:
        gameRow2Cols = None
        singlerow = True
    gens = []
    # loop over columns in each row
    # column has a pokeball in it if the item is available in that gen
    for col in range(0, len(gameRow1Cols)):
        data = gameRow1Cols[col]
        if data.find('img'):
            gen = getItemGen(1, col, singlerow)
            if not gen in gens:
                gens.append(gen)
    if not singlerow:
        for col in range(0, len(gameRow2Cols)):
            data = gameRow2Cols[col]
            if data.find('img'):
                gen = getItemGen(2, col, singlerow)
                if not gen in gens:
                    gens.append(gen)

    # Get the game text for the item
    effectTable = itemTables[3]
    itemEffR = effectTable.find_all('tr')[1]
    itemEff = itemEffR.find('td').text
    # Get the item description
    gameTable = None
    if len(itemTables) > 4:
        gameTable = itemTables[4]
    else:
        # html broken, find from all tables
        allTables = getAllTables(soup)
        for table in allTables:
            if table.find('td').text == 'Flavour Text':
                gameTable = table
                break
    if gameTable:
        lastGame = gameTable.find_all('tr')[-1]
        gameDesc = lastGame.find_all('td')[-1].text
    else:
        gameDesc = None
    # Create the icon name
    itemIcon = 'item_' + itemName.lower().replace(' ','_') + '.png'

    if write:
        # Write/update the DB item
        cur = con.cursor()
        cur.execute(SELECT_ITEM_BY_NAME,[itemName])
        item = cur.fetchone()
        if not item:
            cur.execute(INSERT_ITEM,[itemName,gameDesc,itemEff,itemIcon])
            con.commit()
            print('Inserted ' + itemName)
            # select the record just inserted to get back the itemId
            cur.execute(SELECT_ITEM_BY_NAME,[itemName])
            itemId = cur.fetchone()[0]
        else:
            itemId = item[0]
            cur.execute(UPDATE_ITEM,[itemName,gameDesc,itemEff,itemIcon, itemId])
            con.commit()
            print('Updated ' + itemName)

        # For each gen where the item exists, create a gen/item relationship
        for gen in gens:
            # insert if not existing
            cur.execute(SELECT_ITEM_IN_DEX,[gen,itemId])
            itemInDex = cur.fetchone()
            if not itemInDex and gen and itemId:
                cur.execute(INSERT_ITEMSINDEX,[gen,itemId])
                print('Inserted ' + itemName + ' in gen ' + str(gen))
    else:
        print('Item ' + itemName + ' found in gens: ' + str(gens))
        print('Item desc: ' + gameDesc)
        print('Item eff: ' + itemEff)
    

def getItemGen( row, col, singlerow ):
    if not singlerow:
        genMap = {
            8: { 1: [], 2: [10,11] },
            7: { 1: [], 2: [4,5,6,7] },
            6: { 1: [], 2: [0,1] },
            5: { 1: [10,11,12,13], 2: [] },
            4: { 1: [6,7], 2: [] },
            3: { 1: [3,4], 2: [2,3] },
            2: { 1: [1,2,8,9], 2: [] },
            1: { 1: [0,5], 2: [] }
            }
    else:
        genMap = {
            8: { 1: [], 2: []},
            7: { 1: [18,19,20,21], 2: []},
            6: { 1: [14,15], 2: []},
            5: { 1: [10,11,12,13], 2: []},
            4: { 1: [6,7], 2: []},
            3: { 1: [3,4,16,17], 2: []},
            2: { 1: [1,2,8,9], 2: []},
            1: { 1: [0,5], 2: []}
            }
    for key in genMap.keys():
        if col in genMap[key][row]:
            return key

# ====================
# Insert/Update to the Pokemon table based on the HTML
def updatePokemon( soup, dexId ):
    name = getPokeName(soup, dexId)
    if name is not None:
        cur = con.cursor()
        cur.execute(SELECT_POKE_BY_NATID,[dexId])
        poke = cur.fetchone();
        if not poke:
            cur.execute(INSERT_POKEMON,[dexId,name])
            con.commit()
            print('Inserted #' + str(dexId).zfill(3) + ' ' + name)
            
        # result format: (1, 1, 'Bulbasaur')
        elif poke[2] != name:
            cur.execute(UPDATE_POKEMON,[dexId,name,poke[0]])
            con.commit()
            print('Updated #' + str(dexId).zfill(3) + ' ' + name)
        else:
            print('No change for #' + str(dexId).zfill(3) + ' ' + name)
    else:
        print('Name is None for ' + dexId)
    return

def getPokeName( soup, dexId ):
    dexTab = soup.find('table', class_='dextab')
    header = dexTab.find('h1')
    if (header is None):
        # old gens may use outdated html tags
        header = dexTab.find('b')
        if header is None:
            return None

    # h1 in format: '\xa0#006 Charizard'
    arr = header.text.strip().split()
    # validate format & id
    if (len(arr) < 2):
        return None
    if (len(arr[0].split('#')) < 2):
        return None
    if (dexId != int(arr[0].split('#')[1])):
        return None

    # validated ID, get name
    # check if spaces in the name
    name = ''
    if (len(arr) > 2):
        for i in range(1, len(arr)):
            name = name + ' ' + arr[i]
        name = name.strip()
    else:
        name = arr[1].strip()

    return name

# ====================
# Insert/Update to the PokemonForms table based on the HTML
def updatePokemonForm( pokeName, forms, dexId, gen ):
    formNames = getFormNames( pokeName, statTables, megaTables )
    legTables = getLegendTables()

    # Check if any forms not yet created
    for formIndex in range(0, len(formNames)):
        formName = formNames[formIndex]
        
        # Skip create if base and already processed but changed name, but create gen relationship
        if formName == 'Base' and formName not in forms and len(forms) > 0:
            addPokeFormToGen( pokeName, formName, dexId, gen )
            continue
        # If new form, create it
        elif formName not in forms:
            # base form
            isBase = formName == 'Base'
            # mega form
            isMega = formName.startswith('Mega ') or \
                     formName.startswith('Primal ') or \
                     formName.startswith('Ultra ')
            
            # gender (genderless = 0, gendered = 1, male-only = 2, female-only = 3)
            gender = getGender( allTables )

            # icon
            # shinySprite
            # sprite (need to refactor multiforms)
            if len(formNames) < 2:
                sprite = 'sp_' + str(dexId).zfill(3) + '.png'
                shiny = 'sh_' + str(dexId).zfill(3) + '.png'
                icon = 'ic_' + str(dexId).zfill(3) + '.png'
            else:
                suffix = ''
                if formName != 'Base' and not isMega:
                    suffix = formName.replace(' ', '')
                elif formName != 'Base':
                    suffix = 'mega'
                    if len(formName.split()) >= 3:
                        suffix = suffix.join(formName.split()[2:])
                sprite = 'sp_' + str(dexId).zfill(3) + '_' + suffix + '.png'
                shiny = 'sh_' + str(dexId).zfill(3) + '_' + suffix + '.png'
                icon = 'ic_' + str(dexId).zfill(3) + '_' + suffix + '.png'

            # height
            if not isMega:
                height = getHeight(formIndex, len(formNames), allTables)
            else:
                height = getMegaHeight(formName, megaTables)
            # weight
            if not isMega:
                weight = getWeight(formIndex, len(formNames), allTables)
            else:
                weight = getMegaWeight(formName, megaTables)
            
            # baseHp
            # baseAtk
            # baseDef
            # baseSpatk
            # baseSpdef
            # baseSpeed
            formStats = {}
            if not isMega:
                formStats[formName] = getBaseStats( pokeName, formStats, formName, statTables )
            else:
                formStats[formName] = getMegaStats(formName, megaTables)

            
            baseHp = formStats[formName]['baseHp']
            baseAtk = formStats[formName]['baseAtk']
            baseDef = formStats[formName]['baseDef']
            baseSpatk = formStats[formName]['baseSpatk']
            baseSpdef = formStats[formName]['baseSpdef']
            baseSpeed = formStats[formName]['baseSpeed']

            # EVs earned
            evsEarned = getEVsEarned( formName, allTables )
            
            # can_dmax
            can_dmax = getCanDmax( allTables ) if not isMega else None
            
            # has_gmax
            if can_dmax is not None:
                has_gmax = getHasGmax( allTables ) if not isMega else False
            else:
                has_gmax = None

            # sub_legend
            # legendary
            # mythic
            sub_legend = getIsLegend( pokeName, legTables[0] )
            legendary = getIsLegend( pokeName, legTables[1] )
            mythic = getIsLegend( pokeName, legTables[2] )
            
            # type1 name
            # type2 name
            if not isMega:
                print('getting types for: ' + formName)
                formTypes = getPokeFormTypes( pokeName, formName, allTables)
            else:
                print('getting types for: ' + formName)
                formTypes = getMegaTypes( formName, megaTables)
            # check result to see if formName needs to be updated from base
            formKey = list(formTypes.keys())[0]
            if formName == 'Base' and formKey != 'Base':
                formName = formKey
            # lookup type ids:
            cur = con.cursor()
            cur.execute(SELECT_TYPE_BY_NAME,[formTypes[formName][0]])
            type1 = cur.fetchone()[0]
            type2 = None
            if len(formTypes[formName]) > 1:
                cur.execute(SELECT_TYPE_BY_NAME,[formTypes[formName][1]])
                type2 = cur.fetchone()[0]
            
            # ability1 name
            # ability2 name
            # abilityH name
            if not isMega:
                # certain forms are extensions of base form, get base abilites
                if formName == 'Zen Mode' or formName == '10% Forme' or formName == 'Complete Form':
                    abilities = getFormAbilities(formName, True, allTables)
                else:
                    abilities = getFormAbilities( formName, isBase, allTables )
            else:
                abilities = getMegaAbilities( formName, megaTables )

            for a in range(0, len(abilities)):
                if abilities[a]:
                    if abilities[a] == 'Compoundeyes':
                        abilities[a] = 'Compound Eyes'
                    if not abilities[a] in allAbilities:
                        allAbilities.append(abilities[a])

            # Get the abilities from the database
            cur.execute(SELECT_AB_BY_NAME,[abilities[0]])
            ab1 = cur.fetchone()
            ability1 = ab1[0] if ab1 else None
            cur.execute(SELECT_AB_BY_NAME,[abilities[1]])
            ab2 = cur.fetchone()
            ability2 = ab2[0] if ab2 else None
            cur.execute(SELECT_AB_BY_NAME,[abilities[2]])
            abH = cur.fetchone()
            abilityH = abH[0] if abH else None
            
            # pokeId
            cur.execute(SELECT_POKE_BY_NATID,[dexId])
            poke = cur.fetchone();
            pokeId = poke[0] if poke is not None else None

            ## DB UPDATE ##
            cur.execute(SELECT_BY_FORM_AND_DEXID,[formName,dexId])
            pokeForm = cur.fetchone()
            # If it doesn't exist, insert
            if not pokeForm:
                cur.execute(INSERT_POKE_FORM,[formName,isBase,gender,
                                              sprite, icon, shiny,
                                              height, weight, baseHp, baseAtk, baseDef,
                                              baseSpatk, baseSpdef, baseSpeed, evsEarned,
                                              can_dmax, has_gmax, legendary, sub_legend, mythic,
                                              type1, type2, ability1, ability2, abilityH, pokeId])
                con.commit()
                print('Inserted ' + pokeName + ' - ' + formName)
            # Otherwise update
            else:
                cur.execute(UPDATE_POKE_FORM,[formName,isBase,gender,
                                              sprite, icon, shiny,
                                              height, weight, baseHp, baseAtk, baseDef,
                                              baseSpatk, baseSpdef, baseSpeed, evsEarned,
                                              can_dmax, has_gmax, legendary, sub_legend, mythic,
                                              type1, type2, ability1, ability2, abilityH, pokeId, pokeForm[0]])
                con.commit()
                print('Updated ' + pokeName + ' - ' + formName)

            # After insert/update add gen relation if needed
            addPokeFormToGen( pokeName, formName, dexId, gen )
                    
            # Append formname to not reprocess
            forms.append(formName)

        # If not new form, add to gen if required
        else:
            addPokeFormToGen( pokeName, formName, dexId, gen )
            
#            forms[formName] = {}
#            forms[formName]['isBase'] = isBase
#            forms[formName]['gender'] = gender
#            forms[formName]['sprite'] = sprite
#            forms[formName]['icon'] = icon
#            forms[formName]['shiny'] = shiny
#            forms[formName]['height'] = height
#            forms[formName]['weight'] = weight
#            forms[formName]['stats'] = {}
#            forms[formName]['stats']['baseHP'] = baseHp
#            forms[formName]['stats']['baseAtk'] = baseAtk
#            forms[formName]['stats']['baseDef'] = baseDef
#            forms[formName]['stats']['baseSpatk'] = baseSpatk
#            forms[formName]['stats']['baseSpdef'] = baseSpdef
#            forms[formName]['stats']['baseSpeed'] = baseSpeed
#            forms[formName]['can_dmax'] = can_dmax
#            forms[formName]['has_gmax'] = has_gmax
#            forms[formName]['legend'] = legendary
#            forms[formName]['sub_legend'] = sub_legend
#            forms[formName]['mythic'] = mythic
#            forms[formName]['type1'] = type1
#            forms[formName]['type2'] = type2
#            forms[formName]['abilities'] = abilities
#            forms[formName]['dexId'] = dexId

def addPokeFormToGen( pokeName, formName, dexId, gen ):
    cur = con.cursor()
    cur.execute(SELECT_BY_FORM_AND_DEXID,[formName,dexId])
    pokeForm = cur.fetchone()
    if pokeForm:
        # validate the gen relationship doesn't already exist
        cur.execute(SELECT_POKEINDEX,[gen,pokeForm[0]])
        exists = cur.fetchone()
        if not exists:
            cur.execute(INSERT_POKEINDEX,[gen,pokeForm[0]])
            con.commit()
            print('Added ' + pokeName + ' - ' + formName + ' to Gen' + str(gen))

def getAllTables( soup ):
    return soup.find_all('table', class_='dextable')

def getStatTables( allTables ):
    statTables = []
    for table in allTables:
        headers = table.find_all('h2')
        bolds = table.find_all('b')
        for title in headers:
            if not 'Mega Evolution' in title.text and title.text.startswith('Stats'):
                statTables.append(table)
        for title in bolds:
            if not 'Mega Evolution' in title.text and title.text.startswith('Stats'):
                statTables.append(table)
    return statTables

def getMegaTables( pokeName, allTables ):
    megaTables = []
    for i in range(0, len(allTables)):
        bolds = allTables[i].find_all('b')
        for bold in bolds:
            if bold.text and (bold.text.startswith('Mega Evolution') or \
                              bold.text.startswith('Primal Reversion') or \
                              bold.text.startswith('Ultra Burst')):
                megaName = bold.text.replace('Evolution', pokeName)
                megaName = megaName.replace('Reversion', pokeName)
                megaName = megaName.replace('Burst', pokeName)
                expanded = len(allTables[i].find_all('tr', recursive=False)) == 3
                # Spread formatting
                if expanded:
                    megaSpriteTable = allTables[i]
                    megaInfoTable = allTables[i+1]
                    megaAbilityTable = allTables[i+2]
                    megaStatsTable = allTables[i+4]
                # Compact formatting
                else:
                    megaSpriteTable = allTables[i]
                    megaInfoTable = allTables[i]
                    megaAbilityTable = allTables[i+1]
                    megaStatsTable = allTables[i+3]
                megaTables.append((megaName, megaSpriteTable, megaInfoTable, megaAbilityTable, megaStatsTable, expanded))
    return megaTables

def getFormNames( pokeName, statTables, megaTables ):
    forms = []
    # They took shortcuts with Rotom...set manually
    if pokeName == 'Rotom':
        forms = ['Base', 'Frost Rotom', 'Heat Rotom', 'Mow Rotom', 'Fan Rotom', 'Wash Rotom']
    else:
        for table in statTables:
            header = table.find('h2')
            if header is None:
                header = table.find('b')
            if header is not None:
                formName = translateFormName(header.text, pokeName)
                if formName not in forms and 'Reversion' not in formName and 'Ultra Burst' not in formName:
                    forms.append(formName)

        for tables in megaTables:
            megaName = tables[0]
            if megaName is not None and megaName not in forms:
                forms.append(megaName)
    return forms

def translateFormName( headerText, pokeName ):
    if headerText.strip() == 'Stats':
        return 'Base'
    else:
        toks = headerText.split('-',1)
        formName = toks[-1].strip()
        if formName.startswith('Alola'):
            return 'Alolan ' + pokeName
        elif formName.startswith('Galar'):
            return 'Galarian ' + pokeName
        else:
            return formName

def getGender( allTables ):
    # find gender row
    genderRow = None
    for i in range(0, len(allTables)):
        trs = allTables[i].find_all('tr', recursive=False)
        for r in range(0, len(trs)):
            for td in trs[r].find_all('td'):
                if td.text and td.text.startswith('Gender'):
                    genderRow = trs[r+1]
                    break
                elif td.find('b') and td.find('b').text.startswith('Gender'):
                    genderRow = trs[r+1]
                    break;
            if genderRow:
                break;
        if genderRow:
            break
    if not genderRow:
        return None
    gendCol = genderRow.find_all('td', class_='fooinfo')[3]
    # Genderless pokemon have no table definition
    gendPers = gendCol.find_all('tr')
    if len(gendPers) == 0:
        return 0
    else:
        # get the percentage for male & female
        malePer = gendPers[0].find_all('td')[1].text
        m = re.search('[\d.]+', malePer)
        malePer = m.group(0)
        if malePer:
            malePer = int(malePer)
        femalePer = gendPers[1].find_all('td')[1].text
        m = re.search('[\d.]+', femalePer)
        femalePer = m.group(0)
        if femalePer:
            femalePer = int(femalePer)
        
        if malePer == 100:
            return 2
        elif femalePer == 100:
            return 3
        else:
            return 1

def getHeight( formIndex, numForms, allTables ):
    # find height row
    heightRow = None
    for i in range(0, len(allTables)):
        trs = allTables[i].find_all('tr', recursive=False)
        for r in range(0, len(trs)):
            for td in trs[r].find_all('td', recursive=False):
                if td.text and td.text == 'Height':
                    heightRow = trs[r+1]
                    break
            if heightRow:
                break
        if heightRow:
            break
    if not heightRow:
        return None
    # table with height/weight is 2nd table, 4th row
    #heightRow = allTables[1].find_all('tr', recursive=False)[3]
    heightCol = heightRow.find_all('td', class_='fooinfo')[1]
    height = heightCol.text
    # validate format
    if len(height.replace('/','').split()) % numForms == 0:
        return height.replace('/','').split()[formIndex]
    else:
        return None

def getMegaHeight( formName, megaTables ):
    for mega in megaTables:
        if formName == mega[0]:
            rowInd = 3 if mega[5] else 4
            megaCol = 2 if mega[5] else 1
            heightRow = mega[megaCol].find_all('tr', recursive=False)[rowInd]
            heightCol = heightRow.find_all('td', class_='fooinfo')[1]
            height = heightCol.text
            return height.replace('/','').split()[0]
                

def getWeight( formIndex, numForms, allTables ):
    weightRow = None
    # find weight row
    for i in range(0, len(allTables)):
        trs = allTables[i].find_all('tr', recursive=False)
        for r in range(0, len(trs)):
            for td in trs[r].find_all('td', recursive=False):
                if td.text and td.text == 'Weight':
                    weightRow = trs[r+1]
                    break
            if weightRow:
                break
        if weightRow:
            break
    if not weightRow:
        return None
    weightCol = weightRow.find_all('td', class_='fooinfo')[2]
    weight = weightCol.text
    # validate format
    if len(weight.replace('/','').split()) % numForms == 0:
        return weight.replace('/','').split()[formIndex]
    else:
        return None

def getMegaWeight( formName, megaTables ):
    for mega in megaTables:
        if formName == mega[0]:
            rowInd = 3 if mega[5] else 4
            megaCol = 2 if mega[5] else 1
            weightRow = mega[megaCol].find_all('tr', recursive=False)[rowInd]
            weightCol = weightRow.find_all('td', class_='fooinfo')[2]
            weight = weightCol.text
            return weight.replace('/', '').split()[0]

def getBaseStats( pokeName, formStats, formName, statTables ):
    
    # find the stat table for the specified form
    for i in range(0, len(statTables)):
        table = statTables[i]
        allRows = table.find_all('tr')
        header = allRows[0].find('h2')
        if header is None:
            header = allRows[0].find('b')
        # again they cheated with Rotom...need separate check for it
        if header is not None and \
           (formName == translateFormName(header.text, pokeName) or \
            (pokeName == 'Rotom' and translateFormName(header.text, pokeName) == 'Alternate Forms')):
            baseRow = allRows[2]
            statRows = baseRow.find_all('td')
            baseStats = {}
            baseStats['baseHp'] = statRows[1].text
            baseStats['baseAtk'] = statRows[2].text
            baseStats['baseDef'] = statRows[3].text
            baseStats['baseSpatk'] = statRows[4].text
            baseStats['baseSpdef'] = statRows[5].text
            baseStats['baseSpeed'] = statRows[6].text
            if not formName in list(formStats.keys()):
                return baseStats
            
def getMegaStats( formName, megaTables ):
    for mega in megaTables:
        if formName == mega[0]:
            statTable = mega[4]
            allRows = statTable.find_all('tr')
            baseRow = allRows[2]
            statRows = baseRow.find_all('td')
            baseStats = {}
            baseStats['baseHp'] = statRows[1].text
            baseStats['baseAtk'] = statRows[2].text
            baseStats['baseDef'] = statRows[3].text
            baseStats['baseSpatk'] = statRows[4].text
            baseStats['baseSpdef'] = statRows[5].text
            baseStats['baseSpeed'] = statRows[6].text
            return baseStats

def getEVsEarned( formName, allTables ):
    # find EV Row
    evRow = None
    for i in range(0, len(allTables)):
        trs = allTables[i].find_all('tr', recursive=False)
        for r in range(0, len(trs)):
            for td in trs[r].find_all('td', recursive=False):
                if td.text and td.text == 'Effort Values Earned':
                    evRow = trs[r+1]
                    break
            if evRow:
                break
        if evRow:
            break
    if not evRow:
        return None
    evCol = evRow.find_all('td', class_='fooinfo')[2]
    evs = evCol.text.split('Point(s)')
    # slice empty split
    evs = evs[:len(evs)-1]
    # check whether only one set of EVs provided
    if len(evs) == 1:
        toks = evs[0].strip().split(' ', 1)
        val = toks[0]
        stat = translateStatString(toks[1])
        return val + ' ' + stat
    # if multiple, return evs for form
    else:
        # Check if there are separate EVs for different forms
        for form in evs:
            m = re.search(r'\d', form)
            if m and formName == form[:m.start()]:
                toks = form[m.start():].strip().split(' ', 1)
                val = toks[0]
                stat = translateStatString(toks[1])
                return val + ' ' + stat
            
        # Check if there are multiple EVs for single form
        sameMon = True
        for form in evs:
            m = re.search(r'\d', form)
            if m.start() != 0:
                sameMon = False

        if sameMon:
            modified = []
            for ev in evs:
                m = re.search(r'\d', form)
                toks = form[m.start():].strip().split(' ', 1)
                val = toks[0]
                stat = translateStatString(toks[1])
                modified.append(val + ' ' + stat)

            if len(modified) > 0:
                return ', '.join(modified)
          
        return None

def translateStatString( stat ):
    if stat.endswith('Sp. Attack'):
        return 'SpAtk'
    elif stat.endswith('Sp.Attack'):
        return 'SpAtk'
    elif stat.endswith('Sp. Defense'):
        return 'SpDef'
    elif stat.endswith('Sp.Defense'):
        return 'SpDef'
    elif stat.endswith('Attack'):
        return 'Atk'
    elif stat.endswith('Defense'):
        return 'Def'
    else:
        return stat

def getCanDmax( allTables ):
    # find dmx row, if it exists
    dmaxRow = None
    for i in range(0, len(allTables)):
        trs = allTables[i].find_all('tr', recursive=False)
        for r in range(0, len(trs)):
            tds = trs[r].find_all('td', recursive=False)
            for td in tds:
                if td.text and td.text == 'Dynamax Capable?':
                    dmaxRow = trs[r+1]
                    break
            if dmaxRow:
                break
        if dmaxRow:
            break
    if not dmaxRow:
        return None
    dmaxCol = dmaxRow.find_all('td', class_='fooinfo')[3]
    return not dmaxCol.text.strip().endswith('cannot Dynamax')

def getHasGmax( allTables ):
    # look for table with header with 'gigantimax' (usually last table)
    for table in reversed(allTables):
        header = table.find('h2')
        if header is None:
            header = table.find('b')
        if header is not None and header.text.strip().startswith('Gigantamax'):
            return True
    return False

def getLegendTables():
    legFile = dataDir + 'legends.html'
    with open(legFile, 'r', encoding='utf-8') as f:
        contents = f.read()
        lsoup = BeautifulSoup(contents, 'html.parser')
        return lsoup.find_all('table', class_='trainer')

def getIsLegend( pokeName, legTable ):
    legs = []
    for poke in legTable.find_all('a'):
        href = poke['href'].split('/')[1]
        if not href.startswith('abilitydex') and poke.text and poke.text not in legs:
            legs.append(poke.text)
    return pokeName.upper() in (leg.upper() for leg in legs)

def getPokeFormTypes( pokeName, formName, allTables ):
    # find typeRow
    typeRow = None
    for i in range(0, len(allTables)):
        trs = allTables[i].find_all('tr', recursive=False)
        for r in range(0, len(trs)):
            tds = trs[r].find_all('td', recursive=False)
            for td in tds:
                if td.text and td.text == 'Type':
                    typeRow = trs[r+1]
                    break
            if typeRow:
                break
        if typeRow:
            break
    if not typeRow:
        return None
    typeCol = typeRow.find('td', class_='cen')
    if not typeCol:
        typeCol = typeRow.find('td', { 'align': 'center' })
    if not typeCol:
        return None
    # if multiple forms, will structure with table, each tr is for a form
    # otherwise there is no table just the img links
    formTypes = typeCol.find_all('tr')
    types = []
    if len(formTypes) > 0:
        for i in range(0, len(formTypes)):
            formData = formTypes[i].find_all('td')
            foundName = formData[0].text
            # check if found name matches specified form name
            if (formName == 'Base' and foundName == pokeName) or \
                formName == foundName or \
                (foundName.startswith('Alola') and formName.startswith('Alola')) or \
                (foundName.startswith('Galar') and formName.startswith('Galar')) or \
                (foundName == pokeName + ' ' + formName) or \
                (foundName == formName.split(pokeName)[0].strip()):
                # found the types for the specified form
                for img in formData[1].find_all('img'):
                    toks = img['src'].split('/')
                    types.append(toks[len(toks)-1].split('.')[0])
            elif formName == 'Base' and i == 0:
                # found the base form, but form needs name updated
                formName = foundName
                for img in formData[1].find_all('img'):
                    toks = img['src'].split('/')
                    types.append(toks[len(toks)-1].split('.')[0])
    else:
        # no form type rows, get img direct from typeCol
        for img in typeCol.find_all('img'):
            toks = img['src'].split('/')
            types.append(toks[len(toks)-1].split('.')[0])

    # return as mapped object to update the form name where required
    return { formName: types }

def getMegaTypes( formName, megaTables ):
    for mega in megaTables:
        if formName == mega[0]:
            types = []
            rowInd = 1 if mega[5] else 2
            megaCol = 2 if mega[5] else 1
            typeRow = mega[megaCol].find_all('tr')[rowInd]
            typeCol = typeRow.find('td', class_='cen')
            for img in typeCol.find_all('img'):
                toks = img['src'].split('/')
                types.append(toks[len(toks)-1].split('.')[0])
            return { formName: types }

def getFormAbilities( formName, isBase, allTables ):
    # find ability row
    abRow = None
    for i in range(0, len(allTables)):
        trs = allTables[i].find_all('tr', recursive=False)
        for r in range(0, len(trs)):
            td = trs[r].find('td')
            if td and td.find('b') and td.find('b').text:
                if td.find('b').text.startswith('Abilities'):
                    abRow = trs[r+1]
                    break
        if abRow:
            break
    if not abRow:
        return None
    # Abilities table is 3rd table, 2nd row
    allAbs = abRow.find('td').find_all('b')
    ability1 = None
    ability2 = None
    abilityH = None
    # Base forms don't have lead title
    foundForm = True if isBase else formName == 'Base'
    # Check whether multiforms use same abilities
    singleSet = True
    for i in range(0, len(allAbs)):
        ab = allAbs[i].text.strip()
        # Check for alternate form ability designation
        if ab != 'Hidden Ability' and ab != 'Other Ability' and (ab.endswith('Abilities') or ab.endswith('Ability')):
            singleSet = False

    # Reset foundForm if singleSet
    if not foundForm and singleSet:
        foundForm = True
    
    for i in range(0, len(allAbs)):
        ab = allAbs[i].text
        # First check hidden ability so that can use 'ability' as descriminator
        if foundForm and ab.strip() == 'Hidden Ability':
            abilityH = allAbs[i+1].text.strip()
            break
        # Next check if it is a form change line, then check if is specified form
        elif ab.strip().endswith('Abilities') or ab.strip().endswith('Ability'):
            form = ab.strip().rsplit(' ',1)[0]
            if formName.startswith('Alola') and form.startswith('Alola'):
                foundForm = True
            elif formName.startswith('Galar') and form.startswith('Galar'):
                foundForm = True
            elif form.startswith('Other'):
                foundForm = True
            else:
                foundForm = form == formName
        # If working with specified form set ability 1 if not already set
        elif foundForm and ability1 == None:
            ability1 = allAbs[i].text.strip()
        # If working with found form and ability 1 is set, set ability 2
        elif foundForm:
            ability2 = allAbs[i].text.strip()

    return [ability1, ability2, abilityH]

def getMegaAbilities( formName, megaTables ):
    for mega in megaTables:
        if formName == mega[0]:
            #megaCol = 3 if mega[5] else 2
            abRow = mega[3].find_all('tr')[1]
            megaAbility = abRow.find('td').find('b').text
            return [megaAbility, None, None]

def getLevelTables():
    tables = []
    for t in allTables:
        tr = t.find('tr')
        td = tr.find('h3')
        if td and 'Level Up' in td.text:
            tables.append(t)
    return tables

def getLevelUpMoves( formName ):
    table = None
    levelTables = getLevelTables()
    if len(levelTables) > 0:
        table = levelTables[0]
    if not table:
        return {}

    allRows = table.find_all('tr', recursive=False)
    moves = {}
    name = None
    for r in range(2, len(allRows)):
        # even rows are info rows, odd are descriptions
        if r % 2 == 0:
            infoTds = allRows[r].find_all('td', recursive=False)
            if len(infoTds) > 7:
                name = infoTds[1].find('a').text
                moves[name] = {
                    'level': infoTds[0].text,
                    'type': infoTds[2].find('img')['src'].rsplit('/',1)[1].split('.')[0],
                    'category': infoTds[3].find('img')['src'].rsplit('/',1)[1].split('.')[0],
                    'bp': infoTds[4].text,
                    'acc': infoTds[5].text,
                    'pp': infoTds[6].text,
                    'effPer': infoTds[7].text
                    }
        else:
            if name and name in moves:
                moves[name]['desc'] = allRows[r].find('td').text
            name = None
    return moves

def getAttackTables():
    tables = {}
    for t in allTables:
        h = t.find('tr').find('h3')
        header = h.text if h else None
        if not header:
            h = t.find('tr').find('td')
            header = h.text if h else None
        if not header:
            continue
        elif 'level up' in header.lower() or \
             'attacks' in header.lower() or \
             'moves' in header.lower():
            if header not in tables:
                tables[header] = t
            else:
                header = header + '2'
                tables[header] = t
                
    # Skip collapsed table if details table exists
    return tables

def getAtkTableWithinTable(table):
    # get parent of first tr
    parent = table.find('tr').parent
    allRows = parent.find_all('tr', recursive=False)
    splitRow = None
    for r in range(2, len(allRows)):
        tds = allRows[r].find_all('td', recursive=False)
        if len(tds) == 1 and 'transfer only' in tds[0].text.lower():
            splitRow = r
            break

    if not splitRow or splitRow == 0:
        return (allRows, None)
    else:
        topHalf = []
        bottomHalf = []
        for r in range(0, splitRow):
            topHalf.append(allRows[r])

        bottomHalf.append(allRows[splitRow])
        bottomHalf.append(allRows[1])
        for r in range(splitRow+1, len(allRows)):
            bottomHalf.append(allRows[r])
        return (topHalf, bottomHalf)

def getAttackTableColumnData( title, allRows, formNames, dexId ):
    moves = {}
    name = None
    for r in range(2, len(allRows)):
        # even rows are info rows, odd are descriptions
        if r % 2 == 0:
            preevo = False
            infoTds = allRows[r].find_all('td', recursive=False)
            cols = { 'level': None, 'name': None, 'type': None, 'category': None,
                     'bp': None, 'acc': None, 'pp': None, 'effPer': None, 'forms': None }
            # Level Up tables - 8 columns (level, name, type, category, bp, acc, pp, effPer)
            if 'level up' in title.lower() or \
               'technical machine' in title.lower() or \
               'technical record' in title.lower() or \
               ('tm ' in title.lower() and 'attacks' in title.lower()) or \
               'hm attacks' in title.lower():
                if len(infoTds) > 7:
                    cols['level'] = 0
                    cols['name'] = 1
                    cols['type'] = 2
                    cols['category'] = 3
                    cols['bp'] = 4
                    cols['acc'] = 5
                    cols['pp'] = 6
                    cols['effPer'] = 7
                if len(infoTds) > 8:
                    cols['forms'] = 8                    
            # Egg/Move Tutor/Transfer Tables - 7 columns (name, type, cat, bp, acc, pp, effper)
            elif 'move tutor' in title.lower() or \
                 'egg moves' in title.lower() or \
                 'transfer only' in title.lower() or \
                 'usable' in title.lower() or \
                 'pre-evolution only' in title.lower():
                if len(infoTds) > 6:
                    cols['name'] = 0
                    cols['type'] = 1
                    cols['category'] = 2
                    cols['bp'] = 3
                    cols['acc'] = 4
                    cols['pp']  = 5
                    cols['effPer'] = 6
                if len(infoTds) > 7:
                    cols['forms'] = 7
                if 'pre-evolution only' in title.lower():
                    preevo = True

            # Get column data
            if cols['name'] == None:
                continue
            # using next element instead of text ensures that if there are <br> tags they're ignored
            name = infoTds[cols['name']].find('a').next_element.strip()
            # if no text found, try extracting straight text
            if not name:
                name = infoTds[cols['name']].find('a').text.strip()
            moves[name] = {
                'level': infoTds[cols['level']].text if cols['level'] != None else '--',
                'type': infoTds[cols['type']].find('img')['src'].rsplit('/',1)[1].split('.')[0],
                #'category': infoTds[cols['category']].find('img')['src'].rsplit('/',1)[1].split('.')[0],
                'category': '--',
                'bp': infoTds[cols['bp']].text,
                'acc': infoTds[cols['acc']].text,
                'pp': infoTds[cols['pp']].text,
                'effPer': infoTds[cols['effPer']].text
                }
            # check if there are forms specified
            if cols['forms']:
                forms = getFormsForAttack(infoTds, cols['forms'], formNames, dexId)
                # if empty, likely a details row for pokemon without multiforms, add all forms
                # if any pre-evolution only moves, apply to all forms
                if len(forms) == 0 or preevo:
                    forms = formNames
                moves[name]['forms'] = forms
        else:
            if name and name in moves:
                moves[name]['desc'] = allRows[r].find('td').text
                name = None
                
    return moves

def getFormsForAttack( infoTds, formCol, formNames, dexId ):
    # check if there are forms specified
    forms = []
    if len(infoTds) > formCol:
        formImgs = infoTds[formCol].find_all('img')
        # first check src for if base, then check alt/title for other forms
        for img in formImgs:
            srcId = img['src'].rsplit('/',1)[1]
            # check if base, base form always first in formNames
            if srcId == str(dexId) + '.png':
                forms.append(formNames[0])
                # otherwise use alt text or title tags
            elif img.get('alt'):
                alt = img['alt'].strip()
                if alt in formNames:
                    forms.append(img['alt'].strip())
                else:
                    for form in formNames:
                        if (alt.lower().startswith('alolan') and form.lower().startswith('alolan')) or (alt.lower().startswith('galar') and form.lower().startswith('galar')):
                            forms.append(img['alt'].strip())
                            break
            elif img.get('title'):
                title = img['title'].strip()
                if title in formNames:
                    forms.append(img['title'].strip())
                else:
                    for form in formNames:
                        if (title.lower().startswith('alolan') and form.lower().startswith('alolan')) or (title.lower().startswith('galar') and form.lower().startswith('galar')):
                            forms.append(img['title'].strip())
                            break
    return forms

def getPokeAttacks(formNames, dexId):
    tables = getAttackTables()
    attacks = {}
    # Each table has title row, column headers, then attack rows
    for title in tables.keys():
        table = tables[title]
        rowContainer = table.find('tr').parent
        allRows = rowContainer.find_all('tr', recursive=False)    
        moves = getAttackTableColumnData(title, allRows, formNames, dexId)
        attacks[title] = moves

    return attacks

# ==================
#   Insert/Update attacks from the text list
def updateAttacksFromFile():
    atkFile = dataDir + 'attacks.txt'
    with open(atkFile, 'r', encoding='utf-8') as f:
        atkLines = f.read().splitlines()

    # if attack not in DB insert
    for attack in atkLines:
        cur = con.cursor()
        cur.execute(SELECT_ATTACK,[attack.strip()])
        result = cur.fetchone()
        if not result:
            cur.execute(INSERT_ATTACK,[attack.strip()])
            con.commit()
            print('Wrote ' + attack.strip())

#   Some attacks are read without spacing, correct them
def checkDuplicated( atkName ):
    dupes = {
        'ancientpower': 'Ancient Power',
        'bubblebeam': 'Bubble Beam',
        'doubleslap': 'Double Slap',
        'dragonbreath': 'Dragon Breath',
        'dynamicpunch': 'Dynamic Punch',
        'extremespeed': 'Extreme Speed',
        'featherdance': 'Feather Dance',
        'grasswhistle': 'Grass Whistle',
        'poisonpowder': 'Poison Powder',
        'powersplit': 'Power Split',
        'solarbeam': 'Solar Beam',
        'sonicboom': 'Sonic Boom',
        'thunderpunch': 'Thunder Punch',
        'thundershock': 'Thunder Shock',
        'vicegrip': 'Vice Grip'
        }
    if atkName.lower() in dupes:
        return dupes[atkName.lower()]

    return atkName

# ===================
#   Insert/Update AttackByGen objects from the attach html pages
def getAttackByGenData(startFrom, endAt, genStart, genEnd, specificColumns):
    # get the set of all attacks from the database
    cur = con.cursor()
    cur.execute('SELECT * FROM Attack')
    allAttacks = cur.fetchall()
    atkDir = dataDir + 'Attacks/'

    maxAttacks = getMaxAttacks()

    # Loop over each attack, check if it's in the current gen,
    # then parse & update if found
    foundStart = False
    foundEnd = False
    processedAtks = []
    for attack in allAttacks:
        atkId = attack[0]
        atkName = checkDuplicated(attack[1])
        # skip duplicates
        if atkName in processedAtks:
            continue
        if not foundStart and (startFrom and atkName == startFrom) or startFrom == None:
            foundStart = True
        # skip previous entries if starting point specified
        if not foundStart:
            continue
        elif atkName == endAt:
            foundEnd = True

        # skipping gen 3 backwards at the moment
        for gen in reversed(range(genStart,(genEnd+1))):
            genHtml = 'Gen' + str(gen) + '/' + atkName.lower().replace(' ','') + '.html'
            fullpath = atkDir + genHtml
            if path.exists(fullpath):
                # parse for gen
                with open(fullpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    soup = BeautifulSoup(content, 'html.parser')

                isMax = atkName in maxAttacks
                processedAtks.append(writeAtkByGenData(atkId, atkName, soup, gen, isMax, specificColumns))

        if foundEnd:
            break
        
    return processedAtks

def writeAtkByGenData(atkId, atkName, soup, gen, isMax, specificCols):
    atkData = parseAtkForGen4Up(atkName, soup, gen, isMax)
    ## Attributes:
    # atkCategory, atkDesc, atkEffect,
    # bp, acc, pp, effPercent,
    # critRate, target, maxMove, maxPower,
    # priority, breaksProtect, contacting,
    # soundMove, bitingMove, punchMove,
    # copyable, thaws, reflectable,
    # gravityAffected, snatchable,
    # typeId, atkId, genId
    atkCategory = atkData[atkName]['category']
    atkDesc = atkData[atkName]['desc']
    atkEffect = atkData[atkName]['effect']
    bp = str(translateNumStr( atkData[atkName]['bp'] ))
    acc = str(translateNumStr( atkData[atkName]['acc'] ))
    pp = translateNumStr( atkData[atkName]['pp'] )
    effPercent = str(translateNumStr( atkData[atkName]['effPer'] ))
    if not effPercent == '--':
        effPercent = effPercent + ' %'
    critRate = str(translateNumStr( atkData[atkName]['critRate'] ))
    if not critRate == '--':
        critRate = critRate + ' %'
    target = atkData[atkName]['target']
    maxMove = atkData[atkName]['maxMove']
    maxPower = atkData[atkName]['maxPow']
    priority = atkData[atkName]['priority']
    breaksProtect = not atkData[atkName]['protectable']
    contacting = atkData[atkName]['contacts']
    soundMove = atkData[atkName]['sound']
    bitingMove = atkData[atkName]['biting']
    punchMove = atkData[atkName]['punch']
    copyable = atkData[atkName]['copyable']
    thaws = atkData[atkName]['defrosts']
    reflectable = atkData[atkName]['reflectable']
    gravityAffected = atkData[atkName]['gravity']
    snatchable = atkData[atkName]['snatch']
    typ3 = atkData[atkName]['type']

    # get the typeId from the database
    cur = con.cursor()
    cur.execute(SELECT_TYPE_BY_NAME,[typ3])
    atkType = cur.fetchone()
    typeId = atkType[0]

    # with returned json insert the attack forms
    # check whether the attack by gen doesn't exist
    cur.execute(SELECT_ATK_BYGEN,[atkName, gen])
    existing = cur.fetchone()
    if not existing:
        cur.execute(INSERT_ATK_BYGEN, [atkCategory,atkDesc,atkEffect,
                                        bp, acc, pp, effPercent,
                                        critRate, target, maxMove, maxPower,
                                        priority, breaksProtect, contacting,
                                        soundMove, bitingMove, punchMove,
                                        copyable, thaws, reflectable,
                                        gravityAffected, snatchable,
                                        typeId, atkId, gen])
        con.commit()
        print('Inserted ' + atkName + ' in gen ' + str(gen))
    # TODO: change for individual edits
    elif specificCols:
        cur.execute("""UPDATE AttackByGen SET bp=?, acc=?,
                    pp=?, effPercent=?, critRate=?, maxPower=?
                    WHERE atkFormId=?""",
                    [bp, acc, pp, effPercent, critRate, maxPower, existing[0]])
        con.commit()
        print('Updated specific columns for ' + atkName + ' in gen ' + str(gen))
        
    # if the attack exists, update all columns if none specified
    else:
        cur.execute(UPDATE_ATK_BYGEN, [atkCategory,atkDesc,atkEffect,
                                        bp, acc, pp, effPercent,
                                        critRate, target, maxMove, maxPower,
                                        priority, breaksProtect, contacting,
                                        soundMove, bitingMove, punchMove,
                                        copyable, thaws, reflectable,
                                        gravityAffected, snatchable,
                                        typeId, atkId, gen, existing[0]])
        con.commit()
    print('Updated ' + atkName + ' in gen ' + str(gen))

    return atkName

def translateNumStr( val, upperBound ):
    # extract numerical value from input
    m = re.search('[\d.]+', val)
    if not m:
        return '--'
    
    val = m.group(0)
    numval = None
    if '.' in val:
        try:
            numval = float(val)
        except:
            return '--'
    else:
        try:
            numval = int(val)
        except:
            return '--'

    if upperBound and numval >= 0 and numval <= upperBound:
        return numval
    elif numval >= 0 and not upperBound:
        return numval
    else:
        return '--'

def parseAtkForGen4Up( name, soup, gen, isMax ):
    attack = {}
    tableContainer = soup.find('table', class_='dextable').parent
    # get a non-p container
    while tableContainer.name == 'p':
        tableContainer = tableContainer.parent
    atkTables = tableContainer.find_all('table',class_='dextable')
    if len(atkTables) > 1:
        atkInfo = None
        atkAttr = None
        
        atkInfo = atkTables[0]
        infoRows = atkInfo.find_all('tr', recursive=False)
        # gen 4 has no attr table
        if not gen == 4:
            # find attr table
            for table in atkTables:
                td = table.find('td')
                if td and 'Contact' in td.text:
                    attrRows = table.find_all('tr', recursive=False)

        # Gen 8-4 get common formatted info
        attack = getGen8_4SharedInfo( attack, infoRows, soup )

        # Gen 8-5 get common formatted attributes
        if gen > 4:
            attrCols1 = attrRows[1].find_all('td')
            attrCols2 = attrRows[3].find_all('td')
            attack = getGen8765SharedAttrs( attack, attrCols1, attrCols2 )

        allTrs = soup.find_all('tr')
        # Gen specific attributes
        if gen == 8:
            # check if max move defined, status moves don't have it, use max guard
            if not isMax and attack['category'] == 'other':
                attack['maxMove'] = 'Max Guard'
                attack['maxPow'] = '--'
            # find max row, crit row
            for r in range(0, len(allTrs)):
                title = allTrs[r].find('td')
                if title and 'Corresponding' in title.text:
                    maxRowCols = allTrs[r+1].find_all('td')
                    if not isMax:
                        attack['maxMove'] = maxRowCols[0].find('u').text.strip()
                        attack['maxPow'] = maxRowCols[1].text.strip()
                # crit, prio, target
                elif title and 'Hit Rate' in title.text:
                    critRowCols = allTrs[r+1].find_all('td')
                    attack['critRate'] = critRowCols[0].text.strip()
                    attack['priority'] = critRowCols[1].text.strip()
                    attack['target'] = critRowCols[2].text.strip()

            # Gen 8 attributes
            attack['biting'] = truthyFalsy( attrCols1[3].text.strip() )
            attack['snatch'] = truthyFalsy( attrCols1[4].text.strip() )
            attack['gravity'] = truthyFalsy( attrCols2[0].text.strip() )
            attack['defrosts'] = truthyFalsy( attrCols2[1].text.strip() )
            if isMax:
                attack['maxMove'] = '--'
                attack['maxPow'] = '--'
                attack['category'] = '--'
            return { name: attack }
        # Gen 7
        elif gen == 7:
            # find crit, prio, target
            for r in range(0, len(allTrs)):
                title = allTrs[r].find('td')
                if title and 'Hit Rate' in title.text:
                    critRowCols = allTrs[r+1].find_all('td')
                    attack['critRate'] = critRowCols[0].text.strip()
                    attack['priority'] = critRowCols[1].text.strip()
                    attack['target'] = critRowCols[2].text.strip()
                elif title and ('Corresponding' in title.text or title.text.startswith('Z-')):
                    # Z move
                    zRowTitle = title.text.strip()
                    zRowCols = allTrs[r+1].find_all('td')
                    if 'Corresponding' in zRowTitle:
                        attack['maxMove'] = zRowCols[0].find('u').text.strip()
                    else:
                        attack['maxMove'] = zRowTitle
                    # note that might be description if status move
                    attack['maxPow'] = zRowCols[1].text.strip()
            attack['biting'] = False # doesn't exist
            attack['snatch'] = truthyFalsy( attrCols1[3].text.strip() )
            attack['gravity'] = False
            attack['defrosts'] = truthyFalsy( attrCols2[0].text.strip() )
            if isMax:
                attack['maxMove'] = '--'
                attack['maxPow'] = '--'
            return { name: attack }
        # Gen 6 & 5
        elif gen > 4:
            # crit, prio, target
            for r in range(0, len(allTrs)):
                title = allTrs[r].find('b')
                if title and 'TM' in title.text:
                    prioRowCols = allTrs[r+1].find_all('td')
                    attack['critRate'] = '--' # doesn't exist
                    attack['priority'] = prioRowCols[1].text.strip()
                    attack['target'] = prioRowCols[2].text.strip()
            # no max/z move
            attack['maxMove'] = None
            attack['maxPow'] = None
            attack['biting'] = False # doesn't exist
            attack['snatch'] = truthyFalsy( attrCols1[3].text.strip() )
            attack['gravity'] = False
            attack['defrosts'] = truthyFalsy( attrCols2[0].text.strip() )
            return { name: attack }
        # Gen 4
        elif gen == 4:
            # find attrcols
            for r in range(0, len(allTrs)):
                title = allTrs[r].find('td')
                if title and title.find('b') and title.find('b').text.startswith('TM'):
                    attrCols1 = allTrs[r+1].find_all('td')
                    attrCols2 = allTrs[r+3].find_all('td')
                    attack['priority'] = attrCols1[1].text.strip()
                    attack['target'] = attrCols1[2].text.strip()
                    attack['contacts'] = truthyFalsy( attrCols2[2].text.strip() )
            attack['maxMove'] = None
            attack['maxPow'] = None
            attack['critRate'] = '--'
            attack['biting'] = False
            attack['snatch'] = False
            attack['gravity'] = False
            attack['defrosts'] = False
            attack['protectable'] = True
            attack['sound'] = False
            attack['punch'] = False
            attack['copyable'] = False
            attack['reflectable'] = False
            return { name: attack }

def getGen8_4SharedInfo(attack, infoRows, soup):
    # type & category
    typeRowCols = infoRows[1].find_all('td')
    attack['type'] = typeRowCols[1].find('img')['src'].rsplit('/',1)[1].split('.')[0]
    # curse in gen 4 has ??? type for some reason...
    if attack['type'] == 'curse':
        attack['type'] = 'ghost'
    attack['category'] = typeRowCols[2].find('img')['src'].rsplit('/',1)[1].split('.')[0]
    # power attrs
    powRowCols = infoRows[3].find_all('td')
    attack['pp'] = powRowCols[0].text.strip().split()[0]
    attack['bp'] = powRowCols[1].text.strip().split()[0]
    attack['acc'] = powRowCols[2].text.strip().split()[0]
    # desc/eff - check for in-depth effect
    allTrs = soup.find_all('tr')
    for r in range(0, len(allTrs)):
        first = allTrs[r].find('td')
        if first and 'Battle Effect' in first.text:
            attack['desc'] = allTrs[r+1].find('td').text.strip()
        elif first and 'In-Depth' in first.text:
            attack['effect'] = allTrs[r+1].find('p').text.strip()
        elif first and 'Secondary Effect' in first.text:
            effRowCols = allTrs[r+1].find_all('td')
            if not 'effect' in attack:
                attack['effect'] = effRowCols[0].text.strip()
            attack['effPer'] = effRowCols[1].text.strip()

    return attack

def getGen8765SharedAttrs(attack, attrCols1, attrCols2):
    # attributes
    attack['contacts'] = truthyFalsy( attrCols1[0].text.strip() )
    attack['sound'] = truthyFalsy( attrCols1[1].text.strip() )
    attack['punch'] = truthyFalsy( attrCols1[2].text.strip() )
    attack['reflectable'] = truthyFalsy( attrCols2[2].text.strip() )
    attack['protectable'] = truthyFalsy( attrCols2[3].text.strip() )
    attack['copyable'] = truthyFalsy( attrCols2[4].text.strip() )
    
    return attack

def getMaxAttacks():
    nameFile = dataDir + 'Attacks/maxmoves.txt'
    with open(nameFile, 'r', encoding='utf-8') as f:
        maxNames = f.read().splitlines()

    return maxNames

def addMaxMoves(specificColumns):
    maxNames = getMaxAttacks()

    cur = con.cursor()
    for maxmove in maxNames:    
        # add to the attack table if not exists
        cur.execute(SELECT_ATTACK,[maxmove])
        existing = cur.fetchone()
        if not existing:
            cur.execute(INSERT_ATTACK,[maxmove])
            con.commit()
            print('Inserted ' + maxmove)
            cur.execute(SELECT_ATTACK,[maxmove])
            existing = cur.fetchone()

        atkId = existing[0]
        # insert/update the form for gen 7 or 8
        gen = 8 if (maxmove.startswith('Max ') or maxmove.startswith('G-Max ')) else 7

        # get the max html & open for parsing
        maxhtml = dataDir + 'Attacks/Gen' + str(gen) + '/' + maxmove.lower().strip().replace(' ','') + '.html'
        with open(maxhtml, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')

        writeAtkByGenData(atkId, maxmove, soup, gen, True, specificColumns)
        

def truthyFalsy( val ):
    if val == 'Yes':
        return True
    elif val == 'No':
        return False
    else:
        return bool(val)

def updatePokeAtkGenData( movemap, gen, dexId, pokeName, formName ):
    # remap moves from groups to by name
    # movename: {
    #   level up: { move }
    #   egg move: { move }
    mappedmoves = {}
    # loop over movegroup keys
    for movegroup in movemap.keys():
        # get the moves in the group
        movesingroup = movemap[movegroup]
        # loop over the move name keys
        for move in movesingroup.keys():
            # check if the move is applicable to the specified form
            if 'forms' in move and formName in move['forms']:
                # check if move is not already mapped for the form
                if not move in mappedmoves:
                    mappedmoves[move] = {}
                # add the move to the movegroup for the move
                mappedmoves[move][movegroup] = movesingroup[move]
            # if no form specified, apply to all forms
            elif not 'forms' in move:
                # check if move is not already mapped for the form
                if not move in mappedmoves:
                    mappedmoves[move] = {}
                # add the move to the movegroup for the move
                mappedmoves[move][movegroup] = movesingroup[move]

    cur = con.cursor()
    setErrorFlag = False
    
    # get the poke form and map the attacks in the database
    for attack in mappedmoves.keys():
        # Max Guard isn't a stored attack, so skip it
        if 'Max Guard' in attack:
            continue
        
        atkName = checkDuplicated(attack)
        # get the attack from the database
        cur.execute(SELECT_ATTACK,[atkName])
        atk = cur.fetchone()
        if not atk:
            print('Error - failed to find attack ' + atkName)
            setErrorFlag = True
            continue
        
        # get the attack for the gen
        cur.execute(SELECT_ATK_BYGEN,[atk[1], gen])
        atkForm = cur.fetchone()
        if not atkForm:
            print('Error - failed to find attack ' + atkName + ' in gen ' + str(gen))
            setErrorFlag = True
            continue

        pokeForm = None
        if formName == 'Base':
            #  get the poke forms, need to get all to handle non-'Base' base forms
            cur.execute(SELECT_PFORM_BY_DEXID, [dexId])
            pokeForm = cur.fetchone()
        else:
            cur.execute(SELECT_BY_FORM_AND_DEXID, [formName, dexId])
            pokeForm = cur.fetchone()

        if not pokeForm:
            print('Error - failed to find ' + formName + ' for dex id ' + str(dexId))
            setErrorFlag = True
            continue

        # check whether the relationship already exists
        cur.execute(SELECT_MOVESBYGEN,[gen,pokeForm[0],atkForm[0]])
        existing = cur.fetchone()
        if not existing:
            cur.execute(INSERT_MOVESBYGEN,[gen,pokeForm[0],atkForm[0],str(mappedmoves[attack])])
            con.commit()
            print('Inserted ' + atkName + ' to ' + pokeName + ' - ' + formName + ' in ' + str(gen))
            
    return setErrorFlag

#######################
# Scrape Sprites & Icons
def imgDownloader(start, end, genStart, genEnd):
    base_url = 'https://www.serebii.net'
    for dexId in range(start, (end+1)):
        for gen in reversed(range(genStart, (genEnd+1))):
            genHtml = 'Gen' + str(gen) + '/' + str(dexId).zfill(3) + '.html'
            fullpath = dataDir + genHtml
            if not path.exists(fullpath):
                continue
            with open(fullpath, 'r', encoding='utf-8') as f:
                content = f.read()
                soup = BeautifulSoup(content, 'html.parser')

            # get all imgs
            allImgs = soup.find_all('img')
            outRoot = 'G:/Android Development/Database Stuff/PokeRef/PythonDev/sprites/'
            for img in allImgs:
                imgName = img['src'].rsplit('/',1)[1]
                # determine the type of img
                outPath = None
                if '/icon/' in img['src'].lower() and img['src'].lower().endswith('.png'):
                    # icon
                    outPath = outRoot + 'icons/' + imgName
                elif '/pokemon/' in img['src'].lower() and img['src'].lower().endswith('.png'):
                    # sprite
                    outPath = outRoot + 'sprites/' + imgName
                elif '/shiny/' in img['src'].lower() and img['src'].lower().endswith('.png'):
                    # shiny sprite
                    outPath = outRoot + 'sprites_shiny/' + imgName

                # download the data if the file doesn't already exist
                if not outPath or path.exists(outPath):
                    continue
                
                fullurl = base_url + img['src']
                netImg = requests.get(fullurl)
                if netImg.status_code == 200:
                    with open(outPath, 'wb') as f:
                        f.write(netImg.content)
                    print('downloaded ' + img['src'])
                else:
                    print('Failed to download: ' + fullurl)

def moveUnused():
    outRoot = 'G:/Android Development/Database Stuff/PokeRef/PythonDev/sprites/'
    iconDir = outRoot + 'icons/'
    spriteDir = outRoot + 'sprites/'
    shinyDir = outRoot + 'sprites_shiny/'
    iconUnused = outRoot + 'icons_unused/'
    spriteUnused = outRoot + 'sprites_unused/'
    shinyUnused = outRoot + 'sprites_shiny_unused/'

    allIcons = os.listdir(iconDir)
    allSprites = os.listdir(spriteDir)
    allShiny = os.listdir(shinyDir)
    
    cur = con.cursor()
    cur.execute('SELECT DISTINCT pokeId FROM PokemonForm WHERE isBase=0')
    allAlts = cur.fetchall()
    altids = []
    for alt in allAlts:
        altids.append(alt[0])
        
    for dexId in range(1,898):
        # check icons, sprites, & shiny for alts where shouldn't be
        moveNonAlts(dexId, allIcons, altids, iconDir, iconUnused, False)
        moveNonAlts(dexId, allSprites, altids, spriteDir, spriteUnused, True)
        moveNonAlts(dexId, allShiny, altids, shinyDir, shinyUnused, True)
        
def moveNonAlts(dexId, allFiles, altids, curDir, newDir, keepGmax):
    # check icons for alts where shouldn't be
    pokeImgs = []
    for img in allFiles:
        # find the icon for this dexid
        if img.startswith(str(dexId).zfill(3)):
            pokeImgs.append(img)
    # if the dex id has no alts, keep only the non-alt ID
    if not dexId in altids and len(pokeImgs) > 1:
        for img in pokeImgs:
            # if gmax img but not keep gmax, move it
            if img == (str(dexId).zfill(3) + '-gi.png') and not keepGmax:
                fullpath = curDir + img
                newpath = newDir + img
                os.rename(fullpath, newpath)
                print('moved ' + img)
            # if is gmax and keep gmax, skip
            elif img == (str(dexId).zfill(3) + '-gi.png') and keepGmax:
                continue
            # otherwise anything not equal to base is moved
            elif img != (str(dexId).zfill(3) + '.png'):
                fullpath = curDir + img
                newpath = newDir + img
                os.rename(fullpath, newpath)
                print('moved ' + img)

def findSpriteGaps():
    outRoot = 'G:/Android Development/Database Stuff/PokeRef/PythonDev/sprites/'
    iconDir = outRoot + 'icons/'
    spriteDir = outRoot + 'sprites/'
    shinyDir = outRoot + 'sprites_shiny/'
    iconUnused = outRoot + 'icons_unused/'
    spriteUnused = outRoot + 'sprites_unused/'
    shinyUnused = outRoot + 'sprites_shiny_unused/'

    allIcons = os.listdir(iconDir)
    allSprites = os.listdir(spriteDir)
    allShiny = os.listdir(shinyDir)
    allIcUnused = os.listdir(iconUnused)
    allSpUnused = os.listdir(spriteUnused)
    allShUnused = os.listdir(shinyUnused)

    checkOtherFolder(allIcons, allIcUnused)
    checkOtherFolder(allSprites, allSpUnused)
    checkOtherFolder(allShiny, allShUnused)

def checkOtherFolder(allUsed, allUnused):
    for unused in allUnused:
        m = re.search('[\d]+', unused)
        foundId = m.group(0)
        baseImg = foundId + '.png'
        if not baseImg in allUsed:
            print('missing ' + baseImg)

def renameForms():
    outRoot = 'G:/Android Development/Database Stuff/PokeRef/PythonDev/sprites/'
    iconDir = outRoot + 'icons/'
    spriteDir = outRoot + 'sprites/'
    shinyDir = outRoot + 'sprites_shiny/'
    iconUnused = outRoot + 'icons_unused/'
    spriteUnused = outRoot + 'sprites_unused/'
    shinyUnused = outRoot + 'sprites_shiny_unused/'

    allIcons = os.listdir(iconDir)
    allSprites = os.listdir(spriteDir)
    allShiny = os.listdir(shinyDir)

    #renameImgs(iconDir, allIcons, '-m.png', '_mega.png')
    #renameImgs(spriteDir, allSprites, '-m.png', '_mega.png')
    #renameImgs(shinyDir, allShiny, '-m.png', '_mega.png')

    #renameImgs(iconDir, allIcons, '-gi.png', '_gmax.png')
    #renameImgs(spriteDir, allSprites, '-gi.png', '_gmax.png')
    #renameImgs(shinyDir, allShiny, '-gi.png', '_gmax.png')

    addPrefix(iconDir, allIcons, 'ic_')
    addPrefix(spriteDir, allSprites, 'sp_')
    addPrefix(shinyDir, allShiny, 'sh_')

def renameImgs(curDir, allFiles, search, replace):
    for img in allFiles:
        if img.endswith(search):
            newname = img.replace(search,replace)
            os.rename((curDir + img), (curDir + newname))

def addPrefix(curDir, allFiles, prefix):
    for img in allFiles:
        newname = prefix + img
        os.rename((curDir + img), (curDir + newname))

def fixDbTrailing():
    appDb = 'C:/Users/kbuck/AndroidStudioProjects/PokeRef/app/src/main/assets/databases/BattleDex.db'
    con = sqlite3.connect(appDb)
    cur = con.cursor()
    cur.execute('SELECT pokeFormId, shinySprite, pokeId FROM PokemonForm WHERE shinySprite LIKE "%/_.png" ESCAPE "/"')
    brokenSprites = cur.fetchall()

    for sprite in brokenSprites:
        name = sprite[1]
        toks = name.rsplit('_',1)
        fixed = ''.join(toks)
        if fixed == 'sh_' + str(sprite[2]).zfill(3) + '.png':
            cur.execute('UPDATE PokemonForm SET shinySprite=? WHERE pokeFormId=?',[fixed,sprite[0]])
            con.commit()

def fixAlolanForms():
    appDb = 'C:/Users/kbuck/AndroidStudioProjects/PokeRef/app/src/main/assets/databases/BattleDex.db'
    con = sqlite3.connect(appDb)
    cur = con.cursor()
    outRoot = 'G:/Android Development/Database Stuff/PokeRef/PythonDev/sprites/'
    iconDir = outRoot + 'icons/'
    spriteDir = outRoot + 'sprites/'
    shinyDir = outRoot + 'sprites_shiny/'

    fixSuffixes(iconDir, os.listdir(iconDir), cur, 2)
    fixSuffixes(spriteDir, os.listdir(spriteDir), cur, 1)
    fixSuffixes(shinyDir, os.listdir(shinyDir), cur, 3)
    con.close()

def fixSuffixes(curDir, allFiles, cur, resInd):
    for img in allFiles:
        dexId = img.split('_',1)[1].split('_')[0].split('.')[0].split('-')[0]
        cur.execute('SELECT formName, sprite, icon, shinySprite FROM PokemonForm WHERE pokeId=?',[int(dexId)])
        forms = cur.fetchall()
        for form in forms:
            if 'Alolan' in form[0] and img.endswith('-a.png'):
                os.rename((curDir + img), (curDir + form[resInd]))
                break
            elif 'Galarian' in form[0] and img.endswith('-g.png'):
                os.rename((curDir + img), (curDir + form[resInd]))
                break

def mapMissing():
    appDb = 'C:/Users/kbuck/AndroidStudioProjects/PokeRef/app/src/main/assets/databases/BattleDex.db'
    con = sqlite3.connect(appDb)
    cur = con.cursor()
    cur.execute('SELECT formName, sprite, icon, shinySprite FROM PokemonForm')
    forms = cur.fetchall()
    missingFromFiles = []
    extraInDir = []

    outRoot = 'G:/Android Development/Database Stuff/PokeRef/PythonDev/sprites/'
    iconDir = outRoot + 'icons/'
    spriteDir = outRoot + 'sprites/'
    shinyDir = outRoot + 'sprites_shiny/'
    allIcons = os.listdir(iconDir)
    allSprites = os.listdir(spriteDir)
    allShiny = os.listdir(shinyDir)

    allDbIcons = []
    allDbSprites = []
    allDbShiny = []

    # Check whether the DB records exist
    for form in forms:
        if not path.exists(iconDir + form[2]):
            missingFromFiles.append(form[2])
        if not path.exists(spriteDir + form[1]):
            missingFromFiles.append(form[1])
        if not path.exists(shinyDir + form[3]):
            missingFromFiles.append(form[3])

        allDbIcons.append(form[2])
        allDbSprites.append(form[1])
        allDbShiny.append(form[3])
        
    # Gather list of extra sprites
    for icon in allIcons:
        if not icon in allDbIcons:
            extraInDir.append(icon)
    for sprite in allSprites:
        if not sprite in allDbSprites:
            extraInDir.append(sprite)
    for shiny in allShiny:
        if not shiny in allDbShiny:
            extraInDir.append(shiny)

    print('missing files: ')
    print(missingFromFiles)
    print('extra files: ')
    print(extraInDir)

def findBrokenBp():
    appDb = 'C:/Users/kbuck/AndroidStudioProjects/PokeRef/app/src/main/assets/databases/BattleDex.db'
    con = sqlite3.connect(appDb)
    cur = con.cursor()
    cur.execute('SELECT atkName, atkFormId, bp FROM AttackByGen AS G, Attack AS A WHERE (atkCategory="physical" OR atkCategory="special") AND (bp="--" OR bp="0") AND G.atkId=A.atkId')
    results = cur.fetchall()
    print('\nResults:\n')
    print(results)
    
#############
# Test runner
def iteratePokeAtkGen(start, end, startGen, endGen, write):
    attackFile = dataDir + 'attacks.txt'
    writtenAttacks = []
    # check existing written attacks on re-runs
    if path.exists(attackFile):
        with open(attackFile, 'r', encoding='utf-8') as f:
            writtenAttacks = f.read().splitlines()
    # remove dupes
    allAttacks = set([checkDuplicated(atkName) for atkName in writtenAttacks])

    # Cycle pokemon (attacks loaded for gen 4 up at the moment)
    for gen in reversed(range(startGen,(endGen+1))):
        genDir = dataDir + 'Gen' + str(gen) +'/'
        htmls = os.listdir(genDir)
        for html in htmls:
            # skip any non html file
            if not html.rsplit('.',1)[1] == 'html':
                continue
            else:
                dexId = int(html.rsplit('.',1)[0])
                if start <= dexId and dexId <= end:
                    genHtml = 'Gen' + str(gen) +'/' + html
                    print('\nprocessing ' + genHtml)
                    pokeName = initTests(genHtml)
                    formNames = getFormNames(pokeName, statTables, megaTables)
                    attackGroups = getPokeAttacks(formNames,dexId)
                    mappedattacks = {}
                    for form in formNames:
                        errorFlag = updatePokeAtkGenData(attackGroups, gen, dexId, pokeName, form)    
                        # terminate on error to allow it to be fixed
                        if errorFlag:
                            return writtenAttacks
                        
                    # add the returned attacks to the list of attacks and to the database
                    for group in attackGroups.keys():
                        attacks = attackGroups[group].keys()
                        for attack in attacks:
                            if attack not in writtenAttacks:
                                writtenAttacks.append(attack)
                                
            # write to the attacks file at the end of each pokemon
            if write:
                with open(attackFile, 'w', encoding='utf-8') as f:
                    for attack in writtenAttacks:
                        f.write(attack+'\n')

    return writtenAttacks

def initItemIteration():
    itemFile = dataDir + 'items.txt'
    with open(itemFile, 'r', encoding='utf-8') as f:
        itemlist = f.readlines()
	
    items = {}
    for itemline in itemlist:
        toks = itemline.split('">')
        itemurl = toks[0].replace('.shtml','.html')
        itemname = toks[1].split('</option>')[0]
        items[itemurl] = itemname
    
    itemDir = dataDir + 'Items/'
    if not path.exists(itemDir):
        print('Item directory not found: ' + itemDir)

    htmls = os.listdir(itemDir)
    for html in htmls:
        # skip any non-html file
        if not html.rsplit('.',1)[1] == 'html':
            continue
        fullpath = itemDir + html
        with open(fullpath,'r',encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')

        updateItem(items[html], soup, True)

def initAbIteration(single):
    abDir = dataDir + 'Abilities/'
    if not path.exists(abDir):
        print('Ability directory not found: ' + abDir)

    if not single:
        htmls = os.listdir(abDir)
    else:
        htmls = [abDir + single + '.html']
    for html in htmls:
        # skip any non html file
        if not html.rsplit('.',1)[1] == 'html':
            continue
        fullpath = abDir + html
        with open(fullpath, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')

        updateAbility(soup)

def initPokeIteration(start, end, writeAbilities):
    formMap = {}
    for dexId in range(start, (end+1)):
        cur = con.cursor()
        cur.execute(SELECT_POKE_BY_NATID, [dexId])
        result = cur.fetchone()
        if result:
            formMap[result[2]] = importAllForms(dexId)
            # write after processing each
            if writeAbilities:
                abilityFile = dataDir + 'abilities.txt'
                if path.exists(abilityFile):
                    with open(abilityFile, 'r', encoding='utf-8') as f:
                        abilities = f.readlines()
                    for ability in abilities:
                        if not ability.strip() in allAbilities:
                            allAbilities.append(ability.strip())

                with open(abilityFile, 'w', encoding='utf-8') as f:
                    for ability in allAbilities:
                        f.write(ability+'\n')
        
    return formMap

def importAllForms(dexId):
    forms = []
    for gen in reversed(range(1,9)):
        html = dataDir + 'Gen' + str(gen) + '/' + str(dexId).zfill(3) + '.html'
        if not path.exists(html):
            continue
        print('Processing: ' + 'Gen' + str(gen) + '/' + str(dexId).zfill(3) + '.html')
        with open(html, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
        pokeName = getPokeName(soup, dexId)
        allTables.clear()
        statTables.clear()
        megaTables.clear()
        allTables.extend(getAllTables(soup))
        statTables.extend(getStatTables(allTables))
        megaTables.extend(getMegaTables(pokeName, allTables))
        updatePokemonForm(pokeName, forms, dexId, gen)
    return forms

def initTests( genHtml ):
    html = dataDir + genHtml
    dexId = int(genHtml.split('/')[1].split('.')[0])
    with open(html,'r',encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
    pokeName = getPokeName(soup, dexId)
    allTables.clear()
    statTables.clear()
    megaTables.clear()
    allTables.extend(getAllTables(soup))
    statTables.extend(getStatTables(allTables))
    megaTables.extend(getMegaTables(pokeName, allTables))
    return pokeName

def correctEvsEarned(dexId):
    cur = con.cursor()
    cur.execute('SELECT pokeFormId, formName, pokeId, evsEarned FROM PokemonForm')
    nulls = cur.fetchall()
    # find the most recent form
    dataDir = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/DexPages/'
    for nil in nulls:
        if dexId and dexId != nil[2]:
            continue
        #skip single ev records
        if not ',' in nil[3]:
            continue
        updated = False
        for gen in reversed(range(1,9)):
            genHtml = 'Gen' + str(gen) + '/' + str(nil[2]).zfill(3) + '.html'
            html = dataDir + genHtml
            if path.exists(html):
                initTests(genHtml)
                evsEarned = getEVsEarned(nil[1], allTables)
                if evsEarned:
                    cur.execute('UPDATE PokemonForm SET evsEarned=? WHERE pokeFormId=?',[evsEarned,nil[0]])
                    con.commit()
                    updated = True
                    print('updated evsEarned for ' + str(nil[0]) + ' - ' + nil[1])
                    break

        if not updated:
            print('no evs found for ' + str(nil[0]) + ' - ' + nil[1])            

def findMoveDataFromHtml(startGen, endGen, start, end):
    # Cycle pokemon (attacks loaded for gen 4 up at the moment)
    for gen in reversed(range(startGen,(endGen+1))):
        genDir = dataDir + 'Gen' + str(gen) +'/'
        htmls = os.listdir(genDir)
        for html in htmls:
            # skip any non html file
            if not html.rsplit('.',1)[1] == 'html':
                continue
            else:
                dexId = int(html.rsplit('.',1)[0])
                if start <= dexId and dexId <= end:
                    genHtml = 'Gen' + str(gen) +'/' + html
                    print('\nprocessing ' + genHtml)
                    pokeName = initTests(genHtml)
                    formNames = getFormNames(pokeName, statTables, megaTables)
                    attackGroups = getPokeAttacks(formNames,dexId)
                    mappedattacks = {}
                    for form in formNames:
                        errorFlag = updatePokeAtkGenData(attackGroups, gen, dexId, pokeName, form)    
                        # terminate on error to allow it to be fixed
                        if errorFlag:
                            return

def correctMissingGenMoves(startGen, endGen):
    cur = con.cursor()
    valid_dir = 'G:/Android Development/Database Stuff/PokeRef/PythonDev/pokedata/DexValidate/Attacks/'
    remaining = {}
    for gen in reversed(range(startGen, endGen+1)):
        missingFile = valid_dir + 'Gen' + str(gen) + 'Missing.txt'
        with open(missingFile, 'r', encoding='utf-8') as jsonFile:
            jData = json.load(jsonFile)

        # get the mon & list of missing attacks from the json
        for mon in jData:
            atks = jData[mon]

            # get the nat id from the database
            cur.execute("SELECT nat_id FROM Pokemon WHERE name=?", [mon])
            nat_id = cur.fetchone()[0]

            # update/insert the attacks for this mon
            updatedAttacks = iteratePokeAtkGen(nat_id, nat_id, gen, gen, False)


            # validate that none of the attacks are still missing
            stillMissing = []
            for atk in atks:
                if atk not in updatedAttacks:
                    stillMissing.append(atk)

            if len(stillMissing) > 0:
                remaining[mon] = stillMissing

    return remaining
            
def fixAltFormMoveDuplication():
    # get all mons with alt forms
    cur = con.cursor()
    cur.execute("SELECT nat_id from Pokemon")
    allNatIds = cur.fetchall()
    multiforms = {}
    for natId in allNatIds:
        cur.execute("SELECT * FROM PokemonForm WHERE pokeId=?", [natId[0]])
        forms = cur.fetchall()
        multiforms[natId]=[]
        if len(forms) > 1:
            for form in forms:
                multiforms[natId].append(form)

    # for each of the multiform form IDs, get all of their attacks and check whether the level-up text makes sense
    # also check forms for TM/TR, max moves, move tutors
    invalidMoves = []
    unableToCheck = []
    for key in multiforms:
        allForms = multiforms[key]
        for form in allForms:
            otherForms = []
            for f in allForms:
                if f[0] != form[0]:
                    otherForms.append(f[1])
            cur.execute("SELECT * FROM PokeMovesByGen WHERE pokeFormId=?", [form[0]])
            allMoves = cur.fetchall()
            for move in allMoves:
                desc = move[3]
                desc = fixJsonString(desc)
                j = json.loads(desc)
                # ways to be valid:
                # 'standard level up',
                # 'level up' without other form name,
                # other key has forms attribute containing form
                # if any valid case found, quit searching
                levelUpKeys = []
                otherKeys = []
                tempInvalid = []
                for key in j:
                    if 'level up' in key.lower():
                        levelUpKeys.append(key)
                    else:
                        otherKeys.append(key)

                # check each level up key to see whether it contains the form name of an alt form
                keyCounter = 0
                for levelKey in levelUpKeys:
                    for other in otherForms:
                        if other.lower() in levelKey.lower():
                            keyCounter += 1
                            break
                # if the total alt form counter equals the number of level up keys, means this form is not valid level up
                if len(levelUpKeys) > 0 and keyCounter == len(levelUpKeys):
                    print('form ' + form[1] + ' not in level up for ' + str((move[0],move[1],move[2])))
                    tempInvalid.append((move[0],move[1],move[2]))
                # if valid level up move, then continue to next move
                elif len(levelUpKeys) > 0:
                    continue

                valid = False
                for key in otherKeys:
                    # if searching a 'level up' key, look for other form in key name
                    print('on form ' + str(form[0]) + ' atk: ' + str(move[2]))
                    # check for form name in forms attribute
                    if 'forms' in j[key] and not form[1] in j[key]['forms']:
                        remapped = ['Normal', 'Plant Cloak', 'Land Forme', 'Aria Forme', 'Hoopa Confined', 'Baile Style', 'Hero of Many Battles', 'Single Strike Style']
                        if form[1] in remapped and 'Base' not in j[key]['forms']:
                            print('form ' + form[1] + ' not in forms for ' + str((move[0],move[1],move[2])))
                            tempInvalid.append((move[0],move[1],move[2]))
                        elif form[1] not in remapped:
                            print('form ' + form[1] + ' not in forms for ' + str((move[0],move[1],move[2])))
                            tempInvalid.append((move[0],move[1],move[2]))
                        else:
                            valid = True
                    elif 'forms' in j[key]:
                        valid = True
                    elif 'forms' not in j[key]:
                        unableToCheck.append((move[0],move[1],move[2]))

                if valid:
                    tempInvalid = []

                if len(tempInvalid) > 0:
                    invalidMoves.extend(tempInvalid)

    print('invalid: ')
    print(invalidMoves)
    print('unable: ')
    print(unableToCheck)

def fixJsonString(string):
    openQuotes = False
    newString = ''
    for char in string:
        if char == '"':
            openQuotes = not openQuotes
        elif not openQuotes and char == '\'':
            char = '"'

        newString += char
        
    return newString

def deleteDuplicatedMoves():
    cur = con.cursor()
    dupFile = 'G:/Android Development/Database Stuff/PokeRef/PythonDev/pokedata/DexValidate/Attacks/duplicateAltFormMoves.txt'
    with open(dupFile, 'r', encoding='utf-8') as f:
        moves = f.readlines()
	
    stripped = []
    for move in moves:
        toks = move.split(",")
        gen = toks[0].split("(")[1].strip()
        poke = toks[1].strip()
        atk = toks[2].split(")")[0].strip()
        stripped.append((gen, poke, atk))

    for move in stripped:
        cur.execute("""select atkName, name, formName from Attack as A, Pokemon as P, PokemonForm as F
                        where F.pokeId = P.nat_id 
                        and atkId IN (SELECT atkId FROM AttackByGen AS G WHERE G.atkFormId=? AND atkFormId IN (
                        SELECT atkFormId FROM PokeMovesByGen WHERE genId=? AND pokeFormId = F.pokeFormId))
                        AND F.pokeFormId=?""", [move[2], move[0], move[1]])
        print('move to delete: ' + str(cur.fetchone()))
        #cur.execute("DELETE FROM PokeMovesByGen WHERE genId=? AND pokeFormId=? AND atkFormId=?",[move[0], move[1], move[2]])

def reinsertAllMoves(genId, dexId, moveMap):
    cur = con.cursor()
    missingMoves = []
    # loop over the forms in the move map, querying the DB for the pokeFormId
    for form in moveMap:
        pokeFormId = None
        if form == 'Base':
            cur.execute("SELECT pokeFormId FROM PokemonForm WHERE isBase=1 AND pokeId=?", [dexId])
            pokeFormId = cur.fetchone()[0]
        else:
            cur.execute("SELECT pokeFormId FROM PokemonForm WHERE formName=? AND pokeId=?", [form, dexId])
            pokeFormId = cur.fetchone()[0]

        if not pokeFormId:
            print("failed to find PokemonForm for form: " + form)
            continue

        # for each attack in the movemap, get the atkFormId based on the name and gen
        formMoves = moveMap[form]
        for move in formMoves:
            capitalized = capitalizeWords(move)
            capitalized = checkDuplicated(capitalized)
            if capitalized == 'Max Guard':
                continue
            cur.execute("SELECT atkFormId FROM AttackByGen WHERE genId=? AND atkId=(SELECT atkId FROM Attack WHERE atkName=?)",[genId, capitalized])
            atk = cur.fetchone()
            if not atk:
                print('No move ' + capitalized + ' found in gen ' + str(genId) + ' for ' + str(dexId).zfill(3))
                missingMoves.append(capitalized)
                continue 
            atkFormId = atk[0]

            moveCategories = formMoves[move]
            consolidated = []
            for category in moveCategories:
                if 'level up' in category.lower() and 'Level Up' not in consolidated:
                    consolidated.append('Level Up')
                elif 'technical machine' in category.lower() or 'technical record' in category.lower() or \
                    ('tm ' in category.lower() and 'attacks' in category.lower()) or 'hm attacks' in category.lower():
                    if not 'TM/TR/HM' in consolidated:
                        consolidated.append('TM/TR/HM')
                elif 'move tutor' in category.lower() and 'Tutor Moves' not in consolidated:
                    consolidated.append('Tutor Moves')
                elif 'egg move' in category.lower() and 'Egg Moves' not in consolidated:
                    consolidated.append('Egg Moves')
                elif 'transfer only' in category.lower() and 'Transfer Only' not in consolidated:
                    consolidated.append('Transfer Only')
                elif 'useable' in category.lower() and category not in consolidated:
                    consolidated.append(category)
                elif 'pre-evolution only' in category.lower() and 'Pre-Evolution' not in consolidated:
                    consolidated.append('Pre-Evolution')
            catStr = ''
            for index in range(0, len(consolidated)):
                catStr += consolidated[index]
                if index < (len(consolidated) - 2):
                    catStr += ', '
            # check whether the move already exists:
            cur.execute("SELECT * FROM PokeMovesByGen WHERE genId=? AND pokeFormId=? AND atkFormId=?", [genId, pokeFormId, atkFormId])
            result = cur.fetchone()
            if not result:
                # insert the move for this form in this gen, adding categories to the gen info
                cur.execute("INSERT INTO PokeMovesByGen(genId, pokeFormId, atkFormId, groupDesc) VALUES(?,?,?,?)",[genId, pokeFormId, atkFormId, catStr]) 
                con.commit()
                print("Inserted moves for " + str(dexId).zfill(3) + " - " + form + " in gen " + str(genId))
##            else:
##                print("move already exists for " + str(dexId).zfill(3) + " - " + form + " in gen " + str(genId))

    return missingMoves

def getMovesFromRows(allRows, title, formNames, dexId):
    allMoves = {}
    titleForm = None
    for form in formNames:
        if form.lower() in title.lower():
            titleForm = form
        elif form.lower().startswith('alola') or form.lower().startswith('galar'):
            if 'alola' in title.lower() or 'galar' in title.lower():
                titleForm = form

    moves = getAttackTableColumnData(title, allRows, formNames, dexId)
    
    # if the form found in the table title, add the found moves to the mapped form
    if titleForm:
        if not titleForm in allMoves:
            allMoves[titleForm] = {}
            allMoves[titleForm][title] = {}
        elif title not in allMoves[titleForm]:
            allMoves[titleForm][title] = {}

        for move in moves:
            allMoves[titleForm][title][move] = moves[move]

    # if form not in the title name, try to get it from the moves result
    else:
        for move in moves:
            if 'forms' in moves[move]:
                forms = moves[move]['forms']
                for form in forms:
                    formName = checkBaseTranslation(form, formNames)
                    if not formName in allMoves:
                        allMoves[formName] = {}
                        allMoves[formName][title] = {}
                    elif title not in allMoves[formName]:
                        allMoves[formName][title] = {}
                    allMoves[formName][title][move] = moves[move]
            # if not titleForm && not 'forms' defined, then is standard level up
            else:
                if not 'Base' in allMoves:
                    allMoves['Base'] = {}
                    allMoves['Base'][title] = {}
                elif title not in allMoves['Base']:
                    allMoves['Base'][title] = {}
                allMoves['Base'][title][move] = moves[move]

    allMoves = remapMovesByName(allMoves)
    return allMoves
    #missing = reinsertAllMoves(gen, dexId, allMoves)
    #if len(missing) > 0:
    #    missingMoves[dexId] = missing

def remapPokeMovesByGen(startGen, endGen, start, end):
    cur = con.cursor()
    missingMoves = {}
    for gen in reversed(range(startGen, endGen+1)):
        genDir = dataDir + 'Gen' + str(gen) + '/'
        if not start:
            start = 1
        if not end:
            end = 898

        for dexId in range(start, end+1):
            allTables.clear()
            html = genDir + str(dexId).zfill(3) + '.html'
            
            if path.exists(html):
                print('reading html: ' + html)
                with open(html, 'r', encoding='utf-8') as f:
                    content = f.read()
                    soup = BeautifulSoup(content, 'html.parser')

                allTables.extend(getAllTables(soup))
                print('allTables: ' + str(len(allTables)))
                # map keyed on the table header title
                atkTables = getAttackTables()
                print('atkTables: ' + str(atkTables.keys()))

                # check if there is a forms column
                cur.execute("SELECT formName FROM PokemonForm WHERE pokeId=? AND pokeFormId IN (SELECT pokeFormId FROM PokemonInDex WHERE genId=?)", [dexId, gen])
                result = cur.fetchall()
                formNames = []
                for form in result:
                    formNames.append(form[0])

                # loop over each of the attack tables
                allMoves = {}
                for table in atkTables:
                    tables = getAtkTableWithinTable(atkTables[table])
                    topRows = tables[0]
                    if not topRows or len(topRows) < 1:
                        continue
                    h = topRows[0].find('h3')
                    topTitle = h.text if h else None
                    if not topTitle:
                        h = topRows[0].find('td')
                        topTitle = h.text if h else None
                    if not topTitle:
                        continue

                    topMoves = getMovesFromRows(topRows, topTitle, formNames, dexId)
                    missing = reinsertAllMoves(gen, dexId, topMoves)
                    if len(missing) > 0:
                        missingMoves[dexId] = missing
                    
                    botRows = None
                    botMoves = None
                    if tables[1]:
                        botRows = tables[1]
                        h = botRows[0].find('h3')
                        botTitle = h.text if h else None
                        if not botTitle:
                            h = botRows[0].find('td')
                            botTitle = h.text if h else None
                        if not botTitle:
                            continue

                        botMoves = getMovesFromRows(botRows, botTitle, formNames, dexId)
                        missing = reinsertAllMoves(gen, dexId, botMoves)
                        if len(missing) > 0:
                            missingMoves[dexId] = missing
                    
##                    titleForm = None
##                    for form in formNames:
##                        if form.lower() in title.lower():
##                            titleForm = form
##                        elif form.lower().startswith('alola') or form.lower().startswith('galar'):
##                            if 'alola' in title.lower() or 'galar' in title.lower():
##                                titleForm = form
##
##                    moves = getAttackTableColumnData(title, allRows, formNames, dexId)
##                    
##                    # if the form found in the table title, add the found moves to the mapped form
##                    if titleForm:
##                        if not titleForm in allMoves:
##                            allMoves[titleForm] = {}
##                            allMoves[titleForm][title] = {}
##                        elif title not in allMoves[titleForm]:
##                            allMoves[titleForm][title] = {}
##
##                        for move in moves:
##                            allMoves[titleForm][title][move] = moves[move]
##
##                    # if form not in the title name, try to get it from the moves result
##                    else:
##                        for move in moves:
##                            if 'forms' in moves[move]:
##                                forms = moves[move]['forms']
##                                for form in forms:
##                                    formName = checkBaseTranslation(form, formNames)
##                                    if not formName in allMoves:
##                                        allMoves[formName] = {}
##                                        allMoves[formName][title] = {}
##                                    elif title not in allMoves[formName]:
##                                        allMoves[formName][title] = {}
##                                    allMoves[formName][title][move] = moves[move]
##                            # if not titleForm && not 'forms' defined, then is standard level up
##                            else:
##                                if not 'Base' in allMoves:
##                                    allMoves['Base'] = {}
##                                    allMoves['Base'][title] = {}
##                                elif title not in allMoves['Base']:
##                                    allMoves['Base'][title] = {}
##                                allMoves['Base'][title][move] = moves[move]
##
##                allMoves = remapMovesByName(allMoves)
##                return allMoves
##                #missing = reinsertAllMoves(gen, dexId, allMoves)
##                #if len(missing) > 0:
##                #    missingMoves[dexId] = missing
    return missingMoves

def capitalizeWords(atkName):
    flag = False
    capitalized = ''
    for char in atkName:
        if char == ' ' or char == '-':
            flag = True
            capitalized += char
            continue
        if flag:
            capitalized += char.upper()
            flag = False
        else:
            capitalized += char
    return capitalized
                    
def checkBaseTranslation(formName, allForms):
    remapped = ['Normal', 'Plant Cloak', 'Land Forme', 'Aria Forme', 'Hoopa Confined', 'Baile Style', 'Hero of Many Battles', 'Single Strike Style']
    if formName in remapped:
        return 'Base'
    else:
        if formName.lower().startswith('alola') or formName.lower().startswith('galar'):
            for form in allForms:
                if form.lower().startswith('alola') or form.lower().startswith('galar'):
                    return form

    return formName

def remapMovesByName(allMoves):
    formMoves = {}
    for form in allMoves:
        moveCategories = allMoves[form]
        moves = {}
        for category in moveCategories:
            catMoves = moveCategories[category]
            for move in catMoves:
                if not move in moves:
                    moves[move] = []
                moves[move].append(category)
        formMoves[form] = moves
    return formMoves

def fixBlankGroupDesc():
    cur = con.cursor()
    cur.execute("SELECT * FROM PokeMovesByGen WHERE groupDesc=''")
    moves = cur.fetchall()
    for move in moves:
        gen = move[0]
        pokeFormId = move[1]
        atkFormId = move[2]

        cur.execute("SELECT atkName FROM Attack WHERE atkId=(SELECT atkId FROM AttackByGen WHERE atkFormId=?)",[atkFormId])
        name = cur.fetchone()
        if name[0].startswith('Max') or name[0].startswith('G-Max'):
            cur.execute("UPDATE PokeMovesByGen SET groupDesc='Usable Max' WHERE genId=? AND pokeFormId=? AND atkFormId=?", [gen, pokeFormId, atkFormId])
            con.commit()
            print('updated ' + str(move))
        else:
            zmoves = ['10,000,000 Volt Thunderbolt', 'Acid Downpour', 'All-Out Pummeling', 'Black Hole Eclipse', 'Bloom Doom', 'Breakneck Blitz', 'Catastropika', 'Clangorous Soulblaze', 'Continental Crush', 'Corkscrew Crash', 'Devastating Drake', 'Extreme Evoboost', 'Genesis Supernova', 'Gigavolt Havoc', 'Guardian Of Alola', 'Hydro Vortex', 'Inferno Overdrive', "Let's Snuggle Forever", 'Light That Burns The Sky', 'Malicious Moonsault', 'Menacing Moonraze Maelstrom', 'Never-Ending Nightmare', 'Oceanic Operetta', 'Pulverizing Pancake', 'Savage Spin-Out', 'Searing Sunraze Smash', 'Shattered Psyche', 'Sinister Arrow Raid', 'Soul-Stealing 7-Star Strike', 'Splintered Stormshards', 'Stoked Sparksurfer', 'Subzero Slammer', 'Supersonic Skystrike', 'Tectonic Rage', 'Twinkle Tackle']
            if name[0] in zmoves:
                cur.execute("UPDATE PokeMovesByGen SET groupDesc='Usable Max' WHERE genId=? AND pokeFormId=? AND atkFormId=?", [gen, pokeFormId, atkFormId])
                con.commit()
                print('updated ' + str(move))

def checkItemIcons():
    mapped = mapItemIcons()

    spriteDir = 'G:/Android Development/Database Stuff/PokeRef/PythonDev/sprites/items/'
    allImgs = os.listdir(spriteDir)

    dbExtras = []
    fileExtras= []
    for key in mapped:
        if key not in allImgs:
            dbExtras.append(key)

    for img in allImgs:
        if img not in mapped.keys():
            fileExtras.append(img)

    print('DB Extras: ')
    print(dbExtras)
    print('FileExtras: ')
    print(fileExtras)

def renameItemIcons():
    mapped = mapItemIcons()
    spriteDir = 'G:/Android Development/Database Stuff/PokeRef/PythonDev/sprites/items/'
    allImgs = os.listdir(spriteDir)

    for img in allImgs:
        if img in mapped.keys():
            origFull = spriteDir + img
            newFull = spriteDir + mapped[img]
            if path.exists(origFull):
                os.rename(origFull, newFull)

def mapItemIcons():
    # get all the item names from the database
    cur = con.cursor()
    cur.execute("SELECT itemIcon FROM Item")
    allItems = cur.fetchall()

    mapped = {}
    for item in allItems:
        toks = item[0].split("_")
        urlname = ''
        for r in range(1, len(toks)):
            urlname += toks[r].lower()

        mapped[urlname] = item[0]

    return mapped
