import re
import requests
import sqlite3
import os.path
from os import path
from bs4 import BeautifulSoup

# Downloaded HTML Directory & DB Path (check mac then windows)
dataDir = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/DexPages/'
if not path.exists(dataDir):
    dataDir = 'G:\\Android Development\\Database Stuff\\PokeRef\\PythonDev\\pokedata\\DexPages\\'

dbPath = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/PokeRefDbNew.db'
if not path.exists(dbPath):
    dbPath = 'G:\\Android Development\\Database Stuff\\PokeRef\\PythonDev\\pokedata\\PokeRefDbNew.db'

# =================
# TABLE: Ability
INSERT_ABILITY = 'INSERT INTO Ability(abName,abDesc,abDetails) VALUES (?,?,?)'
UPDATE_ABILITY = 'UPDATE Ability SET abName=?, abDesc=?, abDetails=? WHERE abId=?'
SELECT_AB_BY_NAME = 'SELECT * FROM Ability WHERE abName=? COLLATE NOCASE'
# =================
# TABLE: Attack
INSERT_ATTACK = 'INSERT INTO Attack(atkName) VALUES (?)'
UPDATE_ATTACK = 'UPDATE Attack SET atkName=? WHERE atkId=?'
# =================
# TABLE: AttackForm
INSERT_ATK_FORM = """INSERT INTO AttackForm(
                        atkCategory,atkDesc,
                        atkEffect,bp,acc,pp,effPercent,
                        critRate,target,maxMove,maxPower,
                        priority,breaksProtect,contacting,
                        soundMove,bitingMove,punchMove,
                        copyable,thaws,reflectable,
                        gravityAffected,snatchable,
                        typeId,atkId) 
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
UPDATE_ATK_FORM = """UPDATE AttackForm SET atkCategory=?, atkDesc=?,
                        atkEffect=?,bp=?,acc=?,pp=?,effPercent=?,
                        critRate=?,target=?,maxMove=?,maxPower=?,
                        priority=?,breaksProtect=?,contacting=?,
                        soundMove=?,bitingMove=?,punchMove=?,
                        copyable=?,thaws=?,reflectable=?,
                        gravityAffected=?,snatchable=?,
                        typeId=?,atkId=? 
                    WHERE atkFormId=?"""
# =================
# TABLE: AttacksInDex
INSERT_ATKSINDEX = 'INSERT INTO AttacksInDex(genId,atkFormId) VALUES (?,?)'
DELETE_ATKSINDEX = 'DELETE FROM AttacksInDex WHERE genId=? AND atkFormId=?'
# =================
# TABLE: Item
INSERT_ITEM = 'INSERT INTO Item(itemName,itemEffect,itemIcon) VALUES (?,?,?)'
UPDATE_ITEM = 'UPDATE Item SET itemName=?, itemEffect=?, itemIcon=? WHERE itemId=?'
# =================
# TABLE: ItemsInDex
INSERT_ITEMSINDEX = 'INSERT INTO ItemsInDex(genId,itemId) VALUES (?,?)'
DELETE_ITEMSINDEX = 'DELETE FROM ItemsInDex WHERE genId=? AND itemId=?'
# =================
# TABLE: PokeMovesByGen
INSERT_MOVESBYGEN = 'INSERT INTO PokeMovesByGen(genId,pokeFormId,atkFormId) VALUES (?,?,?)'
DELETE_MOVESBYGEN = 'DELETE FROM PokeMovesByGen WHERE genId=? AND pokeFormId=? AND atkFormId=?'
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
INSERT_POKE_FORM = """INSERT INTO PokemonForm(formName,gender,
                        sprite,icon,shinySprite,
                        height,weight,baseHp,baseAtk,baseDef,
                        baseSpatk,baseSpdef,baseSpeed,can_dmax,
                        has_gmax,legendary,sub_legend,mythic,
                        type1,type2,ability1,ability2,abilityH,pokeId) 
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
UPDATE_POKE_FORM = """UPDATE PokemonForm SET formName=?, gender=?,
                        sprite=?,icon=?,shinySprite=?,
                        height=?,weight=?,baseHp=?,baseAtk=?,baseDef=?.
                        baseSpatk=?,baseSpdef=?,baseSpeed=?,can_dmax=?,
                        has_gmax=?,legendary=?,sub_legend=?,mythic=?,
                        type1=?,type2=?,ability1=?,ability2=?,abilityH=?,pokeId=?
                    WHERE pokeFormId=?"""
