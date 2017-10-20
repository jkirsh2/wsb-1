"""Script to run the analysis with all the parameters

Authors: Joe Kirsh, Casey Emmons, Andrew Mehrmann
"""

from RETF.portfolio.index import portfolio_constructor
import datetime as dt
import matplotlib.pyplot as plt


# parameters...these should be in a config file
subr = 'wallstreetbets'
cp = 'RETF/credentials.txt'
start_date = '2017-06-15'
end_date = '2017-06-25'
lookback = 20
cutoff = 0.02
start_price = 69



def str_to_dt(s):
    return dt.datetime.strptime(s, '%Y-%m-%d')


pc = portfolio_constructor(subr, cp, cutoff=cutoff)

d0 = str_to_dt(start_date)
d1 = str_to_dt(end_date)

pdict = pc.get_portfolio_dict(d0, d1, lookback)
tlist = pc.get_ticker_list(pdict)

print(tlist)
cpdict, dl = pc.get_close_price_dict(d0, d1, tlist)

pdict = pc.drop_tickers(pdict, dl)

pdict, idict = pc.get_portfolio_change(pdict, cpdict)

i = [start_price]
for d in idict:
    i.append(i[-1] * (idict[d] + 1))

plt.plot(list(idict.keys()), i[1:])
plt.show()
