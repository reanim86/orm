import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='book')



def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

login = 'postgres'
password = 'Tehn89tehn'
base = 'db6'
DSN = f'postgresql://{login}:{password}@localhost:5432/{base}'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

