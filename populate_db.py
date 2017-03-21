#!/usr/bin/env/python


'''
	POPULATE OUR CATALOG/ONLINE SHOP:
	1). Data is initialized with inputs in the initData file (imported)
        2). User information is inialized/populated independently from the
            initData.users dictionary
        3). Categories, subcategories, and brands tables are populated by
            looping through the initData.instruments dictionary.
            a). Categories and brands tables are populated independently.
            b). Subcategories are populated only after categories have been
                populated as the category forms a foreign-key constraint
                in the subcategory table.
	4). Finally, we populate the instrument table with detail in the
            initData.instruments dict, retrieving the id values for foreign
            keys category, subcategory, and user_id as rendered by populating
            these tables first in step 3 above.
'''

import initData

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import Base, User, Category, Subcategory, Brand, Instrument

# ---sqlite-driven db
engine = create_engine('sqlite:///instrumentgarage.db')

#  ---bind our Base class data definitions to our db engine 
Base.metadata.bind = engine

# ---establish a session (conn window) with our database for data exchange
DBSession = sessionmaker(bind=engine)
session = DBSession()



# =============================================================================

def popUsers():
    print "Populating users..."
    for user in initData.users:
	addUser = User(  name=initData.users[user]['name']
                       , email=initData.users[user]['email'])
        session.add(addUser)
        session.commit()
    print "...done"

# =============================================================================


# =============================================================================

def popCategories():
    print "Populating categories..."
    cats  = []
    for instr in initData.instruments:
        cats.append(initData.instruments[instr]['cat'])
    categories = set(cats)

    for cat in categories:
        addCat = Category(name=cat)
        session.add(addCat)
        session.commit()
    print "...done"

# =============================================================================


# =============================================================================

def popSubCategories():
    print "Populating subcategories..."
    subcats  = []
    for instr in initData.instruments:
        subcats.append( initData.instruments[instr]['cat'] + '_' 
                       + initData.instruments[instr]['subcat'])
    subcategories = set(subcats)

    for subcat in subcategories:
        parts = subcat.split('_')
        category= session.query(Category).filter_by(name=parts[0]).one()
        addSubCat = Subcategory(name=parts[1],category_id=category.id)
        session.add(addSubCat)
        session.commit()
    print "...done"

# =============================================================================


# =============================================================================
def popBrands():
    print "Populating brands..."
    allbrands = []
    for instr in initData.instruments:
        allbrands.append(initData.instruments[instr]['brand'])
    brands = set(allbrands)

    for br in brands:
        addBrand = Brand(name=br)
        session.add(addBrand)
        session.commit() 
    print "...done"

# =============================================================================


# =============================================================================

def popInstruments():
    print "Populating instruments..."
    for instr in initData.instruments:
        category = session.query(Category).filter_by(
                      name=initData.instruments[instr]['cat']).one()
        subcategory = session.query(Subcategory).filter_by(
                         name=initData.instruments[instr]['subcat']).one()
        brand = session.query(Brand).filter_by(
                   name=initData.instruments[instr]['brand']).one()

        addInstr = Instrument(   
                                  category_id = category.id
                                , subcategory_id = subcategory.id
                                , brand_id = brand.id
                                , model = initData.instruments[instr]['model']
                                , condition = initData.instruments[instr]['condition']
                                , description = initData.instruments[instr]['description']
                                , picture = initData.instruments[instr]['picture']
                                , price = initData.instruments[instr]['price']
                                , user_id = initData.instruments[instr]['user_id']
			      )
        session.add(addInstr)
        session.commit()
    print "...done"

# =============================================================================




if __name__ == '__main__':
   popUsers()
   popCategories()
   popBrands()
   popSubCategories()
   popInstruments()

print "Catalog successfully populated."


