import os
import orodja
import requests

MAPA = 'C:\\Users\\Taja\\Documents\\FMF\\2. letnik\\programiranje 1\\projektna naloga\\analiza-podatkov\\spletne-strani'
STRANI = 40


for page in range(1, STRANI + 1):
    url = f'https://www.goodreads.com/list/show/1.Best_Books_Ever?page={page}'
    print(f'Zajemam: {url}')
    ime = str(page) + '.html'
    ime_mape = os.path.join(MAPA, ime)

    orodja.shrani_spletno_stran(url, ime_mape)





 