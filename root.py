import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import requests
import json
import pandas as pd
import math
import sys
import inspect
from abc import ABC, abstractmethod
import time
import os

Base = declarative_base()

# class being a parrent of all data classes in api_one


class datac(ABC):
    def __init__(self):
        pass

# class being a parrent of all modules in api_one


class adapterc(ABC):

    def __init__(self, engine, session):
        self.session = session
        self.engine = engine

    @abstractmethod
    def check_api(self):
        pass

    @abstractmethod
    def get(self):
        return 0

    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def api_view(self):
        pass

    # this is to report history of actions
    def report(self):
        query = self.session.query(logs).filter(logs.adapter == self.adapter)
        df = pd.read_sql(query.statement, self.engine)
        return df


class logs(Base):
    __tablename__ = '_logs'
    id = Column(Integer, primary_key=True)
    adapter = Column(String)
    action = Column(String)
    status = Column(String)
    comment = Column(String)
    rowdate = Column(DateTime)

    def __init__(self, adapter, action, status, comment=''):
        self.adapter = adapter
        self.action = action
        self.status = status
        self.comment = comment
        self.rowdate = datetime.datetime.now()


class cities(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    district = Column(String)
    voivodeship = Column(String)
    population = Column(Integer)
    owm_id = Column(Integer)

    def __init__(self, name, category, district, voivodeship, population):
        self.name = name
        self.category = category
        self.district = district
        self.voivodeship = voivodeship
        self.population = population
