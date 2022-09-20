from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Max is curious about SandP + BTC corellation

# read cv up until specified date
csv = pd.read_csv("BTC-PERP.csv")

# Convert csv date format to datetime
csv["Date"] = pd.to_datetime(csv["startTime"].str.split('T').str[0])

# Group by dates by averaging relative numbers
btc = csv.groupby('Date').mean()
# Get SandP data
voo = yf.Ticker('voo')
sap = voo.history(start='2019-07-20', end='2022-08-17')

# Merge btc and sap based on dates since sap will not have price everyday of year
# (matchup with btc dates)
combined = pd.merge(btc, sap, on="Date")

X = np.array(combined['Close']).reshape(-1, 1)
Y = np.array(combined['close']).reshape(-1, 1)

# Split up data: train, test
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

model = LinearRegression()
model.fit(x_train, y_train)

plt.scatter(x_test, y_test)

pred = model.predict(x_test)

plt.plot(x_test, pred, color="red")

# Model coefficient
print(model.coef_)
# % accuracy
print(model.score(x_test, y_test))

plt.show()
