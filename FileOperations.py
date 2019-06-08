import sys
import csv

def CSVLoad(filename):

    #opening csv data file
    fopen = csv.reader(open(filename))
    row = []
    for i in fopen:
        row.append(i)
    total_number_of_records=len(row)-1
    partition=int(total_number_of_records*0.8)

    train=row[1:partition]
    test=row[partition:total_number_of_records]

    #first line of file contains column names    
    attributes = row[0]

    #finding index of columns
    index_to_name, name_to_index = Column_Index(attributes)

    #Storing all columns and their values in data
    data = {
        'column_name': attributes,
        'rows':train ,
        'name_to_index': name_to_index,
        'index_to_name': index_to_name
    }
    return data,test,attributes

def Column_Index(column_name):
    name_to_index = {}
    index_to_name = {}

    for i in range(0, len(column_name)):

        name_to_index[column_name[i]] = i
        index_to_name[i] = column_name[i]

    return index_to_name, name_to_index

def fileoperations():
    #At the time of running program give configuration file name as an argument 
    #Configuration files contains information about data file(.csv file).It has data file path,csv column_name/columns and target attribute   
    #Taking configuration file as an argument from command line
    argument = sys.argv

    #reading configuration file 
    with open(argument[1], 'r') as cfg_file:
        data = cfg_file.read()
    configuration_file=eval(data)
    #print(configuration_file)
    #Output:{'data_file': '/tennis.csv', 'data_mappers': [], 'data_project_columns': ['Outlook', 'Temperature', 'Humidity', 'Windy', 'PlayTennis'], 'target_attribute': 'PlayTennis'}
    
    data,test,attributes=CSVLoad(configuration_file['csv_file'])

    #data = project_columns(data, configuration_file['data_project_columns'])
    
    #Consist target attribute
    target_attribute = configuration_file['target_attribute']

    #consists remaining attributes
    remaining_attributes = data['column_name']

    #consists remaining attributes without target attribute
    remaining_attributes.remove(target_attribute)

    return data,target_attribute,remaining_attributes,test