from lxml import html
import requests
import logging
import sys
import http.client as http_client
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
        "priceMin": "200",
        "priceMax": "800",
        "state": "zurich-stadt",
        "permanent": "all",
        "student": "none",
        "typeofwg": "all",
        "orderBy": "@sortDate",
        "orderDir": "descending",
        "startSearchMate": "true",
        "wgStartSearch": "true",
        "start": "0"
    }

    try:
        page = requests.post("https://www.wgzimmer.ch/wgzimmer/search/mate.html?", data=payload)
    except ConnectionError:
        print("No internet connection")
        sys.exit(1)

    tree = html.fromstring(page.content)
    links = tree.xpath("""//*[@id="content"]/ul/li/a[2]/@href""")
    return links


def save_new_zimmer(link, session):

    wg_zimmer_page = requests.get('http://wgzimmer.ch' + link)
    wg_zimmer_tree = html.fromstring(wg_zimmer_page.content)

    zimmer = WgZimmer(link=link)

    zimmer.person_content = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[5]/div[contains(@class, 'person-content')]/p)""")

    zimmer.room_content = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[5]/div[contains(@class, 'room-content')]/p)""")

    zimmer.mate_content = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[5]/div[contains(@class, 'mate-content')]/p)""")

    zimmer.date_from = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[5]/div[contains(@class, 'date-cost')]/p[1])""")

    zimmer.date_to = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[5]/div[contains(@class, 'date-cost')]/p[2])""")

    zimmer.cost = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[5]/div[contains(@class, 'date-cost')]/p[3])""")

    zimmer.address_region = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[5]/div[contains(@class, 'adress-region')]/p[1])""")

    zimmer.address_address = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[5]/div[contains(@class, 'adress-region')]/p[2])""")

    zimmer.address_city = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[5]/div[contains(@class, 'adress-region')]/p[3])""")

    zimmer.address_neighborhood = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[5]/div[contains(@class, 'adress-region')]/p[4])""")

    zimmer.address_close_to = wg_zimmer_tree.xpath(
	"""string(//*[@id="content"]/div[5]/div[contains(@class, 'adress-region')]/p[5])""")

    images = wg_zimmer_tree.xpath("""//*[@id="content"]/div[5]/div[contains(@class, 'image-content')][2]/div/div/a""")

    images_dict = {0: "", 1: "", 2: ""}

    for n, i in enumerate(images):
        
        im_id = i.values()[0].split('_')[-1]
        images_dict[n] = "https://img.wgzimmer.ch/.imaging/wgzimmer_shadowbox-jpg/dam/" + im_id + "/temp.jpg"
        
    zimmer.image1 = images_dict[0]
    zimmer.image2 = images_dict[1]
    zimmer.image3 = images_dict[2]

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


    print(str(new_zimmers) + " new rooms found")


if __name__ == "__main__":
    logging.basicConfig()
    #enable_debugging()
    scrape()
