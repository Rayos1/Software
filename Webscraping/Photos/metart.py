from .. import CONNECTION, INSERT, SELECT, UPDATE
from ..utils import login, progress, save_image, get_hash, get_name, get_tags, generate_tags, bs4, re, requests, time

SITE = 'metarthunter'

def initialize(driver, url='/my-favorite-galleries/page/1/', query=0):
    
    def next_page(page):
             
        try: return page.contents[0].get('href')[28:]
        except IndexError: return False

    if not query:
        query = set(CONNECTION.execute(SELECT[0], (SITE,)), fetch=1)
    
    driver.get(f'https://www.{SITE}.com{url}')
    html = bs4.BeautifulSoup(driver.page_source, 'lxml')
    targets = html.find('ul', class_='gallery-a e')
    
    for target in targets.findAll(href=True, title=True, class_=False):
        
        page_source = requests.get(target.get('href')).content
        page = bs4.BeautifulSoup(page_source, 'lxml')
        artist = page.find(
            href=re.compile('.+/model/.+')
            ).text.lower().replace(' ', '_')

        hrefs = [
            (f' {artist} ', 0, image.get('href'), SITE) for image in 
            page.findAll('a', href=re.compile('https://f6j6u6m9.+'))
            if (image.get('href'),) not in query
            ]
        CONNECTION.execute(INSERT[3], hrefs, 1)
        
    next = next_page(html.find(class_='next'))
    if hrefs and next: initialize(driver, next, query)
    
    CONNECTION.commit()

def page_handler(driver, hrefs):

    if not hrefs: return
    size = len(hrefs)

    for num, (image, artist) in enumerate(hrefs):
        
        progress(size, num, SITE)

        name = get_name(image, 0, 1)
        save_image(name, image)
        tags, rating, exif = generate_tags(
            general=get_tags(driver, name), 
            custom=True, artists=artist, rating=True
            )
        if not save_image(name, image, exif): continue
        hash_ = get_hash(name) 
    
        CONNECTION.execute(UPDATE[3].replace('href', 'src'), (
            name, artist, tags, rating, image, hash_, image),
            commit=1
            )
    
    progress(size, size, SITE)

def setup(driver, initial=True):
    
    try:
        # login(driver, SITE)
        if initial: initialize(driver)
        page_handler(driver, CONNECTION.execute(SELECT[2].replace('href', 'src, artist'), (SITE,), fetch=1))
    except Exception as error: print(f'{SITE}: {error}')
    
    driver.close()