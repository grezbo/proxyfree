__author__ = 'mork'
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Float, DateTime, create_engine

Base = declarative_base()


class Proxy(Base):

    __tablename__ = 'proxy'

    proxy_ip = Column(String(20), primary_key=True)
    proxy_port = Column(String(20))
    connection_type = Column(String(20))
    proxy_type = Column(String(20))
    proxy_country = Column(String(20))
    proxy_location = Column(String(20))
    connection_delay = Column(Float)
    validation_delay = Column(Float)
    validate_time = Column(DateTime)


    def print_proxy(self):
        print ''+self.proxy_ip+self.proxy_port



    #
    # def __init__(self, ip, port, type, anony='', country='',  location='', connection_delay=-1, validation_delay=-1, validate_time=''):
    #     self.ip = ip
    #     self.port = port
    #     self.type = type
    #     self.anony = anony
    #     self.country = country
    #     self.location = location
    #     self.connection_delay = connection_delay
    #     self.validation_delay = validation_delay
    #     self.validate_time = validate_time



