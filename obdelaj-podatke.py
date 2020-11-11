import re
import orodja

URL = 'https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1'
DIRECTORY = 'C:\\Users\\Taja\\Documents\\FMF\\2. letnik\\programiranje 1\\projektna naloga\\analiza-podatkov\\spletne-strani'

block_pattern = re.compile(
    r'<tr itemscope itemtype="http://schema.org/Book">.*?score:',
    flags=re.DOTALL    
)

book_pattern = re.compile(
    r'<a class="bookTitle" itemprop="url" href="(?P<link>.*)">.*?'
    r"<span itemprop='name' role='heading' aria-level='4'>(?P<naslov>.*?)</span>.*?"
    r'<a class="authorName" itemprop="url" href=".*"><span itemprop="name">(?P<avtor>.*?)<.*?'
    r'</span></span>(?P<ocena>.*) avg rating &mdash;(?P<glasovi>.*) ratings</span>',
    flags=re.DOTALL        
)

book_link_pattern = (
    r'<a class="bookTitle" itemprop="url" href="(?P<link>.*)">'    
)

title_pattern = (
    r"<span itemprop='name' role='heading' aria-level='4'>(?P<naslov>.*)</span>"    
)

author_pattern = (
    r'<a class="authorName" itemprop="url" href=".*"><span itemprop="name">(?P<avtor>.*?)<'
)

rating_pattern = (
    r'</span></span>(?P<ocena>.*) avg rating &mdash;(?P<glasovi>.*) ratings</span>'
)
slovar_idjev = {'id': 1}

def izloci_podatke_knjig(blok):
    data = re.search(book_pattern, blok)
    knjiga = data.groupdict()
    knjiga['ocena'] = float(knjiga['ocena'])
    glasovi_niz = knjiga['glasovi'].strip().replace(',', '')
    knjiga['glasovi'] = int(glasovi_niz)
    knjiga['link'] = knjiga['link'].strip()
    knjiga['naslov'] = knjiga['naslov'].strip()
    knjiga['avtor'] = knjiga['avtor'].strip()
    knjiga['id'] = slovar_idjev['id']
    slovar_idjev['id'] = slovar_idjev.get('id') + 1
    # dodala bom še if stavek, ki bo preveril,
    # ali je knjiga iz serije knjig.  
    return knjiga  


def knjige_na_strani(st_strani):
    with open(f'spletne-strani\\{st_strani}.html', 'r', encoding='utf-8') as f:
        vsebina = f.read()
        for blok in re.finditer(block_pattern, vsebina):
            yield izloci_podatke_knjig(blok.group(0)) 

knjige = []

for st_strani in range(1, 41):
    for knjiga in knjige_na_strani(st_strani):
      knjige.append(knjiga)
knjige.sort(key=lambda knjiga: knjiga['avtor'])
#orodja.zapisi_json(knjige, 'obdelani-podatki\\knjige.json')

orodja.zapisi_csv(knjige, ['id', 'avtor', 'naslov', 'link', 'ocena', 'glasovi'], 'obdelani-podatki\\knjige.csv')





