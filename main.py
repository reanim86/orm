import json


import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

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

class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)

class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)

    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='stock')

class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)

    stock = relationship(Stock, backref='sale')

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def add_data():
    """
    Функция читает json файл и записывает данные из него в БД
    """
    with open('fixtures/tests_data.json') as f:
        data = json.load(f)
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record['pk'], **record['fields']))
    return

def get_shop(pub_name, pub_id='0'):
    """
    Функция выводит информацию о магазинах где имеется книга необходимого издателя
    :param pub_name: столбец name в таблице publisher
    :param pub_id: столбец id в таблице publisher
    :return:
    """
    id = int(pub_id)
    if len(pub_name) != 0:
        q = session.query(Shop).join(Stock, Stock.id_shop == Shop.id).join(Book, Book.id == Stock.id_book).\
            join(Publisher, Publisher.id == Book.id_publisher).filter(Publisher.name == pub_name)
        pb = session.query(Publisher).filter(Publisher.name == pub_name)
        for p in pb.all():
            print(f'Издатель "{p.name}" с id {p.id} продается в магазине(ах):')
            for s in q.all():
                print('\t', s.name)
    elif id != 0:
        q = session.query(Shop).join(Stock, Stock.id_shop == Shop.id).join(Book, Book.id == Stock.id_book). \
            join(Publisher, Publisher.id == Book.id_publisher).filter(Publisher.id == id)
        pb = session.query(Publisher).filter(Publisher.id == id)
        for p in pb.all():
            print(f'Издатель "{p.name}" с id {p.id} продается в магазине(ах):')
            for s in q.all():
                print('\t', s.name)
        return

if __name__ == '__main__':
    login = 'postgres'
    password = 'Tehn89tehn'
    base = 'db6'
    DSN = f'postgresql://{login}:{password}@localhost:5432/{base}'
    engine = sq.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    add_data()
    session.commit()

    name_book = input('Введите имя издателя, если Вам известен только id введите его в следующем окне: ')
    id_book = input('Введите id издателя: ')
    if len(name_book) != 0:
        get_shop(name_book)
    elif len(id_book) != 0:
        get_shop(name_book, id_book)
    else:
        print('Данные об издетеле не введены')






