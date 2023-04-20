

# dependencies
from flask import Flask, render_template, jsonify, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
#import bcrypt

# app initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
#salt = bcrypt.gensalt()

# database initialization
db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# database models

# junction table for payments
payments_table = db.Table(
    'payment',
    db.Column('payer_id', db.Integer, db.ForeignKey('payer.id'), primary_key=True),
    db.Column('payee_id', db.Integer, db.ForeignKey('payee.id'), primary_key=True),
    db.Column('amount', db.Float),
    db.Column('mpesa_code', db.String(20), nullable=False),
    db.Column('transaction_fee', db.Float, nullable=False),
    db.Column('timestamp', db.DateTime, default=datetime.utcnow),
    db.Column('payment_list_id', db.Integer, db.ForeignKey('payment_list.id'))
)

# payment lists model
class PaymentList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10), nullable=False)
    payer_id = db.Column(db.Integer, db.ForeignKey('payer.id'))

# deposit model 
class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    payer_id = db.Column(db.Integer, db.ForeignKey('payer.id'))

# payer model
class Payer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    current_balance = db.Column(db.Float, nullable=False, default=0)
    payments = db.relationship('Payee', secondary=payments_table, backref='payers')

    def verify_password(self, password):
        return self.password == password

# payee model
class Payee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    amount_payable = db.Column(db.Float, nullable=False, default=0)
    payer_id = db.Column(db.Integer, db.ForeignKey('payer.id'))
    payments = db.relationship('Payer', secondary=payments_table, backref='payees')

#database creation
with app.app_context():
	db.create_all()


#authentication initialization
auth = HTTPBasicAuth()

# HTTP Basic Auth decorator
@auth.verify_password
def verify_password(username, password):
    user = Payer.query.filter_by(email=username).first()
    if not user or not user.verify_password(password):
        return False
    return True
 
# utility functions

# ToDo
# Implement a database
# Implement login and access control
# Implement Safaricom Daraja API Business2Clients

# Goals
# Our aim is to intergrate with safaricom API's to create a third party bulk disbursement service that is reliable, user friendly, secure, and affordable
# A user can only deposit to our paybill, create payees lists and run payments at any time
# Our revenue is 0.25% of the total amount transferred


# routes and view functions
@app.route("/")
def index():
    return render_template("index.htm")

@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    if request.method == "POST":
        payerX = Payer(email=request.form['email'], phone_number=request.form['phone_number'], password=request.form['password'])
        db.session.add(payerX)
        db.session.commit()
        return jsonify({'message':'user successfully added'})
    else:
        return render_template("create_account.htm")

@app.route("/login")
def login():
    return render_template("login.htm")

@app.route("/add_payee", methods=['GET', 'POST'])
def add_payee():
    return render_template("add_payee.htm")


# sample protected route
@app.route('/protected')
@auth.login_required
def protected():
    return jsonify({'message': 'You are allowed'})
