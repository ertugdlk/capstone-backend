import pandas as pd
import csv
import math
import os

new_list = []

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

def write_csv(dataframe):
    f = open('modelrecord.csv', 'a')  
    writer = csv.writer(f)
    liste = []
    for index, row in dataframe.iterrows():
        x= float("{0:.2f}".format(row['x']))
        y= float("{0:.2f}".format(row['y']))
        vector = math.sqrt(x**2 + y**2)
        liste.append(vector)
        
    E = output_imputation(liste)
    liste.append(E)
    # write a row to the csv file
    writer.writerow(liste)
    # close the file
    f.close()

def chunk_merge(new_list, chunk, first_x , first_y):
    last_row = chunk.tail(1)
    
    x_maxdiff = abs(chunk['x'].max() - first_x )
    x_mindiff = abs(chunk['x'].min() - first_x)
    
    y_maxdiff = abs(chunk['y'].max() - first_y)
    y_mindiff = abs(chunk['y'].min() - first_y)

    x_mean = x_maxdiff + x_mindiff
    y_mean = y_maxdiff + y_mindiff
    time = last_row['TIME']
    
    row = { 'time': time,
           'y': y_mean,
           'x': x_mean}
    new_list.append(row)


def check_chunks(csv_dataframe):
    counter = 0
    first_row = csv_dataframe.iloc[1]
    first_x= first_row['x']
    first_y = first_row['y']
    
    #Check first 100 rows inside the dataframe
    while(counter < 90):
        chunk = csv_dataframe.iloc[counter:counter + 10]
        
        #Chunk length must greater than 10
        if(len(chunk) < 10):
            return
        
        chunk_merge(new_list, chunk , first_x, first_y)
        counter += 10
    
    new_df = pd.DataFrame(new_list, columns=['time', 'x', 'y'])
    return new_df
    

path = "/Users/ertugdilek/Desktop/SensorDataSet10Sec"
dirs = os.listdir(path)
    
for file in dirs:
    ext = file.split('.')
    if ext[1] == 'csv' and ext[0] != 'modelrecord':
        print(file)
        csv_dataframe = pd.read_csv(file)
        new_df = check_chunks(csv_dataframe)
        write_csv(new_df)
        new_list= []   
            
print('Successful. Train dataset created from csv files.') 
    