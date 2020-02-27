from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class SellRequest(Base):
    """ A Request for selling an item """

    __tablename__ = "sell_request"

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(250), nullable=False)
    seller_id = Column(String(250), nullable=False)
    item_id = Column(String(250), nullable=False)
    item_name = Column(String(250), nullable=False)
    time_stamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, customer_id, seller_id, item_id, item_name, time_stamp):
        """ Initializes a request for selling an item """
        self.customer_id = customer_id
        self.seller_id = seller_id
        self.item_id= item_id
        self.item_name = item_name
        self.time_stamp = time_stamp
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a selling request """
        dict = {}
        dict['id'] = self.id
        dict['customer_id'] = self.customer_id
        dict['seller_id'] = self.seller_id
        dict['item_id'] = self.item_id
        dict['item_name'] = self.item_name
        dict['time_stamp'] = self.time_stamp
        dict['data_created'] = self.date_created
        return dict