SELECT_PFORM_BY_DEX_FORM = """SELECT * FROM PokemonForm
                            WHERE formName=?
                            AND pokeId=
                            (SELECT pokeId FROM Pokemon WHERE nat_id=?)"""
# =================
# TABLE: PokemonInDex
INSERT_POKEINDEX = 'INSERT INTO PokemonInDex(genId,pokeFormId) VALUES (?,?)'
DELETE_POKEINDEX = 'DELETE FROM PokemonInDex WHERE genId=? AND pokeFormId=?'
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

# ==============================
# Process the HTML files to insert/update the DB
def processHtmls():
    legTables = getLegendTables()
    
    # Loop over each generation, looking for pokemon instances if they exist
    for gen in range(1,9):
        genDir = dataDir + 'Gen' + str(gen) + '/'
        print('Processing Gen' + str(gen))

        # Loop over the max pokedex values, looking for html files
        for natId in range(1, 899):
            pokeHtml = genDir + str(natId).zfill(3) + '.html'

            # If the file exists, map the pokemon data
            if (path.exists(pokeHtml)):
                # Open file for parsing
                with open(pokeHtml, 'r', encoding='utf-8') as f:
                    content = f.read()
                    soup = BeautifulSoup(content, 'html.parser')

                    # Call functions here
                    updatePokemon(soup, natId)
                
    return

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
def updatePokemonForm( pokeName, forms, dexId ):
    formNames = getFormNames( statTables, megaTables )
    legTables = getLegendTables()

    # Check if any forms not yet created
    for formIndex in range(0, len(formNames)):
        formName = formNames[formIndex]
        if formName not in forms.keys():
            # base form
            isBase = formName == 'Base'
            # mega form
            isMega = formName.startswith('Mega ')
            
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
            if not formName.startswith('Mega '):
                formStats[formName] = getBaseStats( formStats, formName, statTables )
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
                formTypes = getPokeFormTypes(pokeName, formName, allTables)
            else:
                formTypes = getMegaTypes(formName, megaTables)
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
                abilities = getFormAbilities( formName, isBase, allTables )
            else:
                abilities = getMegaAbilities( formName, megaTables )
            #cur.execute(SELECT_AB_BY_NAME,[abilities[0]])
            #ability1 = cur.fetchone()
            #cur.execute(SELECT_AB_BY_NAME,[abilities[1]])
            #ability2 = cur.fetchone()
            #cur.execute(SELECT_AB_BY_NAME,[abilities[2]])
            #abilityH = cur.fetchone()
            
            # pokeId
            #cur.execute(SELECT_POKE_BY_NATID,[dexId])
            #poke = cur.fetchone();
            #pokeId = poke[0] if poke is not None else None

            ## DB UPDATE ##
            #cur.execute(SELECT_PFORM_BY_DEX_FORM,[formName,dexId])
            #pokeForm = cur.fetchone()
            # If it doesn't exist, insert
            #if pokeForm is None:
                #cur.execute(INSERT_POKE_FORM,[formName,gender,
                #                              sprite, icon, shiny,
                #                              height, weight, baseHp, baseAtk, baseDef,
                #                              baseSpatk, baseSpdef, baseSpeed, can_dmax,
                #                              has_gmax, legendary, sub_legend, mythic,
                #                              type1, type2, ability1, ability2, abilityH, pokeId])
            # Otherwise update
            # else:
            forms[formName] = {}
            forms[formName]['isBase'] = isBase
            forms[formName]['gender'] = gender
            forms[formName]['sprite'] = sprite
            forms[formName]['icon'] = icon
            forms[formName]['shiny'] = shiny
            forms[formName]['height'] = height
            forms[formName]['weight'] = weight
            forms[formName]['stats'] = {}
            forms[formName]['stats']['baseHP'] = baseHp
            forms[formName]['stats']['baseAtk'] = baseAtk
            forms[formName]['stats']['baseDef'] = baseDef
            forms[formName]['stats']['baseSpatk'] = baseSpatk
            forms[formName]['stats']['baseSpdef'] = baseSpdef
            forms[formName]['stats']['baseSpeed'] = baseSpeed
            forms[formName]['can_dmax'] = can_dmax
            forms[formName]['has_gmax'] = has_gmax
            forms[formName]['legend'] = legendary
            forms[formName]['sub_legend'] = sub_legend
            forms[formName]['mythic'] = mythic
            forms[formName]['type1'] = type1
            forms[formName]['type2'] = type2
            forms[formName]['abilities'] = abilities
            forms[formName]['dexId'] = dexId

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
            if bold.text and bold.text.startswith('Mega Evolution'):
                megaName = bold.text.replace('Evolution', pokeName)
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

