import sqlite3

mappedTargets = {
    'SELECTED_TARGET': ['Selected Target',
                        'Selected target',
                        'Targeted Pokémon',
                        'Opponent',
                        'adjacentFoe'],
    'ALL_ENEMIES': ['All Adjacent Foes',
                    'All opponent Pokémon in range',
                    'Both opponents',
                    'All Adjacent Opponents',
                    'All opponents',
                    "All opponent's Pokémon in range",
                    'Enemy Side',
                    'Entry Hazard',
                    "Opponent's Field",
                    'Opponent team',
                    "Opponent's Side"],
    'SELF': ['Self','User'],
    'SINGLE_ALLY': ['Self or Ally',
                    'Team-mate or User',
                    'Adjacent Ally',
                    'Team-mate',
                    'Ally'],
    'SINGLE_ENEMY': ['Last opponent who moved',
                     'Special',
                     'Attacker',
                     'Random Target',
                     'Random Opponent',
                     'Random target'],
    'ALL_ALLIES': ['Team','Party',
                   "User's Party",
                   "User's party",
                   'User and Allies',
                   'All Allies',
                   'Allies','Varies'],
    'ALL_ADJACENT': ['Everyone else','All Adjacent Pokémon',
                    'All adjacent to user','All Pokémon in range'],
    'ALL_POKEMON': ['Field',
                    'All',
                    'All active',
                    'Battlefield',
                    'All Pokémon']
    }

db = "G:/Android Development/Database Stuff/PokeRef/PythonDev/pokedata/PokeRefDbNew.db"

remapped = {}
for key in mappedTargets:
    values = mappedTargets[key]
    for val in values:
        remapped[val] = key

def fixTargets():
    con = sqlite3.connect(db)
    cur = con.cursor()

    for key in remapped:
        # get the moves for the selected target key, and update the targets
        cur.execute('SELECT atkFormId FROM AttackByGen WHERE target=?',[key])
        atks = cur.fetchall()

        for atkId in atks:
            cur.execute('UPDATE AttackByGen SET target=? WHERE atkFormId=?',
                        [remapped[key],atkId[0]])
            con.commit()
            print('Updated ' + key + ' to ' + remapped[key])
            
    con.close()

def setTargetsAsOrdinal():
    mappedordinal = {
        'ALL_ADJACENT': 0,
        'ALL_ALLIES': 1,
        'ALL_ENEMIES': 2,
        'ALL_POKEMON': 3,
        'SELECTED_TARGET': 4,
        'SELF': 5,
        'SINGLE_ALLY': 6,
        'SINGLE_ENEMY': 7
        }

    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute('SELECT atkFormId,target FROM AttackByGen')
    allAtks = cur.fetchall()

    for atk in allAtks:
        cur.execute('UPDATE AttackByGen SET target=? WHERE atkFormId=?',
                    [mappedordinal[atk[1]],atk[0]])
        con.commit()

    con.close()

def testStuff():
    val = '10'
    try:
        intval = int(val)
    except:
        print('error on 1!')

    val = '10%'
    try:
        intval = int(val)
    except:
        print('error on 2!')
