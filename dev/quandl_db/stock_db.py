from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

with open('../../../../rds_credentials.txt', 'r') as f:
    qcreds = [x.strip() for x in f]

#if you want a local db uncomment below (sqlite) and comment the mysql+pymysql out 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/stock_db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+qcreds[0]+':'+qcreds[1]+'@'+qcreds[2]+'/'+qcreds[3]
db = SQLAlchemy(app)

class stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True)
    maxDate = db.Column(db.DateTime, unique=False)
    minDate = db.Column(db.DateTime, unique=False)
    exists_quandl = db.Column(db.Boolean, unique=False)
    ohlcs = db.relationship('ohlc', backref='stock_symbol', lazy='dynamic')

    def __init__(self, symbol,maxDate,minDate):
        self.symbol = symbol
        self.maxDate = maxDate
        self.minDate = minDate

	def __repr__(self):
		return '<test %r>' % self.symbol + " " + self.maxDate + " " + self.minDate

class ohlc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50), unique=False)
    oCode = db.Column(db.String(50), unique=True)
    Date = db.Column(db.DateTime, unique=False)
    Open = db.Column(db.Float(asdecimal=True), unique=False)
    High = db.Column(db.Float(asdecimal=True), unique=False)
    Low = db.Column(db.Float(asdecimal=True), unique=False)
    Close = db.Column(db.Float(asdecimal=True), unique=False)
    Volume = db.Column(db.Float(asdecimal=True), unique=False)
    ExDividend = db.Column(db.Float(asdecimal=True), unique=False)
    SplitRatio = db.Column(db.Float(asdecimal=True), unique=False)
    AdjOpen = db.Column(db.Float(asdecimal=True), unique=False)
    AdjHigh = db.Column(db.Float(asdecimal=True), unique=False)
    AdjLow = db.Column(db.Float(asdecimal=True), unique=False)
    AdjClose = db.Column(db.Float(asdecimal=True), unique=False)
    AdjVolume = db.Column(db.Float(asdecimal=True), unique=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))

    def __init__(self,oCode,symbol, Date, Open, High, Low, Close, Volume,ExDividend,SplitRatio,AdjOpen,AdjHigh,AdjLow,AdjClose,AdjVolume,stock_symbol):
        self.oCode = oCode
        self.symbol = symbol
        self.Date = Date
        self.Open = Open
        self.High = High
        self.Low = Low
        self.Close = Close
        self.ExDividend = ExDividend
        self.SplitRatio = SplitRatio
        self.AdjOpen = AdjOpen
        self.AdjHigh = AdjHigh
        self.AdjLow = AdjLow
        self.AdjClose = AdjClose
        self.AdjVolume = AdjVolume
        self.stock_symbol = stock_symbol

    def __repr__(self):
        return '<ohlc %r>' % self.Date.strftime("%Y-%m-%d")
		

