from __future__ import print_function
from datetime import datetime
import sys, re

from flask import render_template, flash, redirect, url_for, request, current_app
from flask_sqlalchemy import sqlalchemy
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditSellerForm, EditBuyerForm, PostItemForm, CheckoutForm, EditItemForm, ReportForm, ReviewForm, SortForm, SearchForm
from app.models import User, Item, Sellerorder, Buyerorder, Report, Review, Search

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()

@app.route('/dummy', methods=['GET', 'POST'])
def dummy():
    form = RegistrationForm()
    seller = User(username="ASeller", email="ASeller@example.com", first_name="SellerFirst", last_name="SellerLast", address="Seller Address", card_number="1111111111111111", security_code="111", is_seller = True)
    seller.set_password("Seller")  
    db.session.add(seller)
    seller2 = User(username="ASeller2", email="ASeller2@example.com", first_name="Seller2First", last_name="Seller2Last", address="Seller2 Address", card_number="3333333333333333", security_code="333", is_seller = True)
    seller2.set_password("Seller2")  
    db.session.add(seller2)
    seller3 = User(username="ASeller3", email="ASeller3@example.com", first_name="Seller3First", last_name="Seller3Last", address="Seller3 Address", card_number="5555555555555555", security_code="555", is_seller = True)
    seller3.set_password("Seller3")  
    db.session.add(seller3)
    seller4 = User(username="ASeller4", email="ASeller4@example.com", first_name="Seller4First", last_name="Seller3Last", address="Seller4 Address", card_number="6666666666666666", security_code="666", is_seller = True)
    seller4.set_password("Seller4")  
    db.session.add(seller4)
    buyer = User(username="ABuyer", email="ABuyer@example.com", first_name="BuyerFirst", last_name="BuyerLast", address="Buyer Address", card_number="2222222222222222", security_code="222", is_seller = False)
    buyer.set_password("Buyer")  
    db.session.add(buyer)
    buyer2 = User(username="ABuyer2", email="ABuyer2@example.com", first_name="Buyer2First", last_name="Buyer2Last", address="Buyer2 Address", card_number="4444444444444444", security_code="444", is_seller = False)
    buyer2.set_password("Buyer2")  
    db.session.add(buyer2)
    item = Item(item_name = 'Healthy Day! Spray Hand Sanitizer', item_description = '80% alchohol hand sanitizer. \nHealth organization approved. \nLiquid spay allows for thorough and even application. Spray formula is often used in medical facilities. \nA good option when soap and water is not readily available, simple and easy. \nKills 99% of germs.'.replace(r' \n', ' \n'), initial_supply = 40, num_available = 40, seller_id = 1, price = 4.99)
    db.session.add(item)
    item2 = Item(item_name = '50 Pack Disposable Face Masks', item_description = 'Breathable & Soft & Comfortable - BLScode masks with the inner skinfriendly non-woven fabric is as soft as comfortable clothing, light and breathable. \n3-Ply Protective Masks - Outer color layer is a water resistant layer, say bye to splashing liquid; Middle layer is a filtering layer, say bye to particles from 0.3 to 1.0 pm. Inner layer is a water absorbing layer, which can absorb moisture from the breath of the wearer, avoid the filtering layer getting wet. \nEasy to Use - Our protective covers are disposable and single user. Lightweight provides comfort and easy breathing while you\'re at work, a store, or running necessary errands. Just slip the elastic bands over your ears and conform the metal nose guard to create a light seal around your face.'.replace(r' \n', ' \n'), initial_supply = 15, num_available = 15, seller_id = 2, price = 12.96)
    db.session.add(item2)
    item3 = Item(item_name = 'Liquid Hand Soap', item_description = 'Washes away bacteria. \nMicellar Deep Cleansing that\'s dermatologically endorsed by the Skin Health Alliance. \nFrequent handwashing helps keep you and your family healthy. \nFresh, clean, hypoallergenic scent. \nContains antioxidants and vitamin-c.'.replace(r' \n', ' \n'), initial_supply = 20, num_available = 20, seller_id = 3, price = 7.88)
    db.session.add(item3)
    item4 = Item(item_name = 'Healthy Day! Vitamins', item_description = '1000mg Vitamin C (as ascorbic acid) per serving, Supports healthy immune system. \n300 tablets, a 10 month supply (taken daily at listed serving size). \nNo artificial colors, flavors or chemical preservatives. \nVegan and gluten free. Blended and packaged in USA. \nMade in a Good Manufacturing Practices (GMP) facility in the USA. \nSatisfaction Guarantee: We\'re proud of our products. If you aren\'t satisfied, we\'ll refund you for any reason within a year of purchase. \nIf you like Healthy Day! Vitamin C 1000mg, we invite you to try Healthy Day! Spray Hand Sanitizer.'.replace(r' \n', ' \n'), initial_supply = 50, num_available = 50, seller_id = 1, price = 6.99)
    db.session.add(item4)
    item5 = Item(item_name = '20 Pack Disposable Face Masks', item_description = 'Breathable & Soft & Comfortable - BLScode masks with the inner skinfriendly non-woven fabric is as soft as comfortable clothing, light and breathable. \n3-Ply Protective Masks - Outer color layer is a water resistant layer, say bye to splashing liquid; Middle layer is a filtering layer, say bye to particles from 0.3 to 1.0 pm. Inner layer is a water absorbing layer, which can absorb moisture from the breath of the wearer, avoid the filtering layer getting wet. \nEasy to Use - Our protective covers are disposable and single user. Lightweight provides comfort and easy breathing while you\'re at work, a store, or running necessary errands. Just slip the elastic bands over your ears and conform the metal nose guard to create a light seal around your face.'.replace(r' \n', ' \n'), initial_supply = 35, num_available = 35, seller_id = 2, price = 7.00)
    db.session.add(item5)
    item6 = Item(item_name = 'Disposable Medical Clear Vinyl Medical Gloves', item_description = '100 Gloves per Box. \nDisposable, Single-Use Only. \nSuper durable 100% Vinyl material, 100% powder free. \nAvailable in Medium, Large and XLarge. \nMultipurpose for Numerous Fields and Jobs: Food Service, Lab, and More.'.replace(r' \n', ' \n'), initial_supply = 25, num_available = 25, seller_id = 4, price = 19.95)
    db.session.add(item6)
    db.session.commit()
    return redirect('/clear_search')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    sortForm=SortForm()
    if sortForm.validate_on_submit():
        newSort = int(sortForm.sort_by.data)
        if (newSort == 4): 
            items=Item.query.order_by(Item.posted_on.desc())
        elif (newSort == 3): 
            items=Item.query.order_by(Item.rating.desc())
        elif (newSort == 2):
            items=Item.query.order_by(Item.price.asc())
        elif (newSort == 1): 
            items=Item.query.order_by(Item.price.desc())
        else: 
            items = Item.query.order_by(Item.item_name.desc())
        item_list = items.all()
    else:    
        items = Item.query.order_by(Item.item_name.desc())
        item_list = items.all()

    searchForm = SearchForm()
    if searchForm.validate_on_submit():
        search = Search.query.get(1)
        if search is None:
            search = Search(search_key = searchForm.search_key.data)
            db.session.add(search)
            db.session.commit()
        else:
            search.search_key = searchForm.search_key.data
            db.session.commit()

    search = Search.query.get(1)
    if search is None:
        search = Search(search_key = '')
        db.session.add(search)
        db.session.commit()

    search_key = search.search_key
    searchForm.search_key.data = search_key

    if search_key != '':
        for item in items:
            item_name = re.split(', |_| |-|!|\.|\n', item.item_name)
            if not search_key in item_name:
                item_description = re.split(', |_| |-|!|\.|\n', item.item_description)
                if not search_key in item_description:
                    item_list.remove(item)

    return render_template('index.html', searchForm=searchForm, sortForm=sortForm, title="Covid Commerce", items=item_list, current_user = current_user)

