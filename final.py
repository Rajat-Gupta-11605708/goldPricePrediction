from numpy import *
import fix_yahoo_finance as yf
import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd

#   Activation Function
def ramp(x):
    if x<0:
        return 0
    elif x==1:
        return 1
    else:
        return x

#   Initial Date for the Data Collection
init_date = '2000-1-1'

#   For setting end date as today
now = datetime.datetime.now()
#   Fromatting end_date as required format
final_date = str(now.year)+'-'+str(now.month)+'-'+str(now.day-1)
adv_date = str(now.year)+'-'+str(now.month)+'-'+str(now.day)

#   Downloading Historical data for GOLD from Yahoo Finances API
frame = yf.download('GLD', init_date, final_date)
frame2 = yf.download('GLD', init_date, adv_date)

#   Only Wanted the Closing Price
frame = frame[['Close']]
frame2 = frame2[['Close']]

#   Drop Rows with NULL Data
frame = frame.dropna()
frame2 = frame2.dropna()

# frame2.to_csv('abc.csv', encoding='utf-8')

frame.Close.plot(figsize=(10, 5))
plt.ylabel("GOLD ETF Prices")
plt.show()

frame['S_3'] = frame['Close'].shift(1).rolling(window=3).mean()
frame['S_9'] = frame['Close'].shift(1).rolling(window=9).mean()

frame2['S_3'] = frame['Close'].shift(1).rolling(window=3).mean()
frame2['S_9'] = frame['Close'].shift(1).rolling(window=9).mean()

frame = frame.dropna()
frame2 = frame2.dropna()

X = frame[['S_3', 'S_9']]
print(X)
X.head()

y = frame2['Close']
y.head()


#Split the data into train and test dataset
t = 0.8
t = int(t*len(frame))

# Train dataset
X_train = X[:t]
y_train = y[:t]

# Test dataset
X_test = X[t:]
y_test = y[t:]

#Create a linear regression model
linear = LinearRegression().fit(X_train,y_train)
print ("Linear Regression equation")
print ("Gold ETF Price (y) =", \
round(linear.coef_[0],2), "* 3 Days Moving Average (x1)", \
round(linear.coef_[1],2), "* 9 Days Moving Average (x2) +", \
round(linear.intercept_,2), "(constant)")

#Predicting the Gold ETF prices
predicted_price = linear.predict(X_test)
print(predicted_price)

for i in predicted_price:
    k = ramp(i)

print('Predicted Price : ', k)
predicted_price = pd.DataFrame(predicted_price, index=y_test.index, columns=['price'])

predicted_price.plot(figsize=(10,5))
y_test.plot()
plt.legend(['predicted_price','actual_price'])
plt.ylabel("Gold ETF Price")
plt.show()
