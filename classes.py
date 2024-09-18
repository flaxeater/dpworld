import sys
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
import uuid

engine = create_engine("sqlite+pysqlite:///database.db", echo=True)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Order(Base):
    ##ORM BOILERPLATE
    __tablename__ = "order"
    id: Mapped[str] = mapped_column(String(36),primary_key=True)
    referenceNumId: Mapped[int] = mapped_column(ForeignKey('order.id'))
    referenceNum: Mapped["ReferenceNum"] = relationship(backref="reference_num")
    countryCode: Mapped["CountryCode"] = relationship(backref="country_code")    
    countryCodeId: Mapped[str] = mapped_column(ForeignKey('order.id'))
    addressId: Mapped[str] = mapped_column(ForeignKey('order.id'))
    address: Mapped["Address"] = relationship(backref="address")    
    customer: Mapped["Customer"] = relationship(backref="customer")    
    customerId: Mapped[str] = mapped_column(ForeignKey('order.id'))
    orderLines: Mapped["OrderLines"] = relationship(backref="order_lines")    
    orderLinesId: Mapped[str] = mapped_column(ForeignKey('order.id'))

    def __init__(
            self,
            referenceNum=None,
            countryCode=None,
            address=None,
            customer=None,
            orderLines=None
        ):
        self.id = str(uuid.uuid4())
        self.referenceNum=referenceNum
        self.countryCode=countryCode
        self.address=address
        self.customer=customer
        self.orderLines=orderLines

    @staticmethod
    def consumeEnvelopeForListOfOrder(transactionRequest):
        o = Order()
        """
        TransactionRequest has Orders
        Orders have one or more Order
        Order have ReferenceNum, CountryCode,Address,Customer OrderLines 
        """
        root = ET.fromstring(transactionRequest)
        orders = []
        for order in root[-1]:
            # I would rather have done this in the constructor, but the order must exist
            # for the others to be properly instantiated.  
            o = Order()
            o.referenceNum = ReferenceNum.consumeElementreeTag(o,order.find('ReferenceNum'))
            o.countryCode = CountryCode.consumeElementreeTag(o, order.find('CountryCode'))
            o.address = Address.consumeElementreeTag(o, order.find('Address'))
            o.customer = Customer.consumeElementreeTag(o, order.find('Customer'))
            o.orderLines = OrderLines.consumeElementreeTag(o, order.find('OrderLines'))
            orders.append(o)
        return orders

class ReferenceNum(Base):
    ##ORM BOILERPLATE
    id: Mapped[str] = mapped_column(String(36),primary_key=True)
    orderId: Mapped[int] = mapped_column(ForeignKey("order.id"))
    order: Mapped["Order"] = relationship(backref="order")
    num: Mapped[str] = mapped_column(String(30),unique=True)
    __tablename__='reference_num'
    def __init__(self, order, num):
        self.id = str(uuid.uuid4())
        self.order = order
        self.order.referenceNumId = self.id
        self.orderId = order.id
        self.num = num
    @staticmethod
    def consumeElementreeTag(order, referenceNum):
        return ReferenceNum(order, referenceNum.text)
        ret = ReferenceNum(order, referenceNum.text)
        ret.orderId = order.id
        ret.order = order
        return ret

class CountryCode(Base):
    ##ORM BOILERPLATE
    __tablename__='country_code'
    id: Mapped[str] = mapped_column(String(36),primary_key=True)
    orderId: Mapped[int] = mapped_column(ForeignKey("order.id"))
    code: Mapped[str] = mapped_column(String(30))
    def __init__(self, order, code):
        self.id = str(uuid.uuid4())
        self.order = order
        self.order.countryCodeId = self.id
        self.orderId = order.id
        self.code = code
    @staticmethod
    def consumeElementreeTag(order, countryCode):
        return CountryCode(order, countryCode.text)

class Address(Base):
    ##ORM BOILERPLATE
    __tablename__='address'
    id: Mapped[str] = mapped_column(String(36),primary_key=True)
    orderId: Mapped[int] = mapped_column(ForeignKey("order.id"))
    fullName: Mapped[str] = mapped_column(String(30))
    addressType: Mapped[str] = mapped_column(String(30))
    addressLine1: Mapped[str] = mapped_column(String(30))
    addressLine2: Mapped[str] = mapped_column(String(30))
    def __init__(
            self,
            order,
            fullName,
            addressType,
            addressLine1,
            addressLine2
            ):
        self.id = str(uuid.uuid4())
        self.order = order
        self.order.addressId = self.id
        self.orderId = order.id
        self.fullName=fullName
        self.addressType=addressType
        self.addressLine1=addressLine1
        self.addressLine2=addressLine2
    @staticmethod
    def consumeElementreeTag(order, address):
        return Address(
            order,
            address.find('FullName').text,
            address.find('AddressType').text,
            address.find('AddressLine1').text,
            address.find('AddressLine2').text
        )

class Customer(Base):
    ##ORM BOILERPLATE
    __tablename__='customer'
    id: Mapped[str] = mapped_column(String(36),primary_key=True)
    orderId: Mapped[int] = mapped_column(ForeignKey("order.id"))
    customerCode: Mapped[str] = mapped_column(String(50))
    firstName: Mapped[str] = mapped_column(String(50))
    lastName: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))

    def __init__(self,order, customerCode,firstName,lastName,phone,email):
        self.id = str(uuid.uuid4())
        self.order = order
        self.order.customerId = self.id
        self.orderId = order.id
        self.customerCode=customerCode
        self.firstName=firstName
        self.lastName=lastName
        self.phone=phone
        self.email=email

    @staticmethod
    def consumeElementreeTag(order, customer):
        return Customer(
            order,
            customer.find('CustomerCode').text,
            customer.find('FirstName').text,
            customer.find('LastName').text,
            customer.find('Phone').text,
            customer.find('Email').text
        )

class OrderLines(Base):
    ##ORM BOILERPLATE
    __tablename__='order_lines'
    id: Mapped[str] = mapped_column(String(36),primary_key=True)
    orderId: Mapped[int] = mapped_column(ForeignKey("order.id"))
    orderLines: Mapped[List["OrderLine"]] = relationship(backref="order_line")
    def __init__(self, order, orderLines):
        self.id = str(uuid.uuid4())
        self.order = order
        self.order.orderLinesId = self.id
        self.orderId = order.id
        self.orderLines = orderLines;
        for line in orderLines:
            line.orderLinesId = self.id
    @staticmethod
    def consumeElementreeTag(order, orderLines):
        lines = []
        for c in orderLines:
            lines.append(OrderLine.consumeElementreeTag(c));
        return OrderLines(order, lines)

class OrderLine(Base):
    ##ORM BOILERPLATE
    __tablename__='order_line'
    id: Mapped[str] = mapped_column(String(36),primary_key=True)
    itemNum: Mapped[str] = mapped_column(String(30))
    itemDescription: Mapped[str] = mapped_column(String(30))
    orderLinesId: Mapped[int] = mapped_column(ForeignKey("order_lines.id"))
    def __init__(self,itemNum,itemDescription):
        self.id = str(uuid.uuid4())
        self.itemNum=itemNum
        self.itemDescription=itemDescription

    @staticmethod
    def consumeElementreeTag(line):
        return OrderLine(
            line.find('ItemNum').text,
            line.find('ItemDescription').text
        )
#Create Database, do nothing if it's there
##Base.metadata.create_all(engine)