@app.route('/clear_search', methods=['GET', 'POST'])
def clear_search():
    search = Search.query.get(1)
    if search is None:
        search = Search(search_key = '')
        db.session.add(search)
        db.session.commit()
    else:
        search.search_key = ''
        db.session.commit()
    return redirect('/index')

@app.route('/seller_page/<seller_username>', methods=['GET'])
def seller_page(seller_username):
    seller = User.query.filter_by(username = seller_username).first()
    items = Item.query.filter_by(seller_id = seller.id)
    return render_template('sellerPage.html', title='Seller Page', items=items.all(), current_user = current_user, seller = seller)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = int(form.buyer_or_seller.data)
        if (user == 1):
            seller = User(username=form.username.data, email=form.email.data, first_name=form.firstname.data, last_name=form.lastname.data, address=form.address.data, card_number=form.card_number.data, security_code=form.security_code.data, is_seller = True)
            seller.set_password(form.password.data)  
            db.session.add(seller)
            db.session.commit()
            flash('Congratulations, you are now a registered seller!')
            return redirect('/clear_search')
        else:
            buyer = User(username=form.username.data, email=form.email.data, first_name=form.firstname.data, last_name=form.lastname.data, address=form.address.data, card_number=form.card_number.data, security_code=form.security_code.data, is_seller = False)
            buyer.set_password(form.password.data)  
            db.session.add(buyer)
            db.session.commit()
            flash('Congratulations, you are now a registered buyer!')
            return redirect('/clear_search')
    return render_template('register.html', title='Register', form=form, current_user = current_user)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.add(current_user)
        db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/clear_search')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.get_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/clear_search')
        login_user(user, remember=form.remember_me.data)
        return redirect('/clear_search')
    return render_template('login.html', title='Sign In', form=form, current_user = current_user)

