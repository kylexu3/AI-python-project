# -*- coding: utf-8 -*-
"""AI coursework.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NK40aUZ4agLoKw0ryIRgKR7LXWdvOZpC

Linear Regression
"""

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pa
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score

# Load csv file
data = pa.read_csv('/content/coursework_other.csv')
# Split data
X = data.drop(columns=['PE'])
y = data['PE']
X_trn, X_tst, y_trn, y_tst = train_test_split(X, y, test_size=0.2, random_state=10 )
plt.plot(X,y)

# Apply linear regression and fit the model to training data
LR= LinearRegression()
LR.fit(X_trn, y_trn)

# Predict on test data and calculate mean squared error of prediction
y_prd = LR.predict(X_tst)
MSE = mean_squared_error(y_tst, y_prd)
R2= r2_score(y_tst, y_prd)

print("MSE and R2:", MSE, R2)

# Plot the result
squared_symbol = '\u00B2'
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title(f'LinearRegressor\nMSE = {MSE:.2f} R{squared_symbol}= {R2:.2f}')
plt.scatter(y_tst, y_prd, color='blue', s=2)
plt.plot(y_tst, y_tst ,color='red')

"""KNN Regression"""

from sklearn.neighbors import KNeighborsRegressor
# Data is already slipt, create knn object.
knnreg = KNeighborsRegressor(n_neighbors=7)
# Fit the model and predict
knnreg.fit(X_trn, y_trn)
y_knnprd=knnreg.predict(X_tst)
# Calculate MSE
knn_MSE = mean_squared_error(y_tst, y_knnprd)
print("knn_MSE:", knn_MSE)

# Plot the result
knn_R2= r2_score(y_tst, y_knnprd)
squared_symbol = '\u00B2'
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title(f'KNeignborsRegressor\nMSE = {knn_MSE:.2f} R{squared_symbol}= {knn_R2:.2f}')
plt.scatter(y_tst, y_prd, color='blue', s=2)
plt.plot(y_tst, y_tst ,color='red')
print("R2:", knn_R2)
plt.scatter(y_tst, y_knnprd, color='blue', s=2)
plt.plot(y_tst, y_tst ,color='red')

"""Baseline

"""

from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Create model and choose strategy
dummy_model = DummyRegressor(strategy="mean")

# Fit the model
dummy_model.fit(X_trn, y_trn)

# Prediction
dummy_predictions = dummy_model.predict(X_tst)

# Calculate mse as metric
dummy_mse = mean_squared_error(y_tst, dummy_predictions)


print("Baseline MSE:", dummy_mse)

# Plot result
plt.scatter(y_tst, dummy_predictions, color='blue', s=2)

plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('DummyRegressor MSE: 290.17')

"""Validation

"""

# Import KFold from sklearn.model_selection
from sklearn.model_selection import KFold

# Instantiate KFold with 5 splits.
# Set the parameter random_state to help you reproduce your results if needed.
X_trn = X_trn.reset_index(drop=True)
y_trn = y_trn.reset_index(drop=True)
cv = KFold(n_splits=5,random_state=10, shuffle=True)

# Set a variable max_k to 30
max_k = 30

# Inititalise two variables to store the
# training accuracies and validation accuracies
# (these need to store max_k*5 accuracies)
trainmse = [[] for _ in range(max_k)]
valmse = [[] for _ in range(max_k)]

# Loop over the values of k:
for k in range(max_k):

    # Instantiate a k-nn classifier (Use the sklearn classifier) with the current value of k
    knn = KNeighborsRegressor(n_neighbors=k+1)
    # Loop over the cross-validation splits:
    for train_index, val_index in cv.split(X_trn):
        Xtrain, Xval = X_trn.iloc[train_index].reset_index(drop=True), X_trn.iloc[val_index].reset_index(drop=True)
        Ytrain, Yval = y_trn.iloc[train_index].reset_index(drop=True), y_trn.iloc[val_index].reset_index(drop=True)
        # fit the model on the current split of data
        model=knn.fit(Xtrain, Ytrain)
        # make predictions
        Ypredtrain=model.predict(Xtrain)
        Ypredval=model.predict(Xval)
        # calculate training and validation accuracy and store
        trainmse[k].append(mean_squared_error(Ytrain, Ypredtrain))
        valmse[k].append(mean_squared_error(Yval,Ypredval))

# Calculate the mean training and validation accuracies across splits for each k
mean_train_acc = np.mean(trainmse, axis=1)
mean_val_acc = np.mean(valmse, axis=1)

x = range(1, max_k+1)
plt.plot(x, mean_train_acc, label='Training MSE')
plt.plot(x, mean_val_acc, label='Validation MSE')
plt.legend()
plt.xlabel('k')
plt.ylabel('MSE')
plt.title('K-fold Cross Validation')
# Find the index and value of the minimum validation accuracy
min_val_mse_index = np.argmin(mean_val_acc)
min_val_mse = mean_val_acc[min_val_mse_index]
min_val_k = x[min_val_mse_index]

# Plot the minimum validation accuracy as a marker
plt.scatter(min_val_k, min_val_mse, color='red', label='Minimum Validation Accuracy')

# Annotate the minimum validation accuracy value
plt.annotate(f'({min_val_k}, {min_val_mse:.4f})', (min_val_k, min_val_mse), textcoords="offset points", xytext=(0, 10), ha='center')

plt.show()

"""Validation on Linear regression"""

from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression


# Set parameters
kfold = KFold(n_splits=5, shuffle=True, random_state=42)
X_trn = X_trn.reset_index(drop=True)
y_trn = y_trn.reset_index(drop=True)
# Create model
model = LinearRegression()
smse = 0
# Implement cross validation
for train_index, val_index in kfold.split(X_trn):
    X_train, X_test = X_trn.iloc[train_index].reset_index(drop=True), X_trn.iloc[val_index].reset_index(drop=True)
    y_train, y_test = y_trn.iloc[train_index].reset_index(drop=True), y_trn.iloc[val_index].reset_index(drop=True)

    # Fit on the training model
    model.fit(X_train, y_train)

    # Predict on the testing model
    y_pred = model.predict(X_test)

    # Calculate the MSE and mean of them
    mse = mean_squared_error(y_test, y_pred)

    smse = mse+ smse
    # print metrics
    print("MSE:", mse)
print("mean", smse/5)