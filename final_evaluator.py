from database import get_session, WgZimmer
import os
import webbrowser

new = 2 # open in a new tab, if possible

session = get_session()
zimmers = session.query(WgZimmer).filter(WgZimmer.interesting == "Y").all()
for zimmer in zimmers:
    os.system("clear")
    url = 'http://wgzimmer.ch' + zimmer.link
    webbrowser.open(url, new=new)

    x = input("y/n: ")
    if x == "y":
        zimmer.interesting = "final"
    else:
        zimmer.interesting = "N"
    session.commit()

