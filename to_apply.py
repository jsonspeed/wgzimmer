from database import get_session, WgZimmer
import os
import webbrowser

new = 2 # open in a new tab, if possible

session = get_session()
zimmers = session.query(WgZimmer).filter(WgZimmer.interesting == "final").all()
for zimmer in zimmers:
    os.system("clear")
    url = 'http://wgzimmer.ch/' + zimmer.link.encode("UTF-8")
    webbrowser.open(url, new=new)
