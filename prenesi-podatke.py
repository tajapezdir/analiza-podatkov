import os
import orodja
import requests
import re

MAPA = 'C:\\Users\\Taja\\Documents\\FMF\\2. letnik\\programiranje 1\\projektna naloga\\analiza-podatkov\\spletne-strani'
KNJIGE_NA_STRAN = 100
STRANI = 40

block_pattern = re.compile(
    r'<tr itemscope itemtype="http://schema.org/Book">.*?score:',
    flags=re.DOTALL    
)

for page in range(1, STRANI + 1):
    url = f'https://www.goodreads.com/list/show/1.Best_Books_Ever?page={page}'
    print(f'Zajemam: {url}')
    start = (page - 1) * KNJIGE_NA_STRAN + 1
    end = page * KNJIGE_NA_STRAN
    ime_datoteke = f'knjige-od-{start}-do-{end}.html'
    datoteka = os.path.join(MAPA, ime_datoteke)
    orodja.shrani_spletno_stran(url, datoteka)
    vsebina = orodja.vsebina_datoteke(datoteka)







 