#!/usr/bin/env/python

import os
import sys


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
   __tablename__ = 'user'

   id = Column(Integer, primary_key=True)
   name = Column(String(250), nullable=False)
   email = Column(String(250))
   picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
                    'id'   : self.id
                  , 'name' : self.name
               }


class Subcategory(Base):
    __tablename__ = 'subcategory'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        return {
                    'id'          : self.id
                  , 'name'        : self.name
                  , 'category_id' : self.category_id
               }

class Brand(Base):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True)
    name = Column(String(250),nullable=False)

    @property
    def serialize(self):
        return {
                    'id'   : self.id
                  , 'name' : self.name
               }


class Instrument(Base):
    __tablename__ = 'instrument'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    subcategory_id = Column(Integer,ForeignKey('subcategory.id'))
    subcategory = relationship(Subcategory)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    brand = relationship(Brand)
    model = Column(String(250))
    condition = Column(String(20), nullable=False)
    description = Column(String(250))
    picture = Column(String(250))
    price = Column(String(10))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
                    'id'             :  self.id
                  , 'category_id'    :  self.category_id
                  , 'subcategory_id' :  self.subcategory_id
                  , 'brand_id'       :  self.brand_id
                  , 'model'          :  self.model
                  , 'condition'      :  self.condition
                  , 'description'    :  self.description
                  , 'picture'        :  self.picture
                  , 'price'          :  self.price 
                  , 'user_id'        :  self.user_id
               }


engine = create_engine('sqlite:///instrumentgarage.db')


Base.metadata.create_all(engine)
