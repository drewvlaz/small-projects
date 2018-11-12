import pandas as pd
import sqlite3
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt

connection = sqlite3.connect('data/iris/database.sqlite')
data = pd.read_sql_query('SELECT * FROM Iris', connection)

# print(data['Species'].value_counts())

# remove redundant column
del data['Id']

# create list of features to train on
features = []
for col in list(data.columns):
    if 'Species' not in col:
        features.append(col)


# create the features and target datasets
X = data[features]
y = data['Species']

# one-hot encode
y = pd.get_dummies(y)

# split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.37, random_state=324)

# determine regression type and create model
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# use model to predict flower type
y_predictions = regressor.predict(X_test)

# print the root mean squared error
RMSE = sqrt(mean_squared_error(y_true = y_test, y_pred = y_predictions))
print(f"Linear Regression RMSE:{RMSE}")

# determine regression type and create model
regressor = DecisionTreeRegressor(max_depth=10)
regressor.fit(X_train, y_train)

# use model to predict the flower type
y_predictions = regressor.predict(X_test)

# print the root mean squared error
RMSE = sqrt(mean_squared_error(y_true = y_test, y_pred = y_predictions))
print(f"Decision Tree Regressor RMSE:{RMSE}")
