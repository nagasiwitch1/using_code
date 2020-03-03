import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_finance import *
import FinanceDataReader as fdr
from pandas.core.common import SettingWithCopyWarning
import warnings

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

# use ticker1 variable for plot label.
ticker1 = 'Bitcoin'
observation_period = 1000

# read csv data
path = './ib_db/' + 'INDU_20200301_10Y_1day' + '.csv'
MA_num = [5, 120, 200, 967]

# want to draw SMA lines,  use longer period of data.
# set raw_  at first,  and slicing data to raw_data

raw_ = pd.read_csv(path, index_col='Date')
raw_.index = pd.to_datetime(raw_.index)

# or I can use Financial DataReaders data
# https://github.com/FinanceData/FinanceDataReader/wiki/Users-Guide
# WTI : CL , KOSPI: KS11 , KOSDAQ : KQ11 , VIX : VIX , Gold : GC , Bond : US10YT=X , KR10YT=RR , currency : BTC/KRW
raw_ = fdr.DataReader('BTC/USD', '2015')

# convert date to num for using
raw_data = raw_.iloc[observation_period:, :]
raw_data.index = pd.to_datetime(raw_data.index)
raw_data['Datetonum'] = [mdates.date2num(d) for d in raw_data.index]

# Re-arrange data so that each row contains values of a day for candlestick's quote:
# 'date','open','high','low','close'.
quote = [tuple(x) for x in raw_data[['Datetonum', 'Open', 'High', 'Low', 'Close']].values]

# SMA_data  using rolling in pandas
SMA_data_ = pd.DataFrame(index=raw_.index)
for g in range(len(MA_num)):
    SMA_data_[str(MA_num[g]) + 'MA'] = raw_['Close'].rolling(MA_num[g]).mean()
SMA_data = SMA_data_.iloc[observation_period:, :]

# visualize candle
fig, ax = plt.subplots(figsize=(14,8))
candlestick_ohlc(ax, quote, width=0.05, colorup='g', colordown='r')

# visualize SMA data. using specific color by MAs
MA_120 = ax.plot(SMA_data.iloc[:, 1], linewidth=0.5, color='b', label='120MA')
MA_200 = ax.plot(SMA_data.iloc[:, 2], linewidth=0.5, color='r', label='200MA')
MA_200w = ax.plot(SMA_data.iloc[:, 3], linewidth=0.5, color='pink', label='200W-MA')


# annotate 120MA
ax.annotate(int(SMA_data.iloc[-1, 1]), color='b', fontsize=7,
                     xy=(SMA_data.index[-1], SMA_data.iloc[-1, 1]+2))

# annotate 200MA
ax.annotate(int(SMA_data.iloc[-1, 2]), color='r', fontsize=7,
                     xy=(SMA_data.index[-1], SMA_data.iloc[-1, 2]))

# annotate 200week MA
ax.annotate(int(SMA_data.iloc[-1, 3]), color='pink', fontsize=7,
                     xy=(SMA_data.index[-1], SMA_data.iloc[-1, 3]))


# annotate last_price
ax.annotate(int(raw_data['Close'][-1]), color='k', fontsize=9,
                     xy=(raw_data.index[-1], raw_data['Close'][-1]), label='Current')

# axes setting
ax.set_ylabel(ticker1, color='g')
ax.yaxis.tick_right()
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

# grid
ax.grid(which='major', axis='both', color='gray', dashes=(2, 4), linewidth=0.2)

# Beautify the x-labels
plt.legend()
plt.gcf().autofmt_xdate()
plt.autoscale()
plt.tight_layout()
plt.savefig('./charts/' + ticker1 + str(observation_period) + 'SMA.png')
plt.show()
