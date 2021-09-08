import sqlite3
import requests
import os
import re
from os import path

dbPath = '/Users/kbuck/Documents/AndriodStuff/BattleDex/BattleDex/PokeRef/app/src/main/assets/databases/BattleDex.db'

missingDir = '/Users/kbuck/Documents/AndriodStuff/Pokeref/sprites/missing_sprites/'

con = sqlite3.connect(dbPath)
cur = con.cursor()

missingFrom8 = [4, 8, 9, 13, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 60, 61, 62, 63, 75, 76, 85, 89, 90, 91, 94, 95, 96, 97, 98, 99, 108, 113, 114, 115, 116, 117, 118, 119, 120, 126, 128, 129, 132, 133, 151, 165, 169, 173, 183, 195, 196, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 211, 212, 213, 214, 225, 226, 227, 228, 234, 235, 236, 237, 238, 239, 240, 245, 248, 249, 251, 252, 253, 255, 257, 258, 259, 262, 265, 267, 268, 269, 270, 280, 281, 282, 284, 285, 287, 288, 302, 309, 313, 317, 318, 319, 324, 325, 326, 327, 328, 335, 336, 342, 343, 344, 345, 346, 347, 348, 349, 356, 357, 359, 360, 361, 363, 365, 369, 370, 371, 372, 375, 376, 377, 378, 379, 381, 382, 385, 388, 389, 390, 392, 393, 394, 398, 399, 402, 403, 404, 419, 420, 421, 422, 423, 426, 427, 429, 433, 437, 438, 439, 441, 445, 449, 454, 456, 459, 461, 463, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 490, 491, 492, 493, 494, 495, 496, 497, 498, 501, 502, 503, 508, 513, 514, 515, 516, 517, 518, 526, 531, 535, 542, 543, 544, 548, 557, 560, 564, 565, 584, 585, 586, 587, 588, 589, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 607, 608, 609, 610, 611, 612, 618, 619, 628, 637, 638, 639, 681, 682, 686, 687, 695, 703, 704, 705, 755, 756, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 786, 840, 841, 842, 853, 854, 855, 856, 857, 861, 862, 863, 899, 900, 901, 905, 929]

baseUrl = 'https://img.pokemondb.net/sprites/'
goUrl = baseUrl + 'go/'
homeUrl = baseUrl + 'home/'

sql = "SELECT A.name, B.formName, B.isBase, B.sprite, B.shinySprite FROM Pokemon AS A, PokemonForm AS B WHERE A.pokeId = B.pokeId AND B.pokeFormId=?"

def getAltForms(startIndex, endIndex):
    altForms = []
    for i in range(startIndex, endIndex):
        print('********* Processing index ' + str(i) + ' *********')
        pokeFormId = missingFrom8[i]
        cur.execute(sql,[pokeFormId])
        form = cur.fetchone()
        if not form[2]:
            altForms.append(form)
            
    return altForms

def getAltSprites(altForms):
    skipped = []
    error = []
    for form in altForms:
        name = form[0]
        formName = form[1]
        toks = re.split(' |-', formName)
        filtered = []
        for tok in toks:
            if tok != name:
                filtered.append(tok)

        print('********* Processing index ' + formName + ' *********')

        goNormalUrl = goUrl + 'normal/' + name + '-' + filtered[0]
        for i in range(1, len(filtered)):
            goNormalUrl = goNormalUrl + '-' + filtered[i]
        goNormalUrl += '.png'

        goShinyUrl = goUrl + 'shiny/' + name + '-' + filtered[0]
        for i in range(1, len(filtered)):
            goShinyUrl = goShinyUrl + '-' + filtered[i]
        goShinyUrl += '.png'

        homeNormalUrl = homeUrl + 'normal/' + name + '-' + filtered[0]
        for i in range(1, len(filtered)):
            homeNormalUrl = homeNormalUrl + '-' + filtered[i]
        homeNormalUrl += '.png'

        homeShinyUrl = homeUrl + 'shiny/' + name + '-' + filtered[0]
        for i in range(1, len(filtered)):
            homeShinyUrl = homeShinyUrl + '-' + filtered[i]
        homeShinyUrl += '.png'

        normalPath = missingDir + 'sprites/' + form[3]
        r = requests.get(goNormalUrl.lower(), stream=True)
        if r.status_code == 200:
            with open(normalPath, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        else:
            r = requests.get(homeNormalUrl.lower(), stream=True)
            if r.status_code == 200:
                with open(normalPath, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
            else:
                error.append(form)

        shinyPath = missingDir + 'shiny/' + form[4]
        r = requests.get(goShinyUrl.lower(), stream=True)
        if r.status_code == 200:
            with open(shinyPath, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        else:
            r = requests.get(homeShinyUrl.lower(), stream=True)
            if r.status_code == 200:
                with open(shinyPath, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
            else:
                error.append(form)
    print('Errors: ')
    print(error)

def downloadSprites(startIndex, endIndex):
    skipped = []
    errors = []
    for i in range(startIndex, endIndex):
        print('********* Processing index ' + str(i) + ' *********')
        pokeFormId = missingFrom8[i]
        cur.execute(sql,[pokeFormId])
        form = cur.fetchone()
        if form[2]:
            goNormalUrl = goUrl + 'normal/' + form[0].lower() + '.png'
            goShinyUrl = goUrl + 'shiny/' + form[0].lower() + '.png'

            homeNormalUrl = homeUrl + 'normal/' + form[0].lower() + '.png'
            homeShinyUrl = homeUrl + 'shiny/' + form[0].lower() + '.png'
        else:
            skipped.append(form)
            continue

        normalPath = missingDir + 'sprites/' + form[3] 
        r = requests.get(goNormalUrl, stream=True)
        if r.status_code == 200:
            with open(normalPath, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        else:
            r = requests.get(homeNormalUrl, stream=True)
            if r.status_code == 200:
                with open(normalPath, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
            else:
                errors.append(form)

        shinyPath = missingDir + 'shiny/' + form[4]
        r = requests.get(goShinyUrl, stream=True)
        if r.status_code == 200:
            with open(shinyPath, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        else:
            r = requests.get(homeShinyUrl, stream=True)
            if r.status_code == 200:
                with open(shinyPath, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
            else:
                errors.append(form)

    print('Skipped: ')
    print(skipped)
    print('')
    print('Errors: ')
    print(errors)
