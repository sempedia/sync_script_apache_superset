from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Dataset(Base):
    __tablename__ = 'datasets'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Chart(Base):
    __tablename__ = 'chart'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Dashboard(Base):
    __tablename__ = 'dashboard'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
