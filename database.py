from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:////Users/macbookair/repos/wgzimmer/wgzimmer.db")
Base = declarative_base()


class WgZimmer(Base):
    __tablename__ = 'wgzimmer'
    id = Column(Integer, primary_key=True)
    link = Column(String)
    person_content = Column(String)
    room_content = Column(String)
    mate_content = Column(String)
    date_from = Column(String)
    date_to = Column(String)
    cost = Column(String)
    address_region = Column(String)
    address_address = Column(String)
    address_city = Column(String)
    address_neighborhood = Column(String)
    address_close_to = Column(String)
    image1 = Column(String)
    image2 = Column(String)
    image3 = Column(String)
    interesting = Column(String)


Base.metadata.create_all(engine)

def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
