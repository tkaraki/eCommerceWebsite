from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

# test_models.py
# want tests for iteration-2 exclusively testing all of the models.
# try to test everything, couple tests for every model table
# if have methods in a model, include a test for each method.
# expecting at least one test per table and method.
# test meaningful stuff.

@login.user_loader
def load_user(id):
    user = User.query.get(int(id))
    return user

cart = db.Table('cart', # shows the relationship between a buyer and the items in their cart
    db.Column('buyer_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'))
)

itemSellerOrder = db.Table('itemSellerOrder', # shows the relationship between a seller and the items ordered from them
    db.Column('order_id', db.Integer, db.ForeignKey('sellerorder.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'))
)

itemBuyerOrder = db.Table('itemBuyerOrder', # shows the relationship between a buyer and the items ordered by them
    db.Column('order_id', db.Integer, db.ForeignKey('buyerorder.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'))
)

sellerBuyerOrder = db.Table('sellerBuyerOrder', # shows the relationship between an order made by a buyer and the sellers selling the items in the order
    db.Column('order_id', db.Integer, db.ForeignKey('buyerorder.id')),
    db.Column('seller_id', db.Integer, db.ForeignKey('user.id'))
)

class Search(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    search_key = db.Column(db.String(100))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item_name = db.Column(db.String(64), index = True)
    item_description = db.Column(db.String(1500))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    price = db.Column(db.Float(precision = 2, asdecimal = True))
    posted_on = db.Column(db.DateTime, default = datetime.utcnow)
    num_available = db.Column(db.Integer, default = 0)
    initial_supply = db.Column(db.Integer, default = 0)
    in_cart_of = db.relationship('User', secondary = cart, primaryjoin = (cart.c.item_id == id), backref = db.backref('cart', lazy = 'dynamic'), lazy = 'dynamic') # All of the carts that an item is in
    num_purchased = db.Column(db.Integer, default = 0)
    supplied_in = db.relationship('Sellerorder', secondary = itemSellerOrder, primaryjoin = (itemSellerOrder.c.item_id == id), backref = db.backref('itemSellerOrder', lazy = 'dynamic'), lazy = 'dynamic') # All of the seller orders that an item exists in
    bought_in = db.relationship('Buyerorder', secondary = itemBuyerOrder, primaryjoin = (itemBuyerOrder.c.item_id == id), backref = db.backref('itemBuyerOrder', lazy = 'dynamic'), lazy = 'dynamic') # All of the buyer orders that an item exists in
    reviews = db.relationship('Review', backref='reviewed', lazy='dynamic')
    rating = db.Column(db.Float(precision = 2, asdecimal = True), default = 0.0)

class Sellerorder(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id')) # The id of the seller who owns this order
    contains = db.relationship('Item', secondary = itemSellerOrder, primaryjoin = (itemSellerOrder.c.order_id == id), backref = db.backref('itemSellerOrder', lazy = 'dynamic'), lazy = 'dynamic') # All of the items from the specific supplier owning this Sellerorder
    purchased_on = db.Column(db.DateTime, default = datetime.utcnow) # Date purchased
    total = db.Column(db.Float(precision = 2, asdecimal = True)) # The total of all items from the specific supplier owning this Sellerorder
    buyer_id = db.Column(db.Integer) # The customer who placed this order
    buyer_username = db.Column(db.String)

    def add_to_order(self, item):
        if not (item in self.contains):
            if (self.seller_id == item.seller_id):
                self.contains.append(item)
                self.total += item.price

class Buyerorder(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id')) # The id of the buyer who owns this order
    contains = db.relationship('Item', secondary = itemBuyerOrder, primaryjoin = (itemBuyerOrder.c.order_id == id), backref = db.backref('itemBuyerOrder', lazy = 'dynamic'), lazy = 'dynamic') # All of the items in this order
    purchased_on = db.Column(db.DateTime, default = datetime.utcnow) # Date purchased
    suppliers = db.relationship('User', secondary = sellerBuyerOrder, primaryjoin = (sellerBuyerOrder.c.order_id == id), backref = db.backref('sellerBuyerOrder', lazy = 'dynamic'), lazy = 'dynamic') # All of the items in this order
    total = db.Column(db.Float(precision = 2, asdecimal = True)) # Total cost of the order

    def add_to_order(self, item):
        if not (item in self.contains):
            self.contains.append(item)
            self.total += item.price
            item.num_purchased += 1

    def add_supplier(self, seller):
        if not (seller in self.suppliers):
            self.suppliers.append(seller)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    about_seller = db.Column(db.String(140))
    address = db.Column(db.String(200))
    card_number = db.Column(db.String(16))
    security_code = db.Column(db.String(3))
    items = db.relationship('Item', backref='supplier', lazy='dynamic')
    is_seller = db.Column(db.Boolean, default = True)
    in_cart = db.relationship('Item', secondary = cart, primaryjoin = (cart.c.buyer_id == id), backref = db.backref('cart', lazy = 'dynamic'), lazy = 'dynamic') # All of the items in a buyer's cart
    orders_to = db.relationship('Sellerorder', backref='supplier', lazy='dynamic') # Order made to a seller
    orders_by = db.relationship('Buyerorder', backref='customer', lazy='dynamic') # Order made by a buyer
    orders_involved_in = db.relationship('Buyerorder', secondary = sellerBuyerOrder, primaryjoin = (sellerBuyerOrder.c.seller_id == id), backref = db.backref('sellerBuyerOrder', lazy = 'dynamic'), lazy = 'dynamic') # All of the items in this order
    reports = db.relationship('Report', backref='reported', lazy='dynamic')
    reviews = db.relationship('Review', backref='reviewer', lazy='dynamic')

    def __repr__(self):
        return '<User {} - {};>'.format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_to_cart(self, item):
        if not (item in self.in_cart):
            item.num_available -= 1
            self.in_cart.append(item)

    def remove_from_cart(self, item):
        if (item in self.in_cart):
            item.num_available += 1
            self.in_cart.remove(item)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    rating = db.Column(db.Integer)

    def add_review(self, buyer, item):
        self.user_id = buyer.id
        self.item_id = item.id

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    username = db.Column(db.String(64)) #Username of the user who made the report
    body = db.Column(db.String(1500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    reported_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def add_report(self, reported, reporter):
        if not (self in reported.reports):
            reported.reports.append(self)
        self.reported_id = reported.id
        self.username = reporter.username