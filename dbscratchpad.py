import sqlite3
from os import path

dbPath = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/PokeRefDbNew.db'
if not path.exists(dbPath):
    dbPath = 'G:\\Android Development\\Database Stuff\\PokeRef\\PythonDev\\pokedata\\PokeRefDbNew.db'

con = sqlite3.connect(dbPath)


# write gassy glide
def grassyGlide():
    cur = con.cursor()
    # insert attack if not exists
    cur.execute('SELECT atkId FROM Attack WHERE atkName="Grassy Glide"')
    exists = cur.fetchone()
    if not exists:
        cur.execute('INSERT INTO Attack(atkName) VALUES (?)',['Grassy Glide'])
        con.commit()
    cur.execute('SELECT atkId FROM Attack WHERE atkName="Grassy Glide"')
    atkId = cur.fetchone()[0]

    # insert for gen 8
    atkCategory = 'physical'
    atkDesc = 'Gliding on the ground, the user attacks the target. This move always goes first on Grassy Terrain.'
    atkEffect = 'Increases priority in Grassy Terrain'
    bp = '70'
    acc = '100'
    pp = '20'
    effPercent = '-- %'
    critRate = '4.17%'
    target = 'Selected Target'
    maxMove = 'Max Overgrowth'
    maxPow = '120'
    priority = 0
    breaksProtect = False
    contacting = True
    soundMove = False
    bitingMove = False
    punchMove = False
    copyable = True
    thaws = False
    reflectable = False
    gravityAffected = False
    snatchable = False
    typeId = 10 # grass
    # make sure not exists
    cur.execute('SELECT * FROM AttackByGen WHERE atkId=? AND genId=?',[atkId,8])
    existing = cur.fetchone()
    if not existing:
        cur.execute("""INSERT INTO AttackByGen(
                            atkCategory,atkDesc,
                            atkEffect,bp,acc,pp,effPercent,
                            critRate,target,maxMove,maxPower,
                            priority,breaksProtect,contacting,
                            soundMove,bitingMove,punchMove,
                            copyable,thaws,reflectable,
                            gravityAffected,snatchable,
                            typeId,atkId,genId) 
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",[
                            atkCategory, atkDesc,
                            atkEffect, bp, acc, pp, effPercent,
                            critRate, target, maxMove, maxPow,
                            priority, breaksProtect, contacting,
                            soundMove, bitingMove, punchMove,
                            copyable, thaws, reflectable,
                            gravityAffected, snatchable,
                            typeId, atkId, 8])
        con.commit()
    
                        
