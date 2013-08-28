import requests
from lxml import html
from pprint import pprint
from urlparse import urljoin


# A list of all deputies in the Argentinian Chamber
BASE_URL = 'http://www.diputados.gob.ar/diputados/listadip.html'


def scrape_deputies():
    """ Scrape all the deputies from the list """
    
    # Download the list.
    response = requests.get(BASE_URL)

    # Parse HTML
    document = html.fromstring(response.content)

    # Get all the links to deputy pages:
    for link in document.cssselect('table#tablesorter td a'):

        # Scrape each deputy's page.
        scrape_deputy(link.get('href'))


def scrape_deputy(link_part):
    """ Extract information from a deputy's page. """

    # Build the full URL for each deputy; download & parse it.
    url = urljoin(BASE_URL, link_part)
    response = requests.get(url)
    document = html.fromstring(response.content)

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