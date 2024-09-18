import uuid
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
engine = create_engine("sqlite+pysqlite:///db.db", echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "order"
##    id: Mapped[int] = mapped_column(Sequence('id'),primary_key=True)
    id: Mapped[str] = mapped_column(String(36),primary_key=True)
    referenceNumId: Mapped[int] = mapped_column(ForeignKey('order.id'))
    referenceNum: Mapped["ReferenceNum"] = relationship(backref="reference_num")
##    referenceNum: Mapped["ReferenceNum"] = relationship(back_populates="order")
##    countryCode: Mapped["CountryCode"] = relationship(back_populates="order")    
##    countryCodeId: Mapped[int] = mapped_column(ForeignKey('order.id'))
##    addressId: Mapped[int] = mapped_column(ForeignKey('order.id'))
##    address: Mapped["Address"] = relationship(back_populates="order")    
##    customer: Mapped["Customer"] = relationship(back_populates="order")    
##    customerId: Mapped[int] = mapped_column(ForeignKey('order.id'))
##    orderLines: Mapped["OrderLines"] = relationship(back_populates="order")    
##    orderLinesId: Mapped[int] = mapped_column(ForeignKey('order.id'))

##    def __init__(
##            self,
##            referenceNum=None,
##            countryCode=None,
##            address=None,
##            customer=None,
##            orderLines=None
##        ):
##        self.referenceNum=referenceNum
##        self.countryCode=countryCode
##        self.address=address
##        self.customer=customer
##        self.orderLines=orderLines
##
##    @staticmethod
##    def consumeEnvelopeForListOfOrder(transactionRequest):
##        o = Order()
##        """
##        TransactionRequest has Orders
##        Orders have one or more Order
##        Order have ReferenceNum, CountryCode,Address,Customer OrderLines 
##        """
##        root = ET.fromstring(transactionRequest)
##        orders = []
##        for order in root[-1]:
##            o = Order()
##            o.referenceNum = ReferenceNum.consumeElementreeTag(o,order.find('ReferenceNum'))
####            orders.append(
####                    Order(
####                        ReferenceNum.consumeElementreeTag(order.find('ReferenceNum')),
####                        CountryCode.consumeElementreeTag(order.find('CountryCode')),
####                        Address.consumeElementreeTag(order.find('Address')),
####                        Customer.consumeElementreeTag(order.find('Customer')),
####                        OrderLines.consumeElementreeTag(order.find('OrderLines'))
####                        )
####                    )
##        return orders

class ReferenceNum(Base):
    __tablename__='reference_num'
##    id: Mapped[int] = mapped_column(Sequence('id'),primary_key=True)
    id: Mapped[str] = mapped_column(String(36),primary_key=True)
    orderId: Mapped[int] = mapped_column(ForeignKey("order.id"))
##    order: Mapped["Order"] = relationship(back_populates="order")
    order: Mapped["Order"] = relationship(backref="order")
    num: Mapped[str] = mapped_column(String(30))
    def __init__(self, order, num):
        self.order = order
        self.num = num
##    @staticmethod
##    def consumeElementreeTag(referenceNum):
##        return ReferenceNum(referenceNum.text)


##o = Order()
##o.id = str(uuid.uuid4())
##r = ReferenceNum(o,'o123141234')
##r.id = str(uuid.uuid4())
##r.orderId = o.id
##o.referenceNum=r;
##o.referenceNumId=r.id;
##Base.metadata.create_all(engine)
##print(o.id)
session = Session()
##session.add(o)
##session.commit()

from sqlalchemy import select
stmt = select(Order).where(Order.id == 'b6b75c3b-2441-47ab-9c44-3952b519123c')
result = session.execute(stmt)
for r in result:
    print(r)
    print(r[0].referenceNum.num)
##print(result)
