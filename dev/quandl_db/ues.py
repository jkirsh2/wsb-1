from quandl import Quandl

q= Quandl()
# Scrape single date
stock = q.stock_scrape_date("AMD","2017-10-16")
for i in stock:
	print "Symbol: " + i.symbol
	print "Date: " + str(i.Date)
	print "Open: " + str(i.Open)
	print "High: " + str(i.High)
	print "Low: " + str(i.Low)
	print "Close: " + str(i.Close)

# Scrape date range
stock = q.stock_scrape_date_range("AMD","2017-10-16","2017-10-18")
for i in stock:
	print "Symbol: " + i.symbol
	print "Date: " + str(i.Date)
	print "Open: " + str(i.Open)
	print "High: " + str(i.High)
	print "Low: " + str(i.Low)
	print "Close: " + str(i.Close)
	print "Volume: " + str(i.Volume)
	print "ExDividend: " + str(i.ExDividend)
	print "SplitRatio: " + str(i.SplitRatio)
	print "AdjOpen: " + str(i.AdjOpen)
	print "AdjHigh: " + str(i.AdjHigh)
	print "AdjLow: " + str(i.AdjLow)
	print "AdjClose: " + str(i.AdjClose)
	print "AdjVolume: " + str(i.AdjVolume)

