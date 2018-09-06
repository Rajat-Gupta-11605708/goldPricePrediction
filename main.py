from numpy import *
import fix_yahoo_finance as yf
import datetime


init_date = '2000-1-1'                                                                          #   Initial Date for the Data Collection
now = datetime.datetime.now()                                                                   #   For setting end date as today
end_date = str(now.year)+'-'+str(now.month)+'-'+str(now.day)                                    #   Fromatting end_date as required format
frame = yf.download('GLD',init_date, end_date)                                                  #   Downloading Historical data for GOLD from Yahoo Finances APU
frame = frame[['Close']]                                                                        #   Only Wanted the Closing Price
frame = frame.dropna()                                                                          #   Drop Rows with NULL Data
