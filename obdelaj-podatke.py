import re
import orodja
import os
import requests

ST_STRANI = 24
POMOZNA_MAPA = 'pomozno.html'
URL = 'https://www.goodreads.com'
DIRECTORY = 'C:\\Users\\Taja\\Documents\\FMF\\2. letnik\\programiranje 1\\projektna naloga\\analiza-podatkov\\spletne-strani'

block_pattern = re.compile(
    r'<tr itemscope itemtype="http://schema.org/Book">.*?score:',
    flags=re.DOTALL    
)

book_pattern = re.compile(
    r'<td valign="top" class="number">(?P<id>\d+)</td>.*?'
    r'<a class="bookTitle" itemprop="url" href="(?P<link>.*)">.*?'
    r"<span itemprop='name' role='heading' aria-level='4'>(?P<naslov>.*?)</span>.*?"
    r'<a class="authorName" itemprop="url" href=".*"><span itemprop="name">(?P<avtor>.*?)<.*?'
    r'</span></span> (?P<ocena>\d\.\d+) avg rating &mdash;(?P<glasovi>.*) ratings</span>',
    flags=re.DOTALL        
)

pomozna_blok_vzorec = re.compile(
    r'<html class="desktop withSiteHeaderTopFullImage.*?'
    r'<a id="bookDataBoxShow"',
    flags=re.DOTALL
)

st_strani_vzorec = re.compile(
    r"<meta content='(?P<strani>\d+)' property='books:page_count'>"
)

zanri_vzorec = re.compile(
    r'googletag.pubads\(\).setTargeting\("shelf", \[(?P<zanri>.*?)\]\)',
    flags=re.DOTALL
)

datum_prve_izdaje_vzorec = re.compile(
    r'<nobr class="greyText">.*?'
    r'\(first published.*?\b(?P<leto>\d+)\b\).*?'
    r'</nobr>',
    flags=re.DOTALL
)

datum_izdaje_vzorec = re.compile(
    r'<div class="row">.*?'
    r'Published.*?\b(?P<leto>\d+)\b',
    flags=re.DOTALL
)

def shrani_pomozno_datoteko(link):
    ''' S pomočjo linka pobranega iz seznama najboljših knjig zacasno shrani vsako posamezno knjigo'''
    link_knjige = URL + link
    mapa = os.path.join(DIRECTORY, POMOZNA_MAPA)
    orodja.shrani_spletno_stran(link_knjige, mapa, True) 
    print('shranila pomozno datoteko')

def poberi_podatke_s_strani():
    mapa = os.path.join(DIRECTORY, POMOZNA_MAPA) 
    vsebina = orodja.vsebina_datoteke(mapa)
    blok = re.search(pomozna_blok_vzorec, vsebina).group(0)
    strani = re.search(st_strani_vzorec, blok)
    if strani:
        strani = int(strani['strani'])
    else:
        strani = None # nekatere knjige nimajo zabeleženih strani
    leto_izdaje = re.search(datum_prve_izdaje_vzorec, blok) 
    if leto_izdaje:
        leto_izdaje = leto_izdaje['leto'] # dobimo slovar letnic
    else:
        leto_izdaje = re.search(datum_izdaje_vzorec, blok)['leto']
    niz_zanrov = re.search(zanri_vzorec, blok).groupdict()
    zanri = niz_zanrov['zanri'].replace('"', '').split(',')
    return strani, leto_izdaje, zanri[:5]


def izloci_podatke_knjig(blok):
    data = re.search(book_pattern, blok)
    knjiga = data.groupdict()
    knjiga['id'] = int(knjiga['id'])
    knjiga['avtor'] = knjiga['avtor'].strip()
    knjiga['ocena'] = float(knjiga['ocena'])
    glasovi_niz = knjiga['glasovi'].strip().replace(',', '')
    knjiga['glasovi'] = int(glasovi_niz)
    # preverimo, če je v seriji
    if '#' in knjiga['naslov']:
        knjiga['serija'] = True
    else:
        knjiga['serija'] = False
    # nekoliko nerodna koda, ker sem zajela še dodatne podatke iz strani posameznih knjig
    shrani_pomozno_datoteko(knjiga['link'])
    strani, leto_izdaje, zanri = poberi_podatke_s_strani()
    knjiga['strani'] = strani
    if leto_izdaje:
        knjiga['leto'] = int(leto_izdaje)
    else:
        knjiga['leto'] = leto_izdaje    
    knjiga['zanri'] = zanri
    del knjiga['link']      
    return knjiga  

def knjige_na_strani(stevilka_strani):
    zacetek = stevilka_strani * 100 + 1
    konec = (stevilka_strani + 1) * 100
    ime = f'knjige-od-{zacetek}-do-{konec}.html'
    ime_dat = os.path.join(DIRECTORY, ime)
    vsebina = orodja.vsebina_datoteke(ime_dat)
    for blok in re.finditer(block_pattern, vsebina):
        yield izloci_podatke_knjig(blok.group(0))

def izloci_zanre(knjige):
    zanri = []
    for knjiga in knjige:
        for zanr in knjiga.pop('zanri'):
            zanri.append({'knjiga': knjiga['id'], 'zanr': zanr})

    zanri.sort(key=lambda zanr: (zanr['knjiga'], zanr['zanr']))
    return zanri


knjige = []
for stevilka_strani in range(ST_STRANI):
    for knjiga in knjige_na_strani(stevilka_strani):
      knjige.append(knjiga)
knjige.sort(key=lambda knjiga: knjiga['id'])

zanri = izloci_zanre(knjige)
# orodja.zapisi_json(knjige, 'obdelani-podatki\\knjige.json')

orodja.zapisi_csv(knjige, ['id', 'avtor', 'naslov', 'ocena', 'glasovi', 'strani', 'leto', 'serija'], 'obdelani-podatki\\knjige.csv')

orodja.zapisi_csv(zanri, ['knjiga', 'zanr'], 'obdelani-podatki\\zanri.csv')





