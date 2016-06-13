from lxml import html
import requests
import logging
import sys
import httplib as http_client
from database import get_session, WgZimmer
from sqlalchemy.orm.exc import NoResultFound
from requests.exceptions import ConnectionError


def enable_debugging():
    http_client.HTTPConnection.debuglevel = 1
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def get_links():

    payload = {
        "query": "",
        "priceMin": "50",
        "priceMax": "1500",
        "state": "bern",
        "permanent": "true",
        "student": "none",
        "country": "ch",
        "orderBy": "MetaData/@mgnl:lastmodified",
        "orderDir": "descending",
        "startSearchMate": "true",
        "wgStartSearch": "true"
    }

    try:
        page = requests.post("http://www.wgzimmer.ch/wgzimmer/search/mate.html?", data=payload)
    except ConnectionError:
        print "No internet connection"
        sys.exit(1)

    tree = html.fromstring(page.content)
    links = tree.xpath("""//*[@id="content"]/ul/li/a[2]/@href""")
    return links 


def save_new_zimmer(link, session):

    wg_zimmer_page = requests.get('http://wgzimmer.ch/' + link)
    wg_zimmer_tree = html.fromstring(wg_zimmer_page.content)

    zimmer = WgZimmer(link=link)

    zimmer.person_content = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[3]/div[contains(@class, 'person-content')]/p)""")

    zimmer.room_content = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[3]/div[contains(@class, 'room-content')]/p)""")

    zimmer.mate_content = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[3]/div[contains(@class, 'mate-content')]/p)""")

    zimmer.date_from = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[3]/div[contains(@class, 'date-cost')]/p[1])""")

    zimmer.date_to = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[3]/div[contains(@class, 'date-cost')]/p[2])""")

    zimmer.cost = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[3]/div[contains(@class, 'date-cost')]/p[3])""")

    zimmer.address_region = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[3]/div[contains(@class, 'adress-region')]/p[1])""")

    zimmer.address_address = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[3]/div[contains(@class, 'adress-region')]/p[2])""")

    zimmer.address_city = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[3]/div[contains(@class, 'adress-region')]/p[3])""")

    zimmer.address_neighborhood = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[3]/div[contains(@class, 'adress-region')]/p[4])""")

    zimmer.address_close_to = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[3]/div[contains(@class, 'adress-region')]/p[5])""")

    zimmer.image1 = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[3]/div[contains(@class, 'image-content')]/div/a[1]/@href)""")

    zimmer.image2 = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[3]/div[contains(@class, 'image-content')]/div/a[2]/@href)""")

    zimmer.image3 = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[3]/div[contains(@class, 'image-content')]/div/a[3]/@href)""")

    session.add(zimmer)
    session.commit()


def scrape():
    session = get_session()
    new_zimmers = 0
    for link in get_links():
        try:
            session.query(WgZimmer).filter(WgZimmer.link == link).one()
        except NoResultFound:
            new_zimmers += 1
            save_new_zimmer(link, session)

    print str(new_zimmers) + " new rooms found"


if __name__ == "__main__":
    logging.basicConfig()
    #enable_debugging()
    scrape()