def getFormNames( statTables, megaTables ):
    forms = []
    for table in statTables:
        header = table.find('h2')
        if header is None:
            header = table.find('b')
        if header is not None and not header.text in forms:
            forms.append(header.text)  
    for i in range(0, len(forms)):
        forms[i] = translateFormName( forms[i] )

    for tables in megaTables:
        megaName = tables[0]
        if megaName is not None and megaName not in forms:
            forms.append(megaName)
    return forms

def translateFormName( headerText ):
    if headerText.strip() == 'Stats':
        return 'Base'
    else:
        toks = headerText.split('-')
        return toks[len(toks)-1].strip()

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
        malePer = int(gendPers[0].find_all('td')[1].text.split('.')[0].split('%')[0])
        femalePer = int(gendPers[1].find_all('td')[1].text.split('.')[0].split('%')[0])
        
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

def getBaseStats( formStats, formName, statTables ):
    # find the stat table for the specified form
    for i in range(0, len(statTables)):
        table = statTables[i]
        allRows = table.find_all('tr')
        header = allRows[0].find('h2')
        if header is None:
            header = allRows[0].find('b')
        if header is not None and formName == translateFormName(header.text):
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
        for form in evs:
            m = re.search(r'\d', form)
            if m and formName == form[:m.start()]:
                toks = form[m.start():].strip().split(' ', 1)
                val = toks[0]
                stat = translateStatString(toks[1])
                return val + ' ' + stat
        return None

def translateStatString( stat ):
    if stat.endswith('Sp. Attack'):
        return 'SpAtk'
    elif stat.endswith('Sp. Defense'):
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
            if (formName == 'Base' and foundName == pokeName) or formName == foundName:
                # found the types for the specified form
                for img in formData[1].find_all('img', class_='typeimg'):
                    toks = img['src'].split('/')
                    types.append(toks[len(toks)-1].split('.')[0])
            elif formName == 'Base' and i == 0:
                # found the base form, but form needs name updated
                formName = foundName
                for img in formData[1].find_all('img', class_='typeimg'):
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
        if ab != 'Hidden Ability' and (ab.endswith('Abilities') or ab.endswith('Ability')):
            singleSet = False

    # Reset foundForm if singleSet
    if not foundForm and singleSet:
        foundForm = True
    
    for i in range(0, len(allAbs)):
        ab = allAbs[i].text
        # First check hidden ability so that can use 'ability' as descriminator
        if foundForm and ab.strip() == 'Hidden Ability':
            abilityH = allAbs[i+1].text
            break
        # Next check if it is a form change line, then check if is specified form
        elif ab.strip().endswith('Abilities') or ab.strip().endswith('Ability'):
            form = ab.strip().rsplit(' ',1)[0]
            foundForm = form == formName
        # If working with specified form set ability 1 if not already set
        elif foundForm and ability1 == None:
            ability1 = allAbs[i].text
        # If working with found form and ability 1 is set, set ability 2
        elif foundForm:
            ability2 = allAbs[i].text

    return (ability1, ability2, abilityH)

def getMegaAbilities( formName, megaTables ):
    for mega in megaTables:
        if formName == mega[0]:
            #megaCol = 3 if mega[5] else 2
            abRow = mega[3].find_all('tr')[1]
            megaAbility = abRow.find('td').find('b').text
            return (megaAbility, None, None)

#############
# Test runner
def initIteration(start, end):
    formMap = {}
    for dexId in range(start, (end+1)):
        cur = con.cursor()
        cur.execute(SELECT_POKE_BY_NATID, [dexId])
        result = cur.fetchone()
        if result:
            formMap[result[2]] = importAllForms(dexId)
    return formMap

def importAllForms(dexId):
    forms = {}
    for i in reversed(range(1,9)):
        html = dataDir + 'Gen' + str(i) + '/' + str(dexId).zfill(3) + '.html'
        if not path.exists(html):
            continue
        print('Processing: ' + 'Gen' + str(i) + '/' + str(dexId).zfill(3) + '.html')
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
        updatePokemonForm(pokeName, forms, dexId)
    return forms

def initTests( genHtml, foundForms ):
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
    
    print(str(updatePokemonForms(soup, pokeName,dexId)))
