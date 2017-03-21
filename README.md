**DESCRIPTION**


This collection of scripts comprises a self-contained web application  
developed in Python which uses the Flask web framework to demonstrate  
the use of a SQLite-driven database back-end and HTML form elements  
to perform common web-based database operations.  

Functionality on the site depends on user registration/logged-in status which  
is handled through 3rd party OAuth 2.0 authorization for security purposes.  

Taken together, this projects illustrates the following important aspects of  
web applications:  

-use of Flask and the SQLAlchemy ORM  
-database create/read/update/delete operations (CRUD)  
-basic RESTful API endpoints to access application data in JSON/XML  
-industry-standard OAuth 2.0 3rd-party authorization (via Google Sign-In)  
-standard SQL queries crafted for the SQLite database engine  
-data integrity operations and navigational/error-checking logic  
-some JavaScript for controlling client-side form behavior  

The application is for a fictional store called "The Instrument Garage" which  
lists the new and used musical instruments members might have to offer or  
trade (buy/sell) with one another.  


**REQUIREMENTS**  


This application is developed in Python 2.7.x and makes use of the following  
modules/libraries:  

-python 2.7.x: random, string, httplib2, json, requests  
-flask: flash, jsonify  
-sqlalchemy: asc, create_engine, func  
-sqlalchemy.orm: sessionmaker  
-oauth2client.client: flow_from_clientsecrets, FlowExchangeError  

Database definitions for the fictional datbase reside in the script create_db.py  
from which the following customized components must also be imported after the  
database has been initialized (created and populated):  

-create_db: Base, User, Category, Subcategory, Brand, Instrument  
-instrumentgarage.db (sqlite database created per instructions below)


**INSTRUCTIONS**  


In order to run the application from scratch, clone this repository to  
your local workspace per GitHub instructions:  

https://help.github.com/articles/cloning-a-repository/  

Before running, you will need to have some flavor of Python 2.7.x installed  
as well as the lightweight Flask web framework and SQLAlchemy database toolkit.  

These may be downloaded here (refer to individual sites for installation  
instructions for the environment which suits your needs):  

-Python 2.7.x  
https://www.python.org/downloads/  

-OAuth 2.0 clients for Python:  
https://pypi.python.org/pypi/oauth2client/2.2.0  

-Flask: 
https://pypi.python.org/pypi/Flask/0.12  

-SQLAlchemy:  
https://www.sqlalchemy.org/download.html  

With all items downloaded and installed, run the following steps to create and  
populate the ficitional store database:  

1). Run the create_db.py script  
    This will setup the instrumentgarage.db database for use in the application
    Note: any changes to the name of this database must also be reflected in the
    corresponding entry in the catalog.py script which creates the sqlite 
    engine with reference to this database object.

2). Run the populate_db.py script
    This will populate the instrumentgarage.db with an initial set of data for
    querying complete with users, instruments in various categories at various
    price points and usage conditions.

Note: the application makes use of flask's built-in web server and sets the  
flask session key (meant to be a secret user key) to a generic value in the  
main catalog.py script.  As such, the application is intended for demonstration  
uses only.  By default, the application is setup to run on localhost with port  
set to 5000.  These settings maybe edited in the catalog.py file, as required.  

As a final step:  

3). Run the catalog.py script  

If all required components have been properly downloaded and installed  
and default settings are used and all components, the website should be  
accessible on:

localhost:5000


**SITE USAGE**


**Navigation Basics**

The main page lists categories of musical instruments which may be clicked  
on to list individual instruments in the category.  As an alternative, users  
may also view instruments as listed by brand,  similar to the display alternative  
many online music retailers also offer.

Clicking on either a brand or a category heading will return a listing of the  
instruments available in either that category or brand.  The entries which  
appear here are summarizes/highlights of the instrument entries for which more  
detail may be accessed by following the 'More' link under each instrument.

Clicking on a 'More' link will render a full page dedicated to that particular  
instrument with full descriptive details including postage by user.

Instrument-page functionality is restricted to viewing-only if the user is  
either not registered or not logged-in.  Registering and/or logging-in gives  
the user the ability to post/edit/delete instrument listings.

Registration and sign-in is done via OAuth 2.0 using Google sign-in and new  
users are added to the user database based on authorizations agreed to by the  
client.

Posting functionality is made available to any signed-in user.  However,  
editing/deleting functionality is restricted to original posters of the  
respective items with a confirmation page used for deletions.  

A token 'Purchase' button reveals the contact information of the poster of  
the item (which in production would likely require an agreement in terms of  
use or be otherwise centrally handled for privacy purposes).


**Posting/Editing Items**

A category-subcategory parent-child relationship is enforced during  
the posting/editing process such that the specified subcategory for the posting  
(pianos) must be a child of the specified parent category (keyboards).  

Required fields are annotated with an asterisk on the posting page and include  
category, subcategory, brand, and condition.  The fields model, description, and  
price are optional for posting/editing purposes.

Errors are raised when any combination of missing required fields are 
not provided.  

In addition to the pre-canned categories/subcategories and instruments which  
come with the initial database, custom categories/subcategories/brands may be  
added.  Errors checks are performed in these instances as well, to ensure  
data integrity/consistency.

Enjoy the demo project!
