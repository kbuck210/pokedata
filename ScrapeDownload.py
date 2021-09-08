import requests
import os
from os import path
from os import mkdir
from bs4 import BeautifulSoup

# Scrape Serebii Dexes
gen8 = "pokedex-swsh/"
gen7 = "pokedex-sm/"
gen6 = "pokedex-xy/"
gen5 = "pokedex-bw/"
gen4 = "pokedex-dp/"
gen3 = "pokedex-rs/"
gen2 = "pokedex-gs/"
gen1 = "pokedex/"

atk8 = "attackdex-swsh/"
atk7 = "attackdex-sm/"
atk6 = "attackdex-xy/"
atk5 = "attackdex-bw/"
atk4 = "attackdex-dp/"
atk3 = "attackdex/"
atk2 = "attackdex-gs/"
atk1 = "attackdex-rby/"

# Scrape Ability Dexes
abdex = "abilitydex/"

# Scrape Item Dex
itemdex = "itemdex/"

# Gen output folders
gen8out = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/DexPages/Gen8/'
gen7out = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/DexPages/Gen7/'
gen6out = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/DexPages/Gen6/'
gen5out = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/DexPages/Gen5/'
gen4out = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/DexPages/Gen4/'
gen3out = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/DexPages/Gen3/'
gen2out = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/DexPages/Gen2/'
gen1out = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/DexPages/Gen1/'

# Gen max dex numbers
gen8max = 898
gen7max = 809
gen6max = 721
gen5max = 649
gen4max = 493
gen3max = 386
gen2max = 251
gen1max = 151

dataDir = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/DexPages/'
if not path.exists(dataDir):
    dataDir = 'G:\\Android Development\\Database Stuff\\PokeRef\\PythonDev\\pokedata\\DexPages\\'
base_url = 'https://www.serebii.net/'

def getLegends():
    url = 'https://www.serebii.net/pokemon/legendary.shtml'
    page = requests.get(url)
    lsoup = BeautifulSoup(page.content, 'html.parser')
    legFile = '/Users/kbuck/Documents/MacDeveloper/Python Scraping/legends.html'
    try:
        with open(legFile, 'w', encoding='utf-8') as f:
            f.write(str(lsoup))
    except IOError as e:
        print('Failed to write ' + maleOut)

def cyclePokemon():
    # Test with just Charizard TODO: change to range(1, 899)
    for dexId in range(1, 899):
        dexIdStr = str(dexId).zfill(3)
        
        # Get the dex entry for each gen if it exists and write it to a file
        output = getDexEntry( gen8, gen8out, dexIdStr )
        if (output is not None):
            toks = output.split('/')
            name = toks[len(toks) - 1]
            print('Wrote Gen8: #' + dexIdStr)
        else:
            print('No Gen 8 Entry for #' + dexIdStr)

        # Check if nat dex ID exists for gen 7
        if (dexId <= gen7max):
            output = getDexEntry( gen7, gen7out, dexIdStr )
            if (output is not None):
                toks = output.split('/')
                name = toks[len(toks) - 1]
                print('Wrote Gen7: #' + dexIdStr)
            else:
                print('No Gen 7 Entry for #' + dexIdStr)
        # If out of range of gen 7, will be out of range for prior gens also
        else:
            continue;

        # Check if nat dex ID exists for gen 6
        if (dexId <= gen6max):
            output = getDexEntry( gen6, gen6out, dexIdStr )
            if (output is not None):
                toks = output.split('/')
                name = toks[len(toks) - 1]
                print('Wrote Gen6: #' + dexIdStr)
            else:
                print('No Gen 6 Entry for #' + dexIdStr)
        # If out of range of gen 6, will be out of range for prior gens also
        else:
            continue

        # Check if nat dex ID exists for gen 5
        if (dexId <= gen5max):
            output = getDexEntry( gen5, gen5out, dexIdStr )
            if (output is not None):
                toks = output.split('/')
                name = toks[len(toks) - 1]
                print('Wrote Gen5: #' + dexIdStr)
            else:
                print('No Gen 5 Entry for #' + dexIdStr)
        # If out of range of gen 5, will be out of range for prior gens also
        else:
            continue

        # Check if nat dex ID exists for gen 4
        if (dexId <= gen4max):
            output = getDexEntry( gen4, gen4out, dexIdStr )
            if (output is not None):
                toks = output.split('/')
                name = toks[len(toks) - 1]
                print('Wrote Gen4: #' + dexIdStr)
            else:
                print('No Gen 4 Entry for #' + dexIdStr)
        # If out of range of gen 4, will be out of range for prior gens also
        else:
            continue

        # Check if nat dex ID exists for gen 3
        if (dexId <= gen3max):
            output = getDexEntry( gen3, gen3out, dexIdStr )
            if (output is not None):
                toks = output.split('/')
                name = toks[len(toks) - 1]
                print('Wrote Gen3: #' + dexIdStr)
            else:
                print('No Gen 3 Entry for #' + dexIdStr)
        # If out of range of gen 3, will be out of range for prior gens also
        else:
            continue

        # Check if nat dex ID exists for gen 2
        if (dexId <= gen2max):
            output = getDexEntry( gen2, gen2out, dexIdStr )
            if (output is not None):
                toks = output.split('/')
                name = toks[len(toks) - 1]
                print('Wrote Gen2: #' + dexIdStr)
            else:
                print('No Gen 2 Entry for #' + dexIdStr)
        # If out of range of gen 2, will be out of range for prior gens also
        else:
            continue

        # Check if nat dex ID exists for gen 1
        if (dexId <= gen1max):
            output = getDexEntry( gen1, gen1out, dexIdStr )
            if (output is not None):
                toks = output.split('/')
                name = toks[len(toks) - 1]
                print('Wrote Gen1: #' + dexIdStr)
            else:
                print('No Gen 1 Entry for #' + dexIdStr)

    return

