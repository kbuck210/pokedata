import sqlite3

dbPath = '/Users/kbuck/Documents/AndriodStuff/BattleDex/BattleDex/PokeRef/app/src/main/assets/BattleDex.db'

con = sqlite3.connect(dbPath)
cur = con.cursor()

def threatAlgo():
    team = getTeam()

    
    return


def getTeam():
    # mons: coalossal, dragonite, celesteela, swampert, grimmsnarl
    cur.execute("SELECT * FROM PokemonForm WHERE pokeFormId=968")
    coalossal = cur.fetchone()

    cur.execute("SELECT * FROM PokemonForm WHERE pokeFormId=193")
    dragonite = cur.fetchone()

    cur.execute("SELECT * FROM PokemonForm WHERE pokeFormId=923")
    celesteela = cur.fetchone()

    cur.execute("SELECT * FROM PokemonForm WHERE pokeFormId=316")
    swampert = cur.fetchone()

    cur.execute("SELECT * FROM PokemonForm WHERE pokeFormId=990")
    grimmsnarl = cur.fetchone()

    return [coalossal, dragonite, celesteela, swampert, grimmsnarl]
