#!/usr/bin/python


from flask import Flask, flash, jsonify, redirect, render_template
from flask import request, url_for, make_response
from flask import session as login_session
from sqlalchemy import asc, create_engine, func
from sqlalchemy.orm import sessionmaker
from create_db import Base, User, Category, Subcategory, Brand, Instrument

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import random
import string
import httplib2
import json
import requests


app = Flask(__name__)

engine = create_engine('sqlite:///instrumentgarage.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine, autoflush=True)
session = DBSession()


# === AUTHORIZATION & AUTHENTICATION: 3RD PARTY OAUTH 2.0 =====================

'''
   Google authentication protocol is derived mainly from demonstrated
   examples. The following modifications were made for functionality:
   1). The credentials object appears to render malformed/incorrectly using
       current Google procedures.  As a result, the logout process was modified
       to reference the access_token directly (which emulates behavior in the
       original).
   2). Sample log-in protocol is dependent on a username but at least some
       Google accounts credentials were observed not to return these in which
       case the gmail address is substituted.
   3). The session object must be cleared directly for logouts to effectuate.
       This deletes cookies and approximates clearing the cache.
'''

# ---oauth Google application credentials
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Sample Project"


'''
   Create anti-forgery state token (random string).
   Prevents unauthorized commands transmitted from a trusted 'user'
'''


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # ---validate state token to prevent CSRF/XSRF attacks
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # ---get the authorization code
    code = request.data

    try:
        # ---form credentials object from authorization code
        '''
           Note: unclear if this works
        '''
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # ---check token validity
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # ---terminate if errors in the access token data
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # ---force verification of access token with user profile
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # ---validate access token is okay for current application
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is \
                                             already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # ---create access token storage
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # ---fetch user profile information
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # ---specify 3rd party in login_session object
    '''
       Note: it would be preferable to build a module with dedicated
       functions per provider and execute logins/logouts with
       vendor-specific methods/attributes.  i

       Thus:

       login_session['Google']['client_id']
       login_session['Google']['access_token']

       and so on.
    '''
    login_session['provider'] = 'google'

    # ---this was observed on at least one occasion (blank returned for 'name')
    if not login_session['username']:
        login_session['username'] = data['email']

    # ---fallback if credentials object does not form properly
    if credentials not in login_session:
        login_session['credentials'] = credentials.access_token

    # ---add user if not in database already
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;"'
    output += ' "-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    return output

# ---logout/disconnect: revoke user's access_token and reset login_session


@app.route('/logout')
def logout():
    if login_session['provider'] == 'google':
        return gdisconnect(login_session)


@app.route('/gdisconnect')
def gdisconnect(login_session):
    # ---check user is connected
    '''
       Note we set login_session.credentials to access_token itself
    '''
    access_token = login_session.get('credentials')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # ---user token is deemed invalid
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    # ---if we're here, then we've revoked the token
    '''
       Go ahead and clear the session, too
    '''
    login_session.clear()
    flash("Successfully logged out.")
    return redirect(url_for('showMain'))

# =============================================================================


# === USER DATABASE UTILITY FUNCTIONS =========================================

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# =============================================================================


# === NAVIGATION ==============================================================

# ---landing: show summary inventory by category
@app.route('/')
@app.route('/thegarage')
def showMain():

    query = "SELECT cat.id, cat.name, COUNT(inst.id) AS total "
    query += "FROM category cat JOIN instrument inst ON "
    query += "cat.id = inst.category_id GROUP BY cat.id, cat.name "
    query += "ORDER BY cat.name"
    totals = session.execute(query)

    menu_heading = "Current Inventory by Category:"
    if 'username' in login_session:
        return render_template('main.html', menu_heading=menu_heading,
                               totals=totals,
                               username=login_session['username'])
    else:
        return render_template('public_main.html', menu_heading=menu_heading,
                               totals=totals)

# ---show inventory by brand name


@app.route('/bybrand')
def showByBrand():
    query = "SELECT brd2.id, sub.* FROM brand brd2 JOIN "
    query += "( SELECT brd.name, COUNT(instr.brand_id) "
    query += "FROM brand brd JOIN instrument instr ON "
    query += "brd.id = instr.brand_id GROUP BY brd.name ) AS sub "
    query += "ON brd2.name = sub.name ORDER BY sub.name"
    totals = session.execute(query)

    menu_heading = "Current Inventory by Brand:"
    if 'username' in login_session:
        return render_template('showByBrand.html', menu_heading=menu_heading,
                               totals=totals,
                               username=login_session['username'])
    else:
        return render_template('public_showByBrand.html',
                               menu_heading=menu_heading, totals=totals)


@app.route('/bycategory')
def showByCategory():
    return redirect(url_for('showMain'))


@app.route('/category/<int:category_id>')
def showCategory(category_id):
    # ---using sqlalchemy's built-in query object model as alternative here
    catInv = session.query(Category.name, Subcategory.name, Instrument.id,
                           Brand.name, Instrument.model, Instrument.condition
                           ).filter_by(id=category_id).join(Subcategory) \
                          .join(Instrument).join(Brand) \
                          .order_by(Subcategory.name)

    heading = session.query(Category).filter_by(id=category_id).one()

    if 'username' in login_session:
        return render_template('category.html',
                               menu_heading=heading.name.capitalize(),
                               username=login_session['username'],
                               stock=catInv)
    else:
        return render_template('public_category.html',
                               menu_heading=heading.name.capitalize(),
                               stock=catInv)


@app.route('/brand/<int:brand_id>')
def showBrand(brand_id):
    brandInv = session.query(Brand.name, Subcategory.name, Instrument.id,
                             Instrument.model, Instrument.condition
                             ).filter_by(id=brand_id).join(Instrument) \
                            .join(Subcategory)
    heading = session.query(Brand).filter_by(id=brand_id).one()

    if 'username' in login_session:
        return render_template('brand.html',
                               menu_heading=heading.name.capitalize(),
                               username=login_session['username'],
                               stock=brandInv)

    else:
        return render_template('public_brand.html',
                               menu_heading=heading.name.capitalize(),
                               stock=brandInv)


@app.route('/<int:instrument_id>')
def instrument(instrument_id):
    instData = session.query(Instrument.model, Instrument.condition,
                             Instrument.description, Instrument.price,
                             Subcategory.name, Brand.name, User.name
                             ).filter_by(id=instrument_id).join(Subcategory) \
                            .join(Brand).join(User)

    heading = "Viewing: " + instData[0][5].capitalize() + ' ' \
        + instData[0][0].capitalize() + ' ' + instData[0][4].capitalize()

    if 'username' in login_session:
        return render_template('instrument.html', menu_heading=heading,
                               username=login_session['username'],
                               instrument_id=instrument_id, info=instData)
    else:
        return render_template('public_instrument.html',
                               instrument_id=instrument_id, info=instData)


def setCategory(newItem):

    # ---add/edit: set item category
    newItem.catError = 0
    newItem.catErrorMsg = ""

    if request.form['category_custom']:
        newItem.category_custom = request.form['category_custom']
        if request.form['selected_category'] != '-1':
            newItem.catError += 1
            newItem.catErrorMsg += "Ambiguous category: select existing \
                              or add a new one (not both). "
            newItem.selected_cat_id = request.form['selected_category']
            newItem.selected_cat = session.query(Category)\
                .filter_by(id=newItem.selected_cat_id).one()
            newItem.selected_cat = newItem.selected_cat.name
        else:
            newItem.selected_cat_id = -1
            newItem.selected_cat = "Category:"
            # ---check to see if attempting to add category already in db
            cat_in_db = session.query(Category)\
                .filter_by(name=newItem.category_custom).first()
            if cat_in_db is not None:
                newItem.catError += 1
                newItem.catErrorMsg += "Category already exists! "
    else:
        newItem.category_custom = ""
        if request.form['selected_category'] == '-1':
            newItem.catError += 1
            newItem.catErrorMsg = "Category required. "
        else:
            newItem.category_id = request.form['selected_category']
            newItem.selected_cat_id = newItem.category_id
            newItem.selected_cat = session.query(Category).\
                filter_by(id=newItem.selected_cat_id).one()
            newItem.selected_cat = newItem.selected_cat.name
            newItem.resetMsg = "(RESET FORM: for all categories)"

    if newItem.catError:
        newItem.selected_cat = "Category:"
        newItem.selected_cat_id = -1
        newItem.categories = session.query(
            Category).order_by(Category.name).all()
    else:
        try:
            newItem.categories = session.query(
                Category).filter_by(id=newItem.category_id).all()
        except AttributeError:
            newItem.categories = ""
        else:
            newItem.category_custom = ""

    newItem.error += newItem.catError
    newItem.errorMsg += newItem.catErrorMsg

    return newItem


def setSubCategory(newItem):

    # ---add/edit: set item subcategory:
    newItem.subCatError = 0
    newItem.subCatErrorMsg = ""

    if request.form['subcategory_custom']:
        newItem.subcategory_custom = request.form['subcategory_custom']
        try:
            newItem.subcategory = request.form['subcategory']
        except KeyError:
            subcat_in_db = session.query(Subcategory)\
                .filter_by(name=newItem.subcategory_custom).first()
            # ---(hands-on check over: except sa.exc.IntegrityError on insert)
            if subcat_in_db is not None:
                newItem.subCatError += 1
                newItem.subCatErrorMsg += "Subcategory already exists! "
            else:
                newItem.subcategory_id = ""
                newItem.selected_subcat = "Subcategory:"
        else:
            if newItem.subcategory != "Subcategory:":
                newItem.subCatError += 1
                newItem.subCatErrorMsg += "Ambiguous subcategory "
                newItem.subCatErrorMsg += "- please respecify. "
                newItem.selected_subcat = session.query(Subcategory)\
                    .filter_by(id=request.form['subcategory']).one()
                newItem.selected_subcat = newItem.selected_subcat.name
    else:
        if newItem.category_custom:
            newItem.subCatError += 1
            newItem.subCatErrorMsg += "Custom category requires new/custom "
            newItem.subCatErrorMsg += "subcategory. "
        missing = 0
        try:
            newItem.subcategory_id = request.form['subcategory']
        except KeyError:
            missing += 1
        else:
            newItem.subcategory_custom = ""

        if (missing or newItem.subcategory_id == "Subcategory:"):
            newItem.subCatError += 1
            newItem.subCatErrorMsg += "Subcategory required. "

    if newItem.catError == 0:
        if newItem.subCatError:
            if "Ambiguous subcategory" not in newItem.subCatErrorMsg:
                newItem.selected_subcat = "Subcategory:"
                newItem.subcategories = session.query(Subcategory)\
                    .order_by(Subcategory.name).all()
                newItem.subcategory_custom = ""
            else:
                newItem.subcategories = session.query(
                    Subcategory).order_by(Subcategory.name).all()
        else:
            if not newItem.subcategory_custom:
                try:
                    selected_subcat = session.query(Subcategory)\
                        .filter_by(id=request.form['subcategory']).one()
                except:
                    selected_subcat = session.query(Subcategory)\
                        .filter_by(name=request.form['subcategory']).one()
                newItem.selected_subcat = selected_subcat.name
                newItem.subcategory_id = selected_subcat.id
                newItem.subcategories = session.query(Subcategory)\
                    .filter_by(id=request.form['subcategory']).all()
                newItem.subcategory_custom = ""
            else:
                newItem.subcategory_custom = request.form['subcategory_custom']
                newItem.selected_subcat = "Subcategory:"
                newItem.subcategories = session.query(
                    Subcategory).order_by(Subcategory.name).all()
    else:
        newItem.selected_subcat = "Subcategory:"
        newItem.subcategories = session.query(
            Subcategory).order_by(Subcategory.name).all()
        newItem.subcategory_custom = ""

    newItem.error += newItem.subCatError
    newItem.errorMsg += newItem.subCatErrorMsg
    return newItem


def setBrand(newItem):

    # ---add/edit: set item brand
    newItem.brandError = 0
    newItem.brandErrorMsg = ""

    if request.form['brand_custom']:
        newItem.brand_custom = request.form['brand_custom']
        try:
            newItem.brand = request.form['brand']
        except KeyError:
            brand_in_db = session.query(Brand)\
                .filter_by(name=newItem.brand_custom).first()
            if brand_in_db is not None:
                newItem.brandError += 1
                newItem.brandErrorMsg += "Brand already exists! "
            else:
                newItem.brand_id = ""
        else:
            if newItem.brand != "Brand:":
                newItem.brandError += 1
                newItem.brandErrorMsg += "Ambiguous brand - please respecify. "
    else:
        missing = 0
        try:
            newItem.brand_id = request.form['brand']
        except KeyError:
            missing += 1
        else:
            newItem.brand_custom = ""

        if (missing or newItem.brand_id == "Brand:"):
            newItem.brandError += 1
            newItem.brandErrorMsg += "Brand required. "

    if newItem.brandError:
        if "Ambiguous" in newItem.brandErrorMsg:
            newItem.brands = session.query(Brand).filter_by(
                id=request.form['brand']).all()
            newItem.selected_brand = session.query(
                Brand).filter_by(id=request.form['brand']).one()
            newItem.selected_brand = newItem.selected_brand.name
            newItem.brand_custom = request.form['brand_custom']
        else:
            try:
                brand_custom = newItem.brand_custom
            except AttributeError:
                newItem.brand_custom = ""
                try:
                    newItem.selected_brand = request.form['brand']
                except KeyError:
                    newItem.selected_brand = "Brand:"
                    newItem.brands = session.query(
                        Brand).order_by(Brand.name).all()
                else:
                    newItem.selected_brand = session.query(Brand)\
                        .filter_by(id=request.form['brand']).one()
                    newItem.selected_brand = selected_brand.name
                    newItem.brands = session.query(Brand)\
                        .filter_by(id=request.form['brand']).all()
            else:
                newItem.brands = session.query(
                    Brand).order_by(Brand.name).all()
                newItem.selected_brand = "Brand:"
    else:
        if not newItem.brand_custom:
            try:
                selected_brand = session.query(Brand)\
                    .filter_by(id=request.form['brand']).one()
            except:
                selected_brand = session.query(Brand)\
                    .filter_by(name=request.form['brand']).one()
            newItem.selected_brand = selected_brand.name
            newItem.brand_id = selected_brand.id
            newItem.brands = session.query(Brand)\
                .filter_by(id=request.form['brand']).all()
            newItem.brand_custom = ""
        else:
            newItem.brand_custom = request.form['brand_custom']
            newItem.selected_brand = "Brand:"
            newItem.brands = session.query(Brand).order_by(Brand.name).all()

    newItem.error += newItem.brandError
    newItem.errorMsg += newItem.brandErrorMsg
    return newItem


def setCondition(newItem):

    # ---add/edit: set new item condition
    newItem.condError = 0
    newItem.condErrorMsg = ""
    try:
        newItem.condition = request.form['condition']
    except KeyError:
        newItem.condError += 1
        newItem.condErrorMsg += "Condition required. "
        newItem.condition = ""

    newItem.error += newItem.condError
    newItem.errorMsg += newItem.condErrorMsg
    return newItem


@app.route('/addinstrumentPost', defaults={'instrument_id': None},
           methods=['POST'])
@app.route('/addinstrumentPost/<int:instrument_id>', methods=['POST'])
def addInstrumentPost(instrument_id):

    newItem = session.query(Instrument)
    newItem.resetMsg = ""
    newItem.error = 0
    newItem.errorMsg = ""

    try:
        newItem.model = request.form['model']
    except KeyError:
        newItem.model = ""

    try:
        newItem.description = request.form['description']
    except KeyError:
        newItem.description = ""

    try:
        newItem.price = request.form['price']
    except KeyError:
        newItem.price = ""

    newItem = setCategory(newItem)
    newItem = setSubCategory(newItem)
    newItem = setBrand(newItem)
    newItem = setCondition(newItem)

    if newItem.error > 0:

        return render_template('addInstrument.html',
                               username=login_session['username'],
                               selected_cat=newItem.selected_cat,
                               selected_cat_id=newItem.selected_cat_id,
                               categories=newItem.categories,
                               category_custom=newItem.category_custom,
                               selected_subcat=newItem.selected_subcat,
                               subcategories=newItem.subcategories,
                               subcategory_custom=newItem.subcategory_custom,
                               selected_brand=newItem.selected_brand,
                               brands=newItem.brands,
                               brand_custom=newItem.brand_custom,
                               description=newItem.description,
                               model=newItem.model,
                               price=newItem.price,
                               condition=newItem.condition,
                               resetMsg=newItem.resetMsg,
                               adderror=newItem.errorMsg)
    else:

        # ---double-check user is logged-in before applying transaction
        if 'username' not in login_session:
            flash("Must be logged in to modify/add an instrument or item!")
            return redirect(url_for('showMain'))
        else:
            user_id = getUserID(login_session['email'])

        newInstr = session.query(Instrument)
        # ---set category
        if newItem.category_custom:
            newCategory = Category(name=newItem.category_custom)
            session.add(newCategory)
            session.commit()
            newCat = session.query(Category)\
                .filter_by(name=newItem.category_custom).one()
            newInstr.category_id = newCat.id
        else:
            newInstr.category_id = newItem.category_id

        # ---set subcategory
        if newItem.subcategory_custom:
            newSubCategory = Subcategory(name=newItem.subcategory_custom,
                                         category_id=newInstr.category_id)
            session.add(newSubCategory)
            session.commit()
            newSubCat = session.query(Subcategory)\
                .filter_by(name=newItem.subcategory_custom).one()
            newInstr.subcategory_id = newSubCat.id
        else:
            newInstr.subcategory_id = newItem.subcategory_id

        # ---set brand
        if newItem.brand_custom:
            newBrand = Brand(name=newItem.brand_custom)
            session.add(newBrand)
            session.commit()
            newBrand = session.query(Brand)\
                .filter_by(name=newItem.brand_custom).one()
            newInstr.brand_id = newBrand.id
        else:
            newInstr.brand_id = newItem.brand_id

        # ---construct query object

        # ---edit existing item
        if instrument_id:
            addInstr = session.query(Instrument)\
                .filter_by(id=instrument_id).one()
            addInstr.category_id = newInstr.category_id
            addInstr.subcategory_id = newInstr.subcategory_id
            addInstr.brand_id = newInstr.brand_id
            addInstr.condition = newItem.condition
            addInstr.model = newItem.model
            addInstr.description = newItem.description
            addInstr.price = newItem.price
            addInstr.picture = ""
            addInstr.user_id = user_id
            flashMsg = "Item successfully updated."
        else:
            # ---add instrument/item
            addInstr = Instrument(category_id=newInstr.category_id,
                                  subcategory_id=newInstr.subcategory_id,
                                  brand_id=newInstr.brand_id,
                                  condition=newItem.condition,
                                  model=newItem.model,
                                  description=newItem.description,
                                  price=newItem.price,
                                  picture="",
                                  user_id=user_id
                                  )
            flashMsg = "Item successfully added to database"

        # ---commit to database
        session.add(addInstr)
        session.commit()

        flash(flashMsg)
        return redirect(url_for('instrument', instrument_id=addInstr.id))


'''
NOTES - add or edit instrument:
Category-subcategory consistency is enforced here, thus we reload
the page with subcategory children of parent categories.

In so doing, we:
1). Set the category selection text to what the user indicated
2). Make note of the selected category in our hidden input in
    a). See: addInstrument.html: selected_ategory
3). Filter subcategory options accordingly
    a). ('Reset Form' retrieves all categories)

A snippet of JS in the addInstrument.html &  editInstrument.html
templates (filterSubcategory) yields this functionality.
'''


@app.route('/addinstrument', defaults={'category_name': None}, methods=['GET'])
@app.route('/addinstrument/<category_name>')
def addInstrument(category_name):

    brands = session.query(Brand).order_by(Brand.name).all()
    resetMsg = ""

    if not category_name:
        selected_cat = "Category:"
        selected_cat_id = -1
        categories = session.query(Category).order_by(Category.name).all()
        subcategories = session.query(
            Subcategory).order_by(Subcategory.name).all()
    else:
        selected_cat = category_name
        categories = session.query(Category).filter_by(
            name=category_name).all()
        category = session.query(Category).filter_by(name=category_name).one()
        selected_cat_id = category.id
        subcategories = session.query(Subcategory).filter_by(
            category_id=category.id).order_by(Subcategory.name).all()
        resetMsg = "(RESET FORM: for all categories)"

    adderror = ""

    return render_template('addInstrument.html', menu_heading="Add Item:",
                           username=login_session['username'],
                           selected_cat=selected_cat,
                           selected_cat_id=selected_cat_id,
                           selected_subcat="Subcategory:",
                           selected_brand="Brand:",
                           categories=categories,
                           subcategories=subcategories,
                           brands=brands,
                           reset_msg=resetMsg,
                           adderror=adderror)


@app.route('/<int:instrument_id>/edit', defaults={'category_name': None},
           methods=['GET'])
@app.route('/<int:instrument_id>/edit/<category_name>')
def edit(instrument_id, category_name):

    # ---check user is actually logged in before this step
    if 'username' not in login_session:
        flash("Must be logged in to edit an instrument/item!")
        return redirect(url_for('showMain'))
    else:
        user_id = getUserID(login_session['email'])

    instData = session.query(Instrument.model, Instrument.condition,
                             Instrument.description, Instrument.price,
                             Instrument.user_id, Instrument.category_id,
                             Category.name.label("category"),
                             Subcategory.name.label("subcategory"),
                             Brand.name.label("brand")
                             ).filter_by(id=instrument_id).join(Subcategory) \
                            .join(Category).join(Brand).one()

    # ---restrict editing to poster/author of item:
    if instData.user_id != user_id:
        flash("Must be owner/poster of instrument or item to edit.")
        return redirect(url_for('instrument', instrument_id=instrument_id))

    resetMsg = ""
    brands = session.query(Brand).order_by(Brand.name).all()

    if not category_name:
        selected_cat = instData.category
        selected_cat_id = instData.category_id
        categories = session.query(Category).order_by(Category.name).all()
        subcategories = session.query(
            Subcategory).order_by(Subcategory.name).all()
    else:
        selected_cat = category_name
        categories = session.query(Category).filter_by(
            name=category_name).all()
        category = session.query(Category).filter_by(name=category_name).one()
        selected_cat_id = category.id
        subcategories = session.query(Subcategory)\
            .filter_by(category_id=category.id)\
            .order_by(Subcategory.name).all()

    return render_template('editInstrument.html', menu_heading="Edit Item:",
                           instrument_id=instrument_id,
                           username=login_session['username'],
                           selected_cat=selected_cat,
                           selected_cat_id=selected_cat_id,
                           categories=categories,
                           category_custom="",
                           selected_subcat=instData.subcategory,
                           subcategories=subcategories,
                           subcategory_custom="",
                           selected_brand=instData.brand,
                           brands=brands, brand_custom="",
                           description=instData.description,
                           model=instData.model, price=instData.price,
                           condition=instData.condition, reset_msg=resetMsg,
                           editerror="")


@app.route('/delete/<int:instrument_id>')
def delete(instrument_id):

    # ---check user is actually logged in before this step
    if 'username' not in login_session:
        flash("Must be logged in to delete an instrument/item!")
        return redirect(url_for('showMain'))
    else:
        user_id = getUserID(login_session['email'])

    instData = session.query(Instrument).filter_by(id=instrument_id).one()

    # ---restrict deletion to poster/author of item:
    if instData.user_id != user_id:
        flash("Must be owner/poster of item to delete.")
        return redirect(url_for('instrument', instrument_id=instrument_id))

    # ---direct to confirmation page
    return redirect(url_for('deleteInstrument', instrument_id=instrument_id))


@app.route('/deleteConfirm/<int:instrument_id>', methods=['GET', 'POST'])
def deleteInstrument(instrument_id):
    if request.method == 'GET':
        instData = session.query(Instrument.model, Instrument.condition,
                                 Instrument.description, Instrument.price,
                                 Subcategory.name, Brand.name, User.name
                                 ).filter_by(id=instrument_id) \
                                 .join(Subcategory) \
                                 .join(Brand).join(User)

        heading = "ARE YOU SURE YOU WANT TO DELETE?"

        if 'username' in login_session:
            return render_template('deleteInstrument.html',
                                   menu_heading=heading,
                                   username=login_session['username'],
                                   instrument_id=instrument_id,
                                   info=instData)
        else:
            flash("Must be owner/poster of item to delete.")
            return redirect(url_for('instrument', instrument_id=instrument_id))

    else:
        delInstr = session.query(Instrument).filter_by(id=instrument_id).one()
        session.delete(delInstr)
        session.commit()

        flash("Successfully deleted instrument/item.")
        return redirect(url_for('showMain'))


@app.route('/purchase/<int:instrument_id>')
def purchase(instrument_id):
    # ---check user is actually logged in before this step
    if 'username' not in login_session:
        flash("Must be logged in to purchase/inquire about an instrument!")
        return redirect(url_for('showMain'))
    else:
        user_id = getUserID(login_session['email'])

    instData = session.query(Instrument).filter_by(id=instrument_id).one()

    # ---restrict deletion to poster/author of item:
    if instData.user_id == user_id:
        flash("You are the poster of this item!")
        return redirect(url_for('instrument', instrument_id=instrument_id))
    else:
        ownerData = session.query(User).filter_by(id=instData.user_id).one()
        msg = "Please send an inquiry to: " + ownerData.email
        msg += " for more information on this item."
        flash(msg)
        return redirect(url_for('instrument', instrument_id=instrument_id))

    # ---direct to confirmation page
    return redirect(url_for('deleteInstrument', instrument_id=instrument_id))

# =============================================================================


# ===JSON API UTILITIES========================================================

@app.route('/instrument/JSON')
def allInstrumentsJSON():
    allInstr = session.query(Instrument).all()
    return jsonify(Instruments=[inst.serialize for inst in allInstr])


@app.route('/brand/JSON')
def brandJSON():
    brands = session.query(Brand).all()
    return jsonify(Brands=[brd.serialize for brd in brands])


@app.route('/category/JSON')
def categoryJSON():
    categoryData = session.query(Category).all()
    return jsonify(Categories=[cat.serialize for cat in categoryData])


@app.route('/<int:instrument_id>/JSON')
def instrumentJSON(instrument_id):
    instrData = session.query(Instrument).filter_by(id=instrument_id).one()
    return jsonify(InstrumentDetails=instrData.serialize)

# =============================================================================


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