def getGen8Nidos():
    male = 'nidoranm/'
    female = 'nidoranf/'
    maleUrl = base_url + gen8 + male
    femaleUrl = base_url + gen8 + female

    malePage = requests.get(maleUrl)
    femalePage = requests.get(femaleUrl)

    if malePage.status_code == 200:
        maleOut = gen8out + '032.html'
        soup = BeautifulSoup(malePage.content, 'html.parser')
        try:
            with open(maleOut, 'w', encoding='utf-8') as f:
                f.write(str(soup))
        except IOError as e:
            print('Failed to write ' + maleOut)

    if femalePage.status_code == 200:
        femaleOut = gen8out + '029.html'
        soup = BeautifulSoup(femalePage.content, 'html.parser')
        with open(femaleOut, 'w', encoding='utf-8') as f:
            f.write(str(soup))

def getDexEntry( genUrl, genOut, dexIdStr ):
    url = base_url + genUrl + dexIdStr + '.shtml'

    page = requests.get(url)
    if (page.status_code == 200):
        outfile = genOut + dexIdStr + '.html'
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            with open(outfile, 'w', encoding='utf-8') as file:
                file.write(str(soup))
            return outfile
        except IOError as e:
            print('Failed to write ' + outfile)
            return None
    else:
        return None

def cycleAbilities():
    abFile = dataDir + 'abilities.txt'
    with open(abFile, 'r', encoding='utf-8') as f:
        getAbilityEntries(f.readlines())

def getAbilityEntries( abilities ):
    for ability in abilities:
        ability = ability.lower().replace(' ','').strip()
        url = base_url + abdex + ability + '.shtml'
        print(url)
        page = requests.get(url)
        print('status: ' + str(page.status_code))
        if page.status_code == 200:
            outFile = dataDir + 'Abilities/' + ability + '.html'
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                with open(outFile, 'w', encoding='utf-8') as file:
                    file.write(str(soup))
                    print('Wrote: ' + ability + '.html')
            except IOError as e:
                print('Failed to write ' + outfile)

def getItemEntries():
    itemdex = 'https://www.serebii.net/itemdex/'
    itemFile = dataDir + 'items.txt'
    with open(itemFile, 'r', encoding='utf-8') as f:
        itemlist = f.readlines()
	
    items = []
    for itemline in itemlist:
        toks = itemline.split('">')
        itemurl = toks[0]
        itemname = toks[1].split('</option>')[0]
        items.append({ 'url': itemurl, 'name': itemname })
	
    for item in items:
        url = itemdex + item['url']
        page = requests.get(url)
        if page.status_code == 200:
            outname = item['url'].replace('.shtml','.html')
            outfile = dataDir + 'Items/' + outname
            soup = BeautifulSoup(page.content, 'html.parser')
            with open(outfile, 'w', encoding='utf-8') as f:
                f.write(str(soup))
                print('Wrote: ' + outname)
        else:
            print('Error ' + str(page.status_code) + ' for ' + item['url'])

def cycleAttacks():
    atkFile = dataDir + 'attacks.txt'
    with open(atkFile, 'r', encoding='utf-8') as f:
        attacks = f.read().splitlines()

    for attack in attacks:
        # Test to see if in each gen
        atkHtml = attack.lower().strip().replace(' ', '') + '.shtml'
        # Gen 8
        gen8url = base_url + atk8 + atkHtml
        page = requests.get(gen8url)
        if page.status_code == 200:
            downloadAttack(page, 'Gen8/', atkHtml)
        # Gen 7
        gen7url = base_url + atk7 + atkHtml
        page = requests.get(gen7url)
        if page.status_code == 200:
            downloadAttack(page, 'Gen7/', atkHtml)
        # Gen 6
        gen6url = base_url + atk6 + atkHtml
        page = requests.get(gen6url)
        if page.status_code == 200:
            downloadAttack(page, 'Gen6/', atkHtml)
        # Gen 5
        gen5url = base_url + atk5 + atkHtml
        page = requests.get(gen5url)
        if page.status_code == 200:
            downloadAttack(page, 'Gen5/', atkHtml)
        # Gen 4
        gen4url = base_url + atk4 + atkHtml
        page = requests.get(gen4url)
        if page.status_code == 200:
            downloadAttack(page, 'Gen4/', atkHtml)
        # Gen 3
        gen3url = base_url + atk3 + atkHtml
        page = requests.get(gen3url)
        if page.status_code == 200:
            downloadAttack(page, 'Gen3/', atkHtml)
        # Gen 2
        gen2url = base_url + atk2 + atkHtml
        if page.status_code == 200:
            downloadAttack(page, 'Gen2/', atkHtml)
        # Gen 1
        gen1url = base_url + atk1 + atkHtml
        if page.status_code == 200:
            downloadAttack(page, 'Gen1/', atkHtml)


