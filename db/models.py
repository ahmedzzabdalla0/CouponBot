from sqlalchemy import Column, Integer, String, Text, ForeignKey, MetaData, Boolean, Date, DateTime, Float, Enum, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base, backref
from sqlalchemy import create_engine
from datetime import datetime
from enums import Gender, UserType
from sqlalchemy.ext.declarative import declared_attr


engine = create_engine('sqlite:///db/storeDB.db', echo=True)
Base = declarative_base()
meta = MetaData()


class Manager(Base):
    __tablename__ = 'Managers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False, unique=True)
    password = Column(String, nullable=False)
    permission = Column(String, nullable=False)
    login_records = relationship(
        'LoginRecord', primaryjoin="and_(foreign(LoginRecord.user_id) == Manager.id, foreign(LoginRecord.user_type) == 'manager')", back_populates='manager')


class Customer(Base):
    __tablename__ = 'Customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    permission = Column(String, nullable=False)
    expiration_date = Column(DateTime, nullable=True)
    visits = relationship('Visit', back_populates='customer')
    orders = relationship('Order', back_populates='customer')
    login_records = relationship(
        'LoginRecord', primaryjoin="and_(foreign(LoginRecord.user_id) == Customer.id, foreign(LoginRecord.user_type) == 'customer')", back_populates='customer', overlaps="login_records")


class Merchant(Base):
    __tablename__ = 'Merchants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    chat_id = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    password = Column(String, nullable=False)
    permission = Column(String, nullable=False)
    stores = relationship('Store', back_populates='merchant')
    login_records = relationship(
        'LoginRecord', primaryjoin="and_(foreign(LoginRecord.user_id) == Merchant.id, foreign(LoginRecord.user_type) == 'merchant')", back_populates='merchant', overlaps="login_records,login_records")


class LoginRecord(Base):
    __tablename__ = 'LoginRecords'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    last_login_date = Column(DateTime)

    @declared_attr
    def __mapper_args__(cls):
        return {
            'polymorphic_on': cls.user_type,
            'polymorphic_identity': 'LoginRecord'
        }

    customer = relationship(
        'Customer', primaryjoin="and_(foreign(LoginRecord.user_id) == Customer.id, LoginRecord.user_type == 'customer')", back_populates='login_records', overlaps="login_records,login_records")
    merchant = relationship(
        'Merchant', primaryjoin="and_(foreign(LoginRecord.user_id) == Merchant.id, LoginRecord.user_type == 'merchant')", back_populates='login_records', overlaps="customer,login_records,login_records")
    manager = relationship(
        'Manager', primaryjoin="and_(foreign(LoginRecord.user_id) == Manager.id, LoginRecord.user_type == 'manager')", back_populates='login_records', overlaps="customer,login_records,login_records,merchant")


class Category(Base):
    __tablename__ = 'Categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    stores = relationship('Store', back_populates='category')


class City(Base):
    __tablename__ = 'Cities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    neighborhoods = relationship('Neighborhood', back_populates='city')


class Neighborhood(Base):
    __tablename__ = 'Neighborhoods'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('Cities.id'), nullable=False)
    city = relationship('City', back_populates='neighborhoods')
    stores = relationship('Store', back_populates='neighborhood')


class Store(Base):
    __tablename__ = 'Stores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    location_url = Column(String)
    category_id = Column(Integer, ForeignKey('Categories.id'), nullable=False)
    neighborhood_id = Column(Integer, ForeignKey(
        'Neighborhoods.id'), nullable=False)
    store_id = Column(Integer, ForeignKey('Merchants.chat_id'), nullable=False)
    category = relationship('Category', back_populates='stores')
    neighborhood = relationship('Neighborhood', back_populates='stores')
    merchant = relationship('Merchant', back_populates='stores')
    offers = relationship('Offer', back_populates='store')

    visits = relationship('Visit', back_populates='store')


class Offer(Base):
    __tablename__ = 'Offers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    images_url = Column(Text, nullable=False)
    description = Column(String, nullable=False)
    price = Column(String, nullable=False)
    discount = Column(String, nullable=False)
    offer_number = Column(String, nullable=False)
    permission = Column(String, nullable=False)
    start_date = Column(Date, nullable=True)
    expiration_date = Column(Date, nullable=True)
    store_id = Column(Integer, ForeignKey('Stores.store_id'), nullable=False)
    store = relationship('Store', back_populates='offers')
    advertisements = relationship('Advertisement', back_populates='offer')
    orders = relationship('Order', back_populates='offer')
    visits = relationship('Visit', back_populates='offer')


class merchantOffer(Base):
    __tablename__ = 'merchantOffers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    images_url = Column(Text, nullable=False)
    description = Column(String, nullable=False)
    price = Column(String, nullable=False)
    discount = Column(String, nullable=False)
    offer_number = Column(String, nullable=False)
    permission = Column(String, nullable=False)
    agreed = Column(String, nullable=False)
    start_date = Column(Date, nullable=True)
    expiration_date = Column(Date, nullable=True)
    store_id = Column(Integer, nullable=False)


class Advertisement(Base):
    __tablename__ = 'Advertisements'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    permission = Column(String, nullable=False)
    offer_id = Column(Integer, ForeignKey(
        'Offers.offer_number'), nullable=False)
    offer = relationship('Offer', back_populates='advertisements')


class Link(Base):
    __tablename__ = 'Links'
    id = Column(Integer, primary_key=True, autoincrement=True)
    link_url = Column(String)
    link_id = Column(String)


class Order(Base):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('Offers.id'), nullable=False)
    chat_id = Column(Integer, ForeignKey('Customers.chat_id'), nullable=False)
    order_number = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    order_date = Column(DateTime, nullable=False)
    order_status = Column(String, nullable=False)
    offer = relationship('Offer', back_populates='orders')
    customer = relationship('Customer', back_populates='orders')


class Message(Base):
    __tablename__ = 'Messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)
    message_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    seen = Column(Boolean, default=False)
    sender_type = Column(String, nullable=False)
    receiver_type = Column(String, nullable=False)


class Visit(Base):
    __tablename__ = 'Visits'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('Customers.id'), nullable=False)
    store_id = Column(Integer, ForeignKey('Stores.id'), nullable=False)
    offer_id = Column(Integer, ForeignKey('Offers.id'), nullable=True)
    visit_date = Column(DateTime, nullable=False)
    customer = relationship('Customer', back_populates='visits')
    store = relationship('Store', back_populates='visits')
    offer = relationship('Offer', back_populates='visits')


# إنشاء الجداول
Base.metadata.create_all(engine)
