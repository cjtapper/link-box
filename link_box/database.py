from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker

engine = None
session = None


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, onupdate=func.now())


Base = declarative_base(cls=Base)


class Article(Base):
    title = Column(String, nullable=False)
    source_url = Column(String, nullable=False)
    html = Column(String, nullable=False)


def init(app):
    global engine, session, Base
    engine = create_engine(get_connection_string(app), echo=True)
    session = scoped_session(
        sessionmaker(bind=engine, autocommit=False, autoflush=False)
    )
    Base.query = session.query_property()


def get_connection_string(app):
    return "sqlite:///" + app.config["DATABASE"]


def create():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init()
