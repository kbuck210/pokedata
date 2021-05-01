import requests
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

base_url = 'https://www.serebii.net/'

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