def downloadAttack( page, gen, atkHtml ):
    # check whether the gen directory exists, if not create it
    if gen:
        atkGenDir = dataDir + 'Attacks/' + gen
    else:
        atkGenDir = dataDir + 'Attacks/'
    if not path.exists(atkGenDir):
        os.mkdir(atkGenDir)

    outFile = atkGenDir + atkHtml.replace('.shtml','.html')
    soup = BeautifulSoup(page.content, 'html.parser')
    with open(outFile, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        print('Wrote: ' + atkHtml.replace('.shtml','.html'))

def downloadMissingMoves(atkName):
    urlname = atkName.lower().strip().replace(' ','') + '.shtml'
    gen8page = requests.get(base_url + atk8 + urlname)
    if gen8page.status_code == 200:
        if atkName.startswith('Max ') or atkName.startswith('G-Max '):
            downloadAttack( gen8page, None, urlname)
        else:
            downloadAttack( gen8page, 'Gen8/', urlname)
    gen7page = requests.get(base_url + atk7 + urlname)
    if gen7page.status_code == 200:
        downloadAttack( gen7page, 'Gen7/', urlname)
    gen6page = requests.get(base_url + atk6 + urlname)
    if gen6page.status_code == 200:
        downloadAttack( gen6page, 'Gen6/', urlname)
    gen5page = requests.get(base_url + atk5 + urlname)
    if gen5page.status_code == 200:
        downloadAttack( gen5page, 'Gen5/', urlname)
    gen4page = requests.get(base_url + atk4 + urlname)
    if gen4page.status_code == 200:
        downloadAttack( gen4page, 'Gen4/', urlname)   

def redownloadMaxMoves():
    maxfile = dataDir + 'Attacks/maxmoves.txt'
    with open(maxfile, 'r', encoding='utf-8') as f:
        maxmoves = f.read().splitlines()

    for maxmove in maxmoves:
        html = maxmove.lower().strip().replace(' ','') + '.html'
        file = dataDir + 'Attacks/' + html
        if not path.exists(file):
            downloadMissingMoves(maxmove)
            print('downloaded ' + html)

def scrapeMaxZAttacks(writeNames, download):
    maxurl = 'https://www.serebii.net/swordshield/maxmoves.shtml'
    zurl = 'https://www.serebii.net/sunmoon/zmoves.shtml'
    nameFile = dataDir + 'Attacks/maxmoves.txt'

    maxPage = requests.get(maxurl)
    if maxPage.status_code == 200:
        soup = BeautifulSoup(maxPage.content, 'html.parser')
        maxmoves = getMaxNames(soup)
    zpage = requests.get(zurl)
    if zpage.status_code == 200:
        soup = BeautifulSoup(zpage.content, 'html.parser')
        zmoves = getMaxNames(soup)

    if writeNames:
        with open(nameFile, 'w', encoding='utf-8') as f:
            for maxmove in maxmoves.keys():
                f.write(maxmove+'\n')
            for zmove in zmoves.keys():
                f.write(zmove+'\n')

    if download:
        maxBase = 'https://www.serebii.net/attackdex-swsh/'
        zBase = 'https://www.serebii.net/attackdex-sm/'
        for maxAtk in maxmoves.keys():
            maxurl = maxBase + maxmoves[maxAtk]
            page = requests.get(maxurl)
            if page.status_code == 200:
                downloadMaxZAttacks(page, maxmoves[maxAtk])
            else:
                print('Failed to get ' + maxAtk)

        for zAtk in zmoves.keys():
            zurl = zBase + zmoves[zAtk]
            page = requests.get(zurl)
            if page.status_code == 200:
                downloadMaxZAttacks(page, zmoves[zAtk])
            else:
                print('Failed to get ' + zAtk)

def getMaxNames(soup):
    moveTable = soup.find_all('table', class_='tab')[1]
    allTrs = moveTable.find_all('tr', recursive=False)
    moveurls = {}
    for r in range(1, len(allTrs)):
        name = allTrs[r].find('a').text
        url = name.lower().strip().replace(' ', '') + '.shtml'
        moveurls[name] = url

    return moveurls

def downloadMaxZAttacks( page, html ):
    atkDir = dataDir + 'Attacks/'
    outfile = atkDir + html.replace('.shtml','.html')
    soup = BeautifulSoup(page.content, 'html.parser')
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        print('Wrote: ' + html.replace('.shtml','.html'))

