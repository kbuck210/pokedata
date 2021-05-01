import requests
from bs4 import BeautifulSoup

# Screen Scraping Pokedex
# Check each pokemon for each generation, creating JSON output for the table schema
#
# Generations:
gen8 = "pokedex-swsh/"
gen7 = "pokedex-sm/"
gen6 = "pokedex-xy/"
gen5 = "pokedex-bw/"
gen4 = "pokedex-dp/"
gen3 = "pokedex-rs/"
gen2 = "pokedex-gs/"
gen1 = "pokedex/"

#
# Total Pokedex numbers 001-898
#
# Tables:
# Pokemon
# PokemonForm
# PokemonInDex
# Attack
# AttackForm
# AttacksInDex

base_url = 'https://www.serebii.net/'

def cyclePokemon():
    # Test with just Charizard TODO: change to range(1, 899)
    for dexId in range(895, 899):
        dexIdStr = str(dexId).zfill(3)
        gen8Url = base_url + gen8 + dexIdStr + '.shtml'

        gen8page = requests.get(gen8Url)
        gen8soup = BeautifulSoup(gen8page.content, 'html.parser')
        # First dextab table is the header
        gen8dextab = gen8soup.find('table', class_='dextab')

        name = getName( dexId, gen8dextab )
        forms = getFormNames( gen8soup )

        headerStr = '#' + dexIdStr + ': ' + name;
        if (forms is not None and len(forms) > 0):
            headerStr = headerStr + ' - ' + str(forms)
        print(headerStr)
    return

# Validate & Get the Pokemon's Name
def getName( dexId, dexTab ):
    header = dexTab.find('h1')
    if (header is None):
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
    return arr[1]

# Get the list of forms (if any)
def getFormNames( soup ):
    forms = soup.find_all('a', class_='sprite-select')
    if (len(forms) == 0):
        return None

    formNames = []
    for form in forms:
        formNames.append(form['title'])

    return formNames


