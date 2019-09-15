from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("sqlite:///:memory:", echo=True)
Session = scoped_session(sessionmaker(bind=engine))


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, onupdate=func.now())

    query = Session.query_property()


Base = declarative_base(cls=Base)


class Article(Base):
    title = Column(String, nullable=False)
    source_url = Column(String, nullable=False)
    html = Column(String, nullable=False)


def init():
    Base.metadata.create_all(engine)
