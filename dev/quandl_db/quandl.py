import requests
import json
import datetime
from stock_db import db,stock,ohlc
from sqlalchemy import desc
from sqlalchemy.sql import exists

db.create_all()

class Quandl:
	def __init__ (self):
		self.first_part = "https://www.quandl.com/api/v3/datasets/WIKI/"
		self.mid_part =  "/data.json?start_date="
		self.mid_part2 = "&end_date="
		self.last_part = "&order=asc&api_key=Q7DSNVGYPQ9WnMmxEgVb"
	def scrape_date_range(self,symbol,start_date,end_date):
		link = self.first_part + symbol + self.mid_part+ str(start_date) + self.mid_part2+ str(end_date)+self.last_part
		r = requests.get(link)
		quandl_stock_json = r.json()
		s = stock.query.filter_by(symbol=symbol).first()
		try:
			data = quandl_stock_json['dataset_data']['data']
			s=stock.query.filter_by(symbol=symbol).first()

			for i in range(0,len(data)):
				o = ohlc(oCode=symbol+str(data[i][0])
					, symbol = symbol
					, Date=datetime.datetime(int(data[i][0][0:4]),int(data[i][0][5:7]),int(data[i][0][8:10]))
					, Open = data[i][1]
					, High = data[i][2]
					, Low = data[i][3]
					, Close = data[i][4]
					, Volume =data[i][5]
					, ExDividend = data[i][6]
					, SplitRatio = data[i][7]
					, AdjOpen = data[i][8]
					, AdjHigh = data[i][9]
					, AdjLow = data[i][10]
					, AdjClose = data[i][11]
					, AdjVolume =data[i][12]
					, stock_symbol = s) 
				db.session.add(o)
				try:
					db.session.commit()	
					s.exists_quandl = True
				except Exception,e:
					db.session.rollback()
					print str(e)
					pass
		except Exception,e:
			print str(e)
			s.exists_quandl = False
			print("stock doesn't exist with quandl")
			pass
		commited = self.commit_stock(s)
		return True

	def stock_scrape_date(self,symbol,date):
		exists = db.session.query(stock.id).filter_by(symbol=symbol).scalar() is not None
		d = datetime.datetime(int(date[0:4]),int(date[5:7]),int(date[8:10]))
		if d.weekday() in (5, 6):
			print("weekend")
			stock_export = []
		else:
			if exists:
				s = stock.query.filter_by(symbol=symbol).first()
				if s.exists_quandl:
					stock_export = self.range_exists(symbol,d,d)
				else:
					print('Stock not in quandl')
					stock_export = []
			else:
				s = stock(symbol=symbol,maxDate=d,minDate=d)
				commited = self.commit_stock(s)
				test = self.scrape_date_range(symbol,d,d)
				stock_export = self.return_range(symbol,d,d)

		return stock_export

	def stock_scrape_date_range(self,symbol,start_date,end_date):
		exists = db.session.query(stock.id).filter_by(symbol=symbol).scalar() is not None
		sd = datetime.datetime(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:10]))
		ed = datetime.datetime(int(end_date[0:4]),int(end_date[5:7]),int(end_date[8:10]))
		if exists:
			s = stock.query.filter_by(symbol=symbol).first()
			if s.exists_quandl:
				stock_export = self.range_exists(symbol,sd,ed)
			else:
				print('Stock not in quandl')
				stock_export = []
		else:
			s = stock(symbol=symbol,maxDate=ed,minDate=sd)
			commited = self.commit_stock(s)
			test = self.scrape_date_range(symbol,sd,ed)
			stock_export = self.return_range(symbol,sd,ed)
		return stock_export

	def range_exists(self,symbol,sd,ed):
		s = stock.query.filter_by(symbol=symbol).first()
		if sd < s.minDate and ed > s.maxDate: 
			data_scrape1 = self.scrape_date_range(symbol,s.maxDate + datetime.timedelta(days=1),ed)
			data_scrape2 = self.scrape_date_range(symbol,sd,s.minDate + datetime.timedelta(days=-1))
			s.maxDate = ed
			s.minDate = sd
			commited = self.commit_stock(s)
			stock_range=self.return_range(symbol,sd,ed)
		elif sd < s.minDate and ed <= s.maxDate:
			data_scrape = self.scrape_date_range(symbol,sd,s.minDate + datetime.timedelta(days=-1))
			s.minDate = sd
			commited = self.commit_stock(s)
			stock_range=self.return_range(symbol,sd,ed)
		elif sd >= s.minDate and ed > s.maxDate:
			data_scrape = self.scrape_date_range(symbol,s.maxDate + datetime.timedelta(days=1),ed)
			s.maxDate = ed
			commited = self.commit_stock(s)
			stock_range=self.return_range(symbol,sd,ed)
		else:
			stock_range=self.return_range(symbol,sd,ed)
		return stock_range

	def return_range(self,symbol,start_date,end_date):
		arr=[]
		rr = ohlc.query.filter(ohlc.symbol==symbol).filter(ohlc.Date >=start_date).filter(ohlc.Date <=end_date).order_by(desc(ohlc.Date))
		for i in rr:
			arr.append(i)
		return arr

	def commit_stock(self,stock):
		db.session.add(stock)
		db.session.commit()
		return True


		
