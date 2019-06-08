############################################################## created by Anirudha Nilegaonkar ##############################################################

############################################################# Date: 09/16/2018 ###############################################################
import math

def YesNoCounter(file_data, target_attribute):
    rows = file_data['rows']
    #stores index of target attribute
    column_idx = file_data['name_to_index'][target_attribute]

    labels = {}
    for row in rows:
        value = row[column_idx]
        if value in labels:
            labels[value] = labels[value] + 1
        else:
            labels[value] = 1
    return labels

def entropy(n, labels): 
    entropy = 0
    for label in labels.keys():
        probability_of_value = labels[label] / n
        #formula for calculating entropy
        if(probability_of_value != 0):
            entropy += -probability_of_value * math.log(probability_of_value)/math.log(2)
    return entropy

def partition_data(data,remaining_attribute ):
    partitions = {}
    data_rows = data['rows']
    partition_attribute_index = data['name_to_index'][remaining_attribute]
    
    for row in data_rows:
        row_value = row[partition_attribute_index]
        if row_value not in partitions.keys():
            partitions[row_value] = {
                'name_to_index': data['name_to_index'],
                'index_to_name': data['index_to_name'],
                'rows': list()
            }
        partitions[row_value]['rows'].append(row)
    return partitions

def AttributeAverageEntropyCalculator(file_data,remaining_attribute, target_attribute):

    data_rows = file_data['rows']
    n = len(data_rows)
    #It consists attribute and it's value with csv data
    partitions = partition_data(file_data,remaining_attribute)
    avg_entropy = 0

    #calculate entropy for each value of attributes
    for partition_key in partitions.keys():
    	#Selects all rows which consists particular key  
    	data_with_partition = partitions[partition_key]
    	partition_length = len(data_with_partition['rows'])
    	partition_labels =YesNoCounter(data_with_partition, target_attribute)
    	partition_entropy = entropy(partition_length, partition_labels)
    	avg_entropy += partition_length / n * partition_entropy

    #it will return Average entropy and partition of particular attribute
    return avg_entropy, partitions

def most_common_label(labels):
    mcl = max(labels, key=lambda k: labels[k])
    return mcl


def id3(file_data,attribute_values, remaining_attributes, target_attribute):

	#To find number of YES and NO's of Target attribute.Key=target attribute & Value=number of YES and NO's
    labels = YesNoCounter(file_data, target_attribute)
    node = {}

    if len(labels.keys()) == 1:
        node['label'] = next(iter(labels.keys()))
        return node

    if len(remaining_attributes) == 0:
        node['label'] = most_common_label(labels)
        return node

    #Represents total number of data
    n = len(file_data['rows'])
    
    #calculating entropy
    Entropy = entropy(n, labels)
    #print(Entropy)


    max_information_gain = None
    max_information_gain_attribute = None
    max_information_gain_partitions = None

    for remaining_attribute in remaining_attributes:
        avg_entropy, partitions = AttributeAverageEntropyCalculator(file_data,remaining_attribute, target_attribute)
        information_gain = Entropy - avg_entropy
        #Calculating maximum information gain attribute
        if max_information_gain is None or information_gain > max_information_gain:
            max_information_gain = information_gain
            max_information_gain_attribute = remaining_attribute
            max_information_gain_partitions = partitions

    if max_information_gain is None:
        node['label'] = most_common_label(labels)
        return node

    node['attribute'] = max_information_gain_attribute
    node['nodes'] = {}
    remaining_attributes_for_subtrees = remaining_attributes
    remaining_attributes_for_subtrees.remove(max_information_gain_attribute)
    #shows values of selected node attribute
    node_attribute_values = attribute_values[max_information_gain_attribute]

    #print(max_information_gain_partitions.keys())
    for attribute_value in node_attribute_values:
        if attribute_value not in max_information_gain_partitions.keys():
            node['nodes'][attribute_value] = {'label': most_common_label(labels)}
            #print(node['nodes'][attribute_value])
            continue
        #running ID3 in attribute values    
        partition = max_information_gain_partitions[attribute_value]
        node['nodes'][attribute_value] = id3(partition,attribute_values,remaining_attributes_for_subtrees,target_attribute)

    return node

