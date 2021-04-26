"""
This file contains the functional tests for the routes.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
import os
import tempfile
import pytest
from config import basedir
from app import app,db,login
from app.models import User, Item, Sellerorder, Buyerorder, Report, Review


@pytest.fixture(scope='module')
def test_client(request):
    #re-configure the app for tests
    app.config.update(
        SECRET_KEY = 'bad-bad-key',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        WTF_CSRF_ENABLED = False,
        DEBUG = True,
        TESTING = True,
    )
    db.init_app(app)
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = app.test_client()
 
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
 
    yield  testing_client 
    # this is where the testing happens!
 
    ctx.pop()


@pytest.fixture
def init_database(request,test_client):
    # Create the database and the database table
    db.create_all()
    #add a seller
    seller = User(username='seller', email="SellerTest@example.com", first_name="SellerFirst", last_name="SellerLast", address="Seller Address", card_number="1111111111111111", security_code="111", is_seller = True)
    seller.set_password('123')
    db.session.add(seller)
    #add a buyer
    buyer = User(username='buyer', email="BuyerTest@example.com", first_name="BuyerFirst", last_name="BuyerLast", address="Buyer Address", card_number="1111111111111111", security_code="111", is_seller = False)
    buyer.set_password('321')
    db.session.add(buyer)
    #add an item
    item = Item(item_name = 'Test item', item_description = 'Test description', initial_supply = 10, num_available = 10, seller_id = 1, price = 10.00)
    db.session.add(item)
    #add a review
    review = Review(title = 'Test review', body = 'This is a test review for a test item!', rating = 4)
    db.session.add(review)
    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()



def test_register_page(request,test_client):
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data


def test_seller_page(request,test_client):
    #Create new seller
    seller = User(username='seller2', email="Seller2@example.com", first_name="SellerFirst", last_name="SellerLast", address="Seller Address", card_number="1111111111111111", security_code="111", is_seller = True)
    seller.set_password('123')
    db.session.add(seller)
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/seller_page/seller2')
    assert response.status_code == 200
    assert b"seller" in response.data


def test_item_page(request,test_client):
    # Create a test client using the Flask application configured for testing
    item = Item(item_name = 'Testitem2', item_description = 'Test description', initial_supply = 10, num_available = 10, seller_id = 1, price = 10.00)
    db.session.add(item)
    response = test_client.get('/detailed_item/1')
    assert response.status_code == 200


def test_register(request,test_client,init_database):
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/register', 
                          data=dict(username="buyer2", email="Buyer2@example.com", password="bad-bad-password",password2="bad-bad-password", firstname="BuyerFirst", lastname="BuyerLast", address="Buyer Address", card_number="1111111111111111", security_code="111", buyer_or_seller=2) ,
                          follow_redirects = True)
    assert response.status_code == 200

    s = db.session.query(User).filter(User.username=='buyer2')
    assert s.count() == 1
    assert b"Congratulations, you are now a registered buyer!" in response.data


def test_invalidlogin(request,test_client,init_database):
    response = test_client.post('/login', 
                          data=dict(username='2buyer', password='12345',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


def test_login_logout(request,test_client,init_database):
    response = test_client.post('/login', 
                          data=dict(username='buyer2', password='bad-bad-password',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    

def test_post_Item(request,test_client,init_database):
    response = test_client.post('/login', 
                          data=dict(username='seller', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
                      
    response = test_client.post('/postItem', 
                          data=dict(item_name='item', item_description='test item',initial_supply = 10, num_available = 10, seller_id = 1, price = 10.00),
                          follow_redirects = True)
    assert response.status_code == 200
    s = db.session.query(Item).filter(Item.item_name=='item')
    assert s.count() == 1
    assert b'Item: item has been posted!' in response.data


def test_edit_profile(request,test_client,init_database):
    response = test_client.post('/edit_profile', 
                          data=dict(username='updated_seller', password="bad-bad-password",password2="bad-bad-password", about_seller="Welcome to my store", email="SellerTest@example.com", firstname="SellerFirst", lastname="SellerLast", address="Seller Address", card_number="1111111111111111", security_code="111"),
                          follow_redirects = True)
    assert response.status_code == 200
    s = db.session.query(User).filter(User.username=='updated_seller')
    assert s.count() == 1
    assert b'Your profile has been saved.' in response.data


def test_edit_item(request,test_client,init_database):
    response = test_client.post('/edit_item1', 
                           data=dict(item_name='item_updated', item_description='test item',initial_supply = 10, num_available = 20, price = 10.00),
                          follow_redirects = True)
    assert response.status_code == 200
    s = db.session.query(Item).filter(Item.item_name=='item_updated')
    assert s.count() == 1
    assert b'Your changes have been saved.' in response.data
    

def test_review_item(request,test_client,init_database):
    response = test_client.post('/review1', 
                           data=dict(title='first review', body='mediocre item',rating = 4),
                          follow_redirects = True)
    assert response.status_code == 200
    s = db.session.query(Review).filter(Review.title=='first review')
    assert s.count() == 1
    assert b'Your review has been recorded.' in response.data


def test_report_user(request,test_client,init_database):
    response = test_client.post('/report2', 
                           data=dict(title='report', body='bad buyer'),
                          follow_redirects = True)
    assert response.status_code == 200
    s = db.session.query(Report).filter(Report.title=='report')
    assert s.count() == 1
    assert b'Your report has been recorded.' in response.data


def test_cart_add_remove(request,test_client,init_database):
    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200

    response = test_client.post('/login', 
                          data=dict(username='buyer', password='321',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200

    response = test_client.get('/add/1')
    s = db.session.query(User).filter(User.username=='buyer').first().in_cart
    assert s.count() == 1

    response = test_client.get('/remove/1')
    s = db.session.query(User).filter(User.username=='buyer').first().in_cart
    assert s.count() == 0



def test_checkout(request,test_client,init_database):
    response=test_client.get('/checkout')
    assert response.status_code == 200


def test_confirm_order(request,test_client,init_database):
    response = test_client.post('/confirm_order', 
                           data=dict(email='BuyerTest@example.com', address='Buyer Address', card_number='1111111111111111',security_code='111'),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b'Your order has been made!' in response.data

