from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FloatField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange
from app.models import User, Item

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PostItemForm(FlaskForm):
    item_name = StringField('Item name', validators=[DataRequired()])
    item_description = TextAreaField('Item description', validators=[Length(max=1500)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min = 0.00, max = 1E+20)])
    num_available = IntegerField('Number available', validators = [DataRequired(), NumberRange(min = 1, max = 1E+20)])
    submit = SubmitField('Post')

class EditItemForm(FlaskForm):
    item_name = StringField('New item name', validators=[DataRequired()])
    item_description = TextAreaField('New item description', validators=[Length(max=1500)])
    price = FloatField('New price', validators=[DataRequired(), NumberRange(min = 0.00, max = 1E+20)])
    num_available = IntegerField('How many more are available', validators = [NumberRange(min = 0, max = 1E+20)])
    submit = SubmitField('Post')

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', [Length(min=0, max=200)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    card_number = TextAreaField('Card Number', [Length(min=16, max=16)])
    security_code = StringField('Security Code', validators=[DataRequired()])
    buyer_or_seller = SelectField('Will this account be for buying or selling?', choices = [(1, 'Selling'), (2, 'Buying')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditSellerForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('New Username', validators=[DataRequired()])
    about_seller = TextAreaField('About me', validators=[Length(min=0, max=140)])
    email = StringField('New Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', [Length(min=0, max=200)])
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat New Password', validators=[DataRequired(), EqualTo('password')])
    card_number = TextAreaField('New Card Number', [Length(min=16, max=16)])
    security_code = StringField('New Security Code', validators=[DataRequired()])
    submit = SubmitField('Submit Changes')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditSellerForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email.')

class CheckoutForm(FlaskForm):
    email = StringField('Confirm Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Confirm Address', [Length(min=0, max=200)])
    card_number = TextAreaField('Confirm Card Number', [Length(min=16, max=16)])
    security_code = StringField('Confirm Security Code', validators=[DataRequired()])
    submit = SubmitField('Checkout')

    def __init__(self, original_email, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email.')

class EditBuyerForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('New Username', validators=[DataRequired()])
    email = StringField('New Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', [Length(min=0, max=200)])
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat New Password', validators=[DataRequired(), EqualTo('password')])
    card_number = TextAreaField('New Card Number', [Length(min=16, max=16)])
    security_code = StringField('New Security Code', validators=[DataRequired()])
    submit = SubmitField('Submit Changes')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditBuyerForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email.')

class ReviewForm(FlaskForm):
    title = TextAreaField('Title', [Length(min=1, max=20)])
    body = TextAreaField('Body', validators=[Length(min=1, max=1500)])
    rating = SelectField('Rating', choices = [(1), (2), (3), (4), (5)])
    submit = SubmitField('Submit Review')

class ReportForm(FlaskForm):
    title = TextAreaField('Title', [Length(min=1, max=20)])
    body = TextAreaField('Body', validators=[Length(min=1, max=1500)])
    submit = SubmitField('Submit Report')

class SortForm(FlaskForm):
    sort_by = SelectField('Sort by...',choices = [(4,'Newest'),(3, 'Top Reviewed'), (2, 'Price: Low to High'), (1,'Price: High to Low')])
    submit = SubmitField('Refresh')

class SearchForm(FlaskForm):
    search_key = StringField('Search for', validators=[Length(min = 1, max = 100)])
    submit = SubmitField('Search')