import requests
from lxml import html
from pprint import pprint
from urlparse import urljoin


BASE_URL = "http://www.csjn.gov.ar/jurisp/jsp/sumarios.do?usecase=goConsultaJurisprudencia&internet=N"
LISTING = "http://www.csjn.gov.ar/jurisp/jsp/nomenclador.do?usecase=getNomencladoresArbolFull&origen=titulo"


def get_titles(session):
    """ Get all the titles from the web pop-up. """

    # This requires a valid session. 
    response = session.get(LISTING)
    document = html.fromstring(response.content)
    for link in document.cssselect('a'):
        if link.get('onclick') is not None:
            # de-compose some JavaScript :) 
            _, _, _, title_id, _, title, _ = link.get('onclick').split("'")
            yield title_id, title


def scrape_verdicts():
    """ Scrape verdict summaries. """

    # Make a session for storing HTTP cookies.
    session = requests.Session()

    # Get the cookie to make a valid session.
    response = session.get(BASE_URL)

    for title_id, title in get_titles(session):

        # Fake the search form:
        form_data = {
            "cantInicial": -1,
            "cantFinal": 100,
            "txtTitulo": title,
            "cs1987": "cs1987",
            "operadorCampos": "todas",
            "tituloNodoId": title_id
        }
        url = urljoin(BASE_URL, 'BuscadorSumarios')
        response = session.post(url, data=form_data)
        document = html.fromstring(response.content)

        for link in document.cssselect('.txt-m a'):
            # Get all the links to summary pages.
            if 'openSumario' in link.get('href'):
                case_id = link.get('href').split('(')[-1].split(',')[0]
                scrape_verdict(case_id)


def scrape_verdict(case_id):
    # Look ma, no code!
    print case_id


if __name__ == '__main__':
    scrape_verdicts()