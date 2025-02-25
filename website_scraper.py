from scrape_utils import get_soup, get_selenium, get_soup_with_selenium
from regex_utils import is_email
from logs import log
from email.utils import parseaddr


def get_contact_page(get_as):
    links = {}
    for link in get_as:
        hyperlink = link.get('href')
        if 'contact' in hyperlink.lower():
            links['contact'] = hyperlink
        elif 'iletisim' in hyperlink.lower():
            links['iletisim'] = hyperlink
        elif 'communication' in hyperlink.lower():
            links['communication'] = hyperlink
        elif 'ulas' in hyperlink.lower():
            links['ulas'] = hyperlink
        elif 'job' in hyperlink.lower():
            links['job'] = hyperlink
        elif 'iş' in hyperlink.lower():
            links['iş'] = hyperlink
        elif 'support' in hyperlink.lower():
            links['support'] = hyperlink
        elif 'destek' in hyperlink.lower():
            links['destek'] = hyperlink
        elif 'sss' in hyperlink.lower():
            links['sss'] = hyperlink
        elif 'office' in hyperlink.lower():
            links['office'] = hyperlink
        elif 'ouroffices' in hyperlink.lower():
            links['offices'] = hyperlink    
        elif 'ofis' in hyperlink.lower():
            links['ofis'] = hyperlink

    if (links.__contains__('contact')):
        return links['contact']
    elif (links.__contains__('iletisim')):
        return links['iletisim']
    elif (links.__contains__('ulas')):
        return links['ulas']
    elif (links.__contains__('job')):
        return links['job']
    elif (links.__contains__('iş')):
        return links['iş']
    elif (links.__contains__('support')):
        return links['support']
    elif (links.__contains__('destek')):
        return links['destek']
    elif (links.__contains__('sss')):
        return links['sss']
    elif (links.__contains__('office')):
        return links['office']
    elif (links.__contains__('ofis')):
        return links['ofis']
    elif (links.__contains__('communication')):
        return links['communication']
    elif (links.__contains__('offices')):
        return links['offices']

def url_parser(url, base_url):
    new_url = []
    last_char = url[-1]
    base_url = base_url.split('//')[1]
    base_url = base_url.split('/')[1:]
    url = url.split('/')
    a = 0
    b = 0   
    url = list(filter(lambda a: a != '', url))
    base_url = list(filter(lambda a: a != '', base_url))

    while (a < len(url) and b < len(base_url)):
        if (url[a] == base_url[b]):
            a = a + 1
            b = b + 1
        else:
            break

    while (a < len(url)):
        new_url.append(url[a])
        new_url.append('/')
        a = a + 1

    print(new_url)

    if last_char == '/':
        last_string = ''.join(a for a in new_url)
    else:
        last_string = ''.join(a for a in new_url[:-1])
    return last_string


def url_checker(url, base_url):
    print(url, base_url)
    if url.startswith('http'):
        log(f'The page is {url}')
        return url
    else:
        parsed_url = url_parser(url, base_url)
        log(f'The page is {parsed_url}')
        if parsed_url.startswith('/') and base_url.endswith('/'):
            return base_url + parsed_url[1:]
        elif parsed_url.startswith('/') and not base_url.endswith('/'):
            return base_url + parsed_url
        elif not parsed_url.startswith('/') and base_url.endswith('/'):
            return base_url + parsed_url
        else:
            return base_url + '/' + parsed_url


def get_contact_url_soup(soup, base_url, a, driver):
    get_as = soup.find_all('a', href=True)

    contact_page = get_contact_page(get_as)

    if not contact_page:
        contact_page = base_url
        return get_soup(base_url)

    url_to_go = url_checker(contact_page, base_url)

    if a == 1:
        return get_soup_with_selenium(url_to_go, driver)
    else:
        return get_soup(url_to_go)


def get_email_from_soup(soup):

    get_as = soup.find_all('a', href=True)
    for link in get_as:
        mail = link.get('href')
        a = mail.split(':')
        if len(a) > 1 and is_email(a[1]):
            print(a[1])
            return a[1]

    get_ps = soup.find_all('p')
    for p in get_ps:
        mail = p.text
        if is_email(mail):
            return mail

    get_spans = soup.find_all('span')
    for span in get_spans:
        mail = span.text
        if is_email(mail):
            return mail

    result = soup.find_all(string=lambda text: "@" in text)

    for i in result:
        if is_email(i):
            return i

    result1 = soup.find_all(string=lambda text: "at" in text)

    for i in result1:
        if is_email(i):
            return i
    return 'Not Found'


def run_and_get_email(url):
    log('------------------------------------Scraping------------------------------------')
    print("Scraping: ", url)
    driver = get_selenium()
    web_page, new_url = None, None
    mail = 'Not Found'
    for a in range(2):
        if a == 1:
            print("Selenium is being used..")
            log("Selenium is being used..")
            web_page, new_url = get_soup_with_selenium(url, driver)
            if not web_page:
                print("Selenium didn't respond...")
                log("Selenium didn't respond...")
                continue
        else:
            print("Requests is being used..")
            log("Requests is being used..")
            web_page, new_url = get_soup(url)
            if not web_page:
                print("Requests didn't respond, trying selenium...")
                log("Requests didn't respond, trying selenium...")
                continue
        print(web_page.prettify())

        log(f'Page is {new_url}')    
        log('Looking for email in MAIN page')
        mail = get_email_from_soup(web_page)


        if mail == 'Not Found':
            log('Looking for email in CONTACT page')
            contact_page = get_contact_url_soup(web_page, new_url, a, driver)
            found = False

            if contact_page[0]:
                print("Contact page:", contact_page[1])
                log(f"Contact page: {contact_page[1]}")
                mail = get_email_from_soup(contact_page[0])
                if mail == 'Not Found':
                    continue
                else:
                    found = True
            if found:
                print(mail)
                print("Email found: ", mail)
                log(f"Email found in contact page: {mail} for: {url}\n")
                driver.quit()
                return mail, url
        else:
            print(mail)
            print("Email found: ", mail)
            log(f"Email found in main page: {mail} for: {url}\n")
            driver.quit()
            return mail, url

    log(f"Email not found for trying all possible scenarios for: {url}\n")
    print("Email not found for trying all possible scenarios for: ", url)

    driver.quit()

    return 'Not found', url