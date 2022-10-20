from database import get_session, WgZimmer


session = get_session()
not_rated = session.query(WgZimmer).filter(WgZimmer.interesting == None).count()
liked = session.query(WgZimmer).filter(WgZimmer.interesting == "Y").count()
final = session.query(WgZimmer).filter(WgZimmer.interesting == "final").count()
print("not rated: " + str(not_rated))
print("liked: " + str(liked))
print("final: " + str(final))