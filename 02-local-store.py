import os
import requests
from lxml import html
from pprint import pprint
from urlparse import urljoin
from hashlib import sha1


# A list of all deputies in the Argentinian Chamber
BASE_URL = 'http://www.diputados.gob.ar/diputados/listadip.html'

CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')


def _url_to_filename(url):
    """ Make a URL into a file name, using SHA1 hashes. """
    hash_file = sha1(url).hexdigest() + '.html'
    return os.path.join(CACHE_DIR, hash_file)


def store_local(url, content):
    """ Save a local copy of the file. """

    # If the cache directory does not exist, make one.
    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    # Save to disk.
    local_path = _url_to_filename(url)
    with open(local_path, 'wb') as fh:
        fh.write(content)


def load_local(url):
    """ Read a local copy of a URL. """
    local_path = _url_to_filename(url)
    if not os.path.exists(local_path):
        return None

    with open(local_path, 'rb') as fh:
        return fh.read()


def get_content(url):
    """ Wrap requests.get() """
    content = load_local(url)
    if content is None:
        response = requests.get(url)
        content = response.content
        store_local(url, content)
    return content


def scrape_deputies():
    """ Scrape all the deputies from the list """
    
    # Download the list or use the cache.
    content = get_content(BASE_URL)

    # Parse HTML
    document = html.fromstring(content)

    # Get all the links to deputy pages:
    for link in document.cssselect('table#tablesorter td a'):

        # Scrape each deputy's page.
        scrape_deputy(link.get('href'))


def scrape_deputy(link_part):
    """ Extract information from a deputy's page. """

    # Build the full URL for each deputy; download & parse it.
    url = urljoin(BASE_URL, link_part)
    content = get_content(url)
    document = html.fromstring(content)

    # Grab some elements with relevant info:
    box1 = document.cssselect(".info-diputados-principal1").pop()
    box2 = document.cssselect(".info-diputados-principal2").pop()

    # Extract the actual contents of some HTML elements:
    data = {
        'source_url': url,
        'name': box1.find('.//h2').text.strip(),
        'party': box2.find('.//h3').text.strip(),
        'email': box2.find('.//a').text.strip()
    }

    # Print it. 
    pprint(data)


if __name__ == '__main__':
    scrape_deputies()