@app.route('/postItem', methods=['GET', 'POST'])
@login_required
def postItem():
    if current_user.is_seller:
        form = PostItemForm()
        if form.validate_on_submit():
            newItem = Item(item_name = form.item_name.data, item_description = form.item_description.data, initial_supply = form.num_available.data, num_available = form.num_available.data, seller_id = current_user.id, price = form.price.data)
            db.session.add(newItem)
            db.session.commit()
            flash('Item: {} has been posted!'.format(newItem.item_name))
            return redirect('/clear_search')
        return render_template('post_item.html', title = 'Post Item', form = form, current_user = current_user)
    else:
        flash('You must be a seller to post an item!')
        return redirect('/clear_search')
    return render_template('login.html', title='Sign In', form=form, current_user = current_user)

@app.route('/', methods=['GET', 'POST'])
@app.route('/seller_items<seller_id>', methods=['GET', 'POST'])
@login_required
def seller_items(seller_id):
    seller = User.query.filter_by(id = seller_id).first()
    items = Item.query.filter_by(seller_id = seller.id)
    return render_template('seller_items.html', title="Items", items=items.all(), current_user = current_user)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/clear_search')

@app.route('/confirm_order', methods=['GET', 'POST'])
@login_required
def confirm_order():
    form = CheckoutForm(current_user.email)
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.card_number = form.card_number.data
        current_user.security_code = form.security_code.data
        db.session.commit()
        flash('Your order has been made!')
        return redirect('/checkout')
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.card_number.data = current_user.card_number
        form.security_code.data = current_user.security_code
    return render_template('confirm_order.html', title='Confirm Order', form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if (current_user.is_seller == True):
        form = EditSellerForm(current_user.username, current_user.email)
    else:
        form = EditBuyerForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.set_password(form.password.data)
        current_user.first_name = form.firstname.data
        current_user.last_name = form.lastname.data
        if (current_user.is_seller == True):
            current_user.about_seller = form.about_seller.data
        current_user.address = form.address.data
        current_user.card_number = form.card_number.data
        current_user.security_code = form.security_code.data
        db.session.commit()
        flash('Your profile has been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.firstname.data = current_user.first_name
        form.lastname.data = current_user.last_name
        if (current_user.is_seller == True):
            form.about_seller.data = current_user.about_seller
        form.address.data = current_user.address
        form.card_number.data = current_user.card_number
        form.security_code.data = current_user.security_code
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/edit_item<item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get(item_id)
    if not (item in current_user.items):
        flash('You cannot edit that item.')
        return redirect(url_for('index'))
    form = EditItemForm()
    if form.validate_on_submit():
        item.item_name = form.item_name.data
        item.item_description = form.item_description.data
        item.price = form.price.data
        item.initial_supply += form.num_available.data
        item.num_available += form.num_available.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.item_name.data = item.item_name
        form.item_description.data = item.item_description
        form.price.data = item.price
        form.num_available.data = 0
    return render_template('edit_item.html', title='Edit Item', form=form)

@app.route('/review<item_id>', methods=['GET', 'POST'])
@login_required
def review_item(item_id):
    item = Item.query.get(item_id)
    buyer = User.query.get(current_user.id)
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(title = form.title.data, body = form.body.data, rating = form.rating.data)
        db.session.add(review)
        db.session.commit()
        review.add_review(buyer, item)
        total = 0
        for i in item.reviews:
            total += i.rating
        item.rating = (total / item.reviews.count())
        db.session.commit()
        flash('Your review has been recorded.')
        return redirect('/clear_search')
    return render_template('review.html', title='Review Item', form=form)

@app.route('/delete_review<review_id>', methods=['DELETE', 'POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get(review_id)
    item = review.reviewed
    return redirect('/detailed_item<item.id>')

@app.route('/report<user_id>', methods=['GET', 'POST'])
@login_required
def report(user_id):
    user = User.query.get(user_id)
    form = ReportForm()
    if form.validate_on_submit():
        report = Report(title = form.title.data, username = current_user.username, body = form.body.data)
        db.session.add(report)
        db.session.commit()
        report.add_report(user, current_user)
        db.session.commit()
        flash('Your report has been recorded.')
        return redirect('/clear_search')
    return render_template('report.html', title='Report User', form=form)

@app.route('/add/<item_id>', methods=['GET'])
@login_required
def add_item(item_id):
    item = Item.query.get(item_id)
    if (item.num_available <= 0):
        flash('Sorry, this item is unavailable!')
        return redirect('/clear_search')
    else:
        current_user.add_to_cart(item)
        db.session.commit()
        flash('Item: "' + item.item_name + '" has been added to your cart')
        return redirect('/cart')

@app.route('/remove/<item_id>', methods=['GET'])
@login_required
def remove_item(item_id):
    item = Item.query.get(item_id)
    current_user.remove_from_cart(item)
    db.session.commit()
    flash('Item: "' + item.item_name + '" has been removed from your cart')
    return redirect('/cart')

@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
# if I try to add the same item to the cart it does not increase the quantity and price of the item. Is that okay for now?
    items = current_user.in_cart
    totalcost=0
    for i in items:
        totalcost+= i.price
    return render_template('cart.html', title="Your Cart", items=items.all(), current_user = current_user, totalcost = format(totalcost, ".2f"))

@app.route('/detailed_item/<item_id>', methods=['GET'])
def detailed_item(item_id):
    item = Item.query.get(item_id)
    name = item.item_name
    description = item.item_description
    price= item.price
    timestamp= item.posted_on
    quantity = item.num_available
    return render_template('detailed_item.html',item=item, name=name, reviews = item.reviews.all(), rating = item.rating, rating_count = item.reviews.count(), description=description, price= format(price, ".2f"), timestamp=timestamp, quantity=quantity)


@app.route('/order_history', methods=['GET', 'POST'])
@login_required
def order_history():
    if (current_user.is_seller == True):
        orders = current_user.orders_to.all()
        orders = reversed(orders) # reverse the list to get the most recent order in front/on top of order history
    else:
        orders = current_user.orders_by.all()
        orders = reversed(orders) # reverse the list to get the most recent order in front/on top of order history
    return render_template('order_history.html', orders=orders)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    buyer_order = Buyerorder(buyer_id = current_user.id, total = 0)
    buyer = User.query.filter_by(id = current_user.id).first()
    for item in buyer.in_cart:
        buyer_order.add_to_order(item) # Add each item from the cart to the order
        supplier = User.query.filter_by(id=item.seller_id).first() # Find the seller of the item
        buyer_order.add_supplier(User.query.filter_by(id=item.seller_id).first()) # Add the seller of an item to the list of suppliers
        buyer.in_cart.remove(item) # Item is added to order and removed from cart
    # Now make the seller orders
    for seller in buyer_order.suppliers:
        seller_order = Sellerorder(seller_id = seller.id, total = 0, buyer_id = buyer.id, buyer_username = buyer.username) # Make a new seller order
        for item in buyer_order.contains:
            seller_order.add_to_order(item) # The current seller is the supplier of this item, add the item to the seller order
        seller.orders_involved_in.append(buyer_order) # Add the buyer_order to the list of orders that the seller is involved in
        seller.orders_to.append(seller_order) # Add the seller_order to the list of orders that the seller recieves
        db.session.add(seller_order) # Add the new seller order
    current_user.orders_by.append(buyer_order)
    db.session.add(buyer_order) # Add the buyer order
    db.session.commit()
    return render_template('cart.html', title="Your Cart", items=buyer.in_cart.all(), current_user = current_user)
