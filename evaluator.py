from database import get_session, WgZimmer
import os


session = get_session()
zimmers = session.query(WgZimmer).filter(WgZimmer.interesting == None).all()

if len(zimmers) == 0:
    print("all rooms evaluated")

for zimmer in  zimmers:
    os.system("clear")
    if "Unbefristet" not in zimmer.date_to:
        continue

    print("\nWir sind:")
    print(zimmer.person_content)

    print("\nWir suchen:")
    print(zimmer.room_content)

    print("\nDas Zimmer ist:")
    print(zimmer.mate_content)

    print("\nQuartier:")
    print(zimmer.address_neighborhood)

    input = input("y/n: ")
    if input == "y":
        zimmer.interesting = "Y"
    else:
        zimmer.interesting = "N"
    session.commit()

