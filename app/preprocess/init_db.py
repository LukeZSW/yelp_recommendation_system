# -*- coding: UTF-8 -*-
# init database

from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50))


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    address = Column(String(150))
    latitude = Column(Float)
    longitude = Column(Float)
    postal_code = Column(String(50))
    categories = Column(String(150))
    stars = Column(Float)
    city = Column(String(50))
    state = Column(String(50))


if __name__ == '__main__':
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    current_parent_path = os.path.dirname(current_dir_path)
    res_dir = os.path.join(current_parent_path, 'res')
    item_file = os.path.join(res_dir, 'item.json')
    engine = create_engine('sqlite:///' + current_parent_path + '/data.db?check_same_thread=False')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    for i in range(6722):
        user = User(id=i, username=str(i), password=generate_password_hash(str(i), method='sha256'))
        session.add(user)
    df_item = pd.read_json(item_file, encoding='utf-8')
    columns = ['address', 'categories', 'city', 'latitude', 'longitude', 'name', 'postal_code', 'stars', 'state', 'itemorder']
    df_item = df_item[columns]
    for i in range(len(df_item)):
        item = Item(id=int(df_item.iloc[i]['itemorder']),
                    name=str(df_item.iloc[i]['name']),
                    address=str(df_item.iloc[i]['address']),
                    latitude=df_item.iloc[i]['latitude'],
                    longitude=df_item.iloc[i]['longitude'],
                    postal_code=str(df_item.iloc[i]['postal_code']),
                    categories=str(df_item.iloc[i]['categories']),
                    stars=df_item.iloc[i]['stars'],
                    city=str(df_item.iloc[i]['city']),
                    state=str(df_item.iloc[i]['state']))
        session.add(item)
    session.commit()

