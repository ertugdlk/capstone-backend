from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

def output_imputation(row):
    m = 5
    halfm = m/2
    totalE = 0
    for item in row:
        displacement = item
        velocity = (displacement / 1) * 0.01
        Ekinetic = halfm * (velocity**2)
        totalE += Ekinetic
        
    return totalE

def target_df():
    df = pd.read_csv('output.csv')
    array = []
    for index, row in df.iterrows():
        E= output_imputation(row)
        liste = []
        liste.append(E)
        array.append(liste)
    
    nparray = np.asarray(array)
    newdf = pd.DataFrame(nparray, columns=['output'])
    result = pd.concat([df, newdf], axis=1)
    return result

def normalize(dataframe):
    data = dataframe
    target = data.T.tail(1).T
    testdata = data.iloc[:,:-1]
    scaler = MinMaxScaler()
    testdata = scaler.fit_transform(testdata)
    newtarget = scaler.fit_transform(target)
    newdf = pd.DataFrame(newtarget)
    
    return newdf

def scaler(dataframe):
    data = dataframe
    testdata = data.iloc[:,:-1]
    scaler = StandardScaler()
    # transform data
    scaled = scaler.fit_transform(testdata)
    scaleddf = pd.DataFrame(scaled)
    return scaleddf
    
    
dataset = target_df()
inputs = scaler(dataset)
outputs = normalize(dataset)

##Logistic Regression
X_train, X_test, y_train, y_test = train_test_split( inputs, outputs, test_size=0.2, random_state=42)
regressor = LinearRegression()
regressor.fit(X_train, y_train)
predicted = regressor.predict(X_test)
rmse = mean_squared_error(y_test.iloc[10,:], predicted[10])
print(rmse)


        

 