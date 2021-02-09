import os
import orodja
import re

POMOZNA_MAPA = 'pomozno.html'
URL = 'https://www.goodreads.com'
link_knjige = '/book/show/1953.A_Tale_of_Two_Cities'
DIRECTORY = 'C:\\Users\\Taja\\Documents\\FMF\\2. letnik\\programiranje 1\\projektna naloga\\analiza-podatkov\\spletne-strani'

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
    ''' S pomočjo linka pobranega iz seznama najboljših knjig zacasno shrani vsako posamezno sliko'''
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
        strani = None
    leto_izdaje = re.search(datum_prve_izdaje_vzorec, blok) 
    if leto_izdaje:
        leto_izdaje = leto_izdaje['leto'] # dobimo slovar letnic
    else:
        leto_izdaje = re.search(datum_izdaje_vzorec, blok)['leto']
    niz_zanrov = re.search(zanri_vzorec, blok).groupdict()
    zanri = niz_zanrov['zanri'].replace('"', '').split(',')
    return strani, leto_izdaje, zanri[:5]



def izloci_zanre(knjige):
    zanri = []
    for knjiga in knjige:
        for zanr in knjiga.pop('zanri'):
            zanri.append({'knjiga': knjiga['id'], 'zanr': zanr})

    # zanri.sort(key=lambda zanr: (zanr['knjiga'], zanr['zanr']))
    return zanri


# def izpljuni_seznam_s_knjigo():
#     knjiga = {}
#     shrani_pomozno_datoteko(link_knjige)
#     strani, leto, zanri = poberi_podatke_s_strani()
#     knjiga['id'] = 1
#     knjiga['avtor'] = 'tvoja mami'
#     knjiga['naslov'] = 'lepo nam je'
#     knjiga['ocena'] = 5.0
#     knjiga['glasovi'] = 63176
#     knjiga['strani'] = int(strani)
#     knjiga['leto'] = int(leto)
#     knjiga['serija'] = False
#     knjiga['link'] = link_knjige
#     knjiga['zanri'] = zanri
#     del knjiga['link']
#     return knjiga



# knjige = []
# knjiga = izpljuni_seznam_s_knjigo()
# knjige.append(knjiga)
# print(knjige)
# zanri = izloci_zanre(knjige) 
# print(zanri)

# orodja.zapisi_csv(knjige, ['id', 'avtor', 'naslov', 'ocena', 'glasovi', 'strani', 'leto', 'serija'], 'obdelani-podatki\\pomozno_knjige.csv')

# orodja.zapisi_csv(zanri, ['knjiga', 'zanr'], 'obdelani-podatke\\pomozno_zanri.csv')
    
