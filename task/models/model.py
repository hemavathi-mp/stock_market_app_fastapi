import datetime

from sqlalchemy import Column, Text, Integer, String, DateTime, func, Boolean

from task.config.db import DB_BASE

# models
class Register(DB_BASE):
    __tablename__ = 'register'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, default=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    modified_on = Column(DateTime,onupdate=datetime.datetime.now)
    mobile_no = Column(String(255), nullable=False, default=False)
    password = Column(String(255), nullable=False, default=False)
    confirm_password = Column(String(255), nullable=False, default=False)
    address = Column(Text, nullable=True, default=None)

# total_sale is True if the product is sale otherwise False
# if we get profit the column should filled with string "profit" else "loss"
class Order(DB_BASE):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    stock = Column(Integer, nullable=False, default=100)
    price = Column(Integer, nullable=False,default=0)
    created_at = Column(DateTime, default=func.now())
    total_sale = Column(Integer, nullable=False, default=False)
    profit_loss = Column(String(255), nullable=False, default=False)
    total_product = Column(Integer, nullable=False, default=0)

