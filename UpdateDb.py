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
SELECT_TYPE_BY_NAME = 'SELECT * FROM Type WHERE typeName=?'

# Connect to database
con = sqlite3.connect(dbPath)

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
def updatePokemonForms( soup, pokeName, dexId ):
    allTables = getAllTables(soup)
    statTables = getStatTables( allTables )

    # FIELDS
    # formName (default Base)
    formNames = getFormNames( statTables )

    for formName in formNames:
        # base form
        isBase = formName == 'Base'
        
        # gender (genderless = 0, gendered = 1, male-only = 2, female-only = 3)
        gender = getGender( allTables )

        # icon
        # shinySprite
        # sprite (handle multi-forms manually)
        if len(formNames) < 2:
            sprite = 'sp_' + dexId + '.png'
            shiny = 'sh_' + dexId + '.png'
            icon = 'ic_' + dexId + '.png'
        else:
            # TODO handle multi-form

        # height
        # weight
        
        # baseHp
        # baseAtk
        # baseDef
        # baseSpatk
        # baseSpdef
        # baseSpeed
        formStats = {}
        for formName in formNames:
            formStats = getBaseStats( formStats, formName, statTables )
        
        # can_dmax
        # has_gmax
        # legendary
        # sub_legend
        # mythic
        
        # type1
        # type2
        formTypes = getPokeFormTypes(pokeName, formName, allTables)
        # check result to see if formName needs to be updated from base
        formKey = list(formTypes.keys())[0]
        if formName == 'Base' and formKey != 'Base':
            formName = formKey
        
        # ability1
        # ability2
        # abilityH
        # pokeId
    

def getAllTables( soup ):
    return soup.find_all('table', class_='dextable')

def getGender( allTables ):
    # table with gender is 2nd table, 2nd row
    gendRow = allTables[1].find_all('tr')[1]
    gendCol = gendRow.find_all('td', class_='fooinfo')[3]
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
    

def getPokeFormTypes( pokeName, formName, allTables ):
    # table with types is 2nd table, 2nd row
    typeRow = allTables[1].find_all('tr')[1]
    typeCol = typeRow.find('td', class_='cen')
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
        for img in typeCol.find_all('img', class_='typeimg'):
            toks = img['src'].split('/')
            types.append(toks[len(toks)-1].split('.')[0])

    # return as mapped object to update the form name where required
    return { formName: types } 

def getStatTables( allTables ):
    statTables = []
    for table in allTables:
        headers = table.find_all('h2')
        if headers is None:
            headers = table.find_all('b')
        for title in headers:
            if title.text.startswith('Stats'):
                statTables.append(table)
    return statTables

def getFormNames( statTables ):
    forms = []
    for table in statTables:
        header = table.find('h2')
        if header is None:
            header = statTable.find('b')
        if header is not None:
            forms.append(header.text)
    for i in range(0, len(forms)):
        forms[i] = translateFormName( forms[i] )
    return forms

def translateFormName( headerText ):
    if headerText.strip() == 'Stats':
        return 'Base'
    else:
        toks = headerText.split('-')
        return toks[len(toks)-1].strip()

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
        formStats[formName] = baseStats

    return formStats
