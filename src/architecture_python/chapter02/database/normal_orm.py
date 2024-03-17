from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Order(Base):
    id = Column(Integer, primmary_key=True)

class OrderLine(Base):
    id = Column(Integer, primmary_key=True)
    sku = Column(String(250))
    qty = Column(String(250))
    order_id = Column(Integer, ForeignKey('order.id'))
    order = relationship(Order)

class Allocation(Base):
    id = Column(Integer, primmary_key=True)
    orderline_id = Column(Integer, ForeignKey('order_lines.id'))
    batch_id = Column(Integer, ForeignKey('batches.id'))


# batches