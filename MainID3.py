############################################################## created by Anirudha Nilegaonkar(IST) ##############################################################

############################################################# Date: 09/16/2018 ###############################################################
#Importing function from 
import FileOperations as fo
import algoID3 as algo
import numpy as np
import predict as pre

'''
This function is used to create decision rules. 
    parameters used:
        node= It is a dictionary and contains structure of entire tree.
'''
def tree(node):
    #Stack is used to create decision rule
    stack = []
    rules=[]
    decision=set()
    #rules=np.array(rules)
    #rulesSet function gives set of rules drawn from decision tree.
    def tree_traverse(node, stack):
        #Append label to node.
        if 'label' in node:
            #Append label to node.
            stack.append(' THEN ' + node['label'])
            #Performing transformation for calculations.
            #print(stack)
            decision.add(''.join(stack))
            rule=np.array(stack)
            rule.tolist()
            #Print tree.
            rules.append(rule)
            #printTree(rule)
            stack.pop()
        elif 'attribute' in node:
            #Append attribute to stack
            ifstatement = 'IF ' if not stack else ' AND '
            stack.append(ifstatement + node['attribute'] + ' EQUALS ')
            #Iterating through attribute subnodes(attribute values)
            for subnode in node['nodes']:
                #Append subnode to stack
                stack.append(subnode)
                #Iterating through subnodes
                tree_traverse(node['nodes'][subnode], stack)
                stack.pop()
            stack.pop()

    tree_traverse(node, stack)
    #Consists all rules 
    rules=np.array(rules)
    #print(rules)
    printTree(rules)

'''
    print tree
    parameters used:
        rule= It is a array of strings which represents decision rule
'''
def printTree(rules):    
    #Required for storing previous results
    temp=""
    temp1=""
    temp2=""
    temp3=""

    #Used for decision making
    flag=0
    
    #Considering one rule at a time
    for rule in (rules):
        #Finiding poisition of decision in a rule array
        decision_position=len(rule)-1
        #Calculating number of attributes in a rule array
        number_of_attributes=int((len(rule)-1)/2)        
       
        #Looping through number of attributes in a rule 
        for i in range(number_of_attributes):
            
            if(i==0):
                #Checking previous rule and current rule
                if(temp!=(rule[i]+rule[i+1])):
                    print(rule[i]+rule[i+1])
                    #Storing result
                    temp=rule[i]+rule[i+1]
                    flag=0
                else:
                    flag=1

            elif(i==1):
                #Checking previous rule and current rule
                if(temp1!=(rule[i+1]+rule[i+2])):
                    print('\t'+rule[i+1]+rule[i+2]) 
                    #Storing result 
                    temp1=rule[i+1]+rule[i+2] 
                    flag=0
                else:
                    flag=1    
            elif(i==2):
                #Checking previous rule and current rule
                if(temp2!=(rule[i+2]+rule[i+3])):
                    print('\t\t'+rule[i+2]+rule[i+3]) 
                    #Storing result 
                    temp2=rule[i+2]+rule[i+3]
                    flag=0
                else:
                    flag=1
            elif(i==3):
                #Checking previous rule and current rule
                if(temp3!=(rule[i+3]+rule[i+4])):
                    print('\t\t\t'+rule[i+3]+rule[i+4]) 
                    #Storing result 
                    temp3=rule[i+3]+rule[i+4]
                    flag=0
                else:
                    flag=1
        if(flag==0):
            print('\t\t\t\t'+rule[decision_position])


def AttributeValueFinder(data):
    #contains columns and their value
    index_to_name = data['index_to_name']
    #contains only index
    indexs = index_to_name.keys()

    #Key is attribute and value is value of attribute(key,value)
    value_map = {}
    #Defining map
    for index in indexs:
        value_map[index_to_name[index]] = set()

    #adding elements in map
    for data_row in data['rows']:
        for index in indexs:
            attribute_name = index_to_name[index]
            value = data_row[index]
            if value not in value_map.keys():
                value_map[attribute_name].add(value)
    
    return value_map

def main():
	
	
    file_data,target_attribute,remaining_attributes,test=fo.fileoperations()

    test=np.array(test)

    index_of_decision_attribute=len(test[0])-1

    total_number_of_records=len(test)

    X_test=test[0:total_number_of_records,0:index_of_decision_attribute]
    
    #Y_test =Testing data which contains decision attribute values
    Y_test=test[0:total_number_of_records,index_of_decision_attribute]  
    
    #stores attribute and their values(columns)
    attribute_values = AttributeValueFinder(file_data)

    node = algo.id3(file_data,attribute_values, remaining_attributes, target_attribute)

    tree(node)
    file_data,target_attribute,remaining_attributes,test=fo.fileoperations()

    attributes=[]
    attributes.extend(remaining_attributes)
    attributes.append(target_attribute)

    #Predicting and finding accuracy.
    Accuracy=pre.predict(X_test,Y_test,attributes,remaining_attributes,index_of_decision_attribute,node)
    print("Accuracy is: "+repr(Accuracy)+" %")


main()

