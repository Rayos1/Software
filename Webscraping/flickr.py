from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException, NoSuchElementException

SITE = 'flickr'

def initialize(driver, url='/photos/140284163@N04/favorites/page1', query=0):
    
    def next_page(page):
             
        try: return page.get('href')[:-1]
        except IndexError: return False

    if not query:
        CURSOR.execute(SELECT[0], (SITE,))
        query = set(CURSOR.fetchall())
    driver.get(f'https://www.flickr.com{url}')
    for _ in range(2):
        driver.find_element_by_tag_name('html').send_keys(Keys.END)
        time.sleep(2)

    html = bs4.BeautifulSoup(driver.page_source, 'lxml')
    hrefs = [
        (target.get('href'), 0, SITE) for target in 
        html.findAll('a', class_='overlay', href=True)
        if (target.get('href'),) not in query
        ]
    execute(INSERT[0], hrefs, 1)
        
    next = next_page(html.find('a', {'data-track':'paginationRightClick'}))
    if hrefs and next: initialize(driver, next, query)

    DATAB.commit()
    
def page_handler(driver, hrefs):

    if not hrefs: return
    size = len(hrefs)
    view = 'view.photo-notes-scrappy-view'
    target = 'view.photo-well-scrappy-view.requiredToShowOnServer'

    for num, (href,) in enumerate(hrefs):
        
        progress(size, num, SITE)
        driver.get(f'https://www.flickr.com{href}')
        
        for _ in range(25):
            try:
                element = driver.find_element_by_class_name(view)
                ActionChains(driver).move_to_element(element).perform()
                driver.find_element_by_class_name(target).click()

            except ElementClickInterceptedException:
                image = driver.find_element_by_class_name(
                    'zoom-large').get_attribute('src')
                break

            except NoSuchElementException:
                try:
                    image = driver.find_element_by_xpath(
                        '//*[@id="video_1_html5_api"]'
                        ).get_attribute('src')
                    break

                except:
                    image = None
                    try:
                        status = driver.find_element_by_class_name('statusCode')
                        if status.text == '404':
                            execute(UPDATE[3], (
                                f'404 - {href}', None, None, 1, None, None, 0, href),
                                commit=1
                                )
                    except: pass
                    break
        
        if image is None: continue
        name = get_name(image, 0, 1)
        save_image(name, image)
        tags = get_tags(driver, name)
        tags, rating, exif = generate_tags(
            general=tags, custom=True, rating=True, exif=True
            )
        if name.endswith(('jpg', 'jpeg')): save_image(name, image, exif)
        hash_ = get_hash(name) 
        
        try:
            execute(UPDATE[3], (
                name, ' ', tags, rating, image, hash_, 0, href),
                commit=1
                )
        except sql.errors.IntegrityError:
            execute(UPDATE[3], (
                f'202 - {href}', ' ', tags, rating, image, hash_, 0, href),
                commit=1
                )
        except (sql.errors.OperationalError, sql.errors.DatabaseError): continue
    
    progress(size, size, SITE)

def setup(initial=True):
    
    try:
        driver = get_driver(headless=True)
        login(driver, SITE)
        if initial: initialize(driver)
        CURSOR.execute(SELECT[2],(SITE,))
        page_handler(driver, CURSOR.fetchall())
    except WebDriverException:
        user = input(f'\n{SITE}: Browser closed\nContinue? ')
        if user.lower() in 'yes': setup(False)
    except Exception as error: print(f'{SITE}: {error}')
        
    try: driver.close()
    except: pass

if __name__ == '__main__':
    
    from utils import *
    setup()

else: from .utils import *