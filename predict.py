import numpy as np
#Gobal array which represents decision attribute values drawn for X_test data 
X_test_decision=[]

'''
This function is used to predict the decision atrribute value by using X_test data.  
Parameters used are:
    X_test =Testing data which contains attribute values excluding decision attribute values
    Y_test =Testing data which contains decision attribute values
    attributes=It is a array of attribute values
    remaining_attributes=It is a array which contains attributes other than decision attribute.
    index_of_decision_attribute=Represents index of decision attribute in a dataset.
    node=It is a dictionary which contains decision tree
'''
def predict(X_test,Y_test,attributes,remaining_attributes,index_of_decision_attribute,node):
    #Stack is used to draw decisions from tree
    stack = []
    rules=[]
    #rulesSet function gives set of rules drawn from decision tree.
    def rulesSet(node, stack):
        #creating rule list
        rule=[]

        #If node contains label,this means that this is the end of one decision rule.
        if 'label' in node:
            #Append label to node.
            stack.append(node['label'])
            #Performing transformation for calculations.
            rule=np.array(stack)
            rule.tolist()
            rules.append(rule)
            #Drawing decision atrribute value by using decision rule. 
            #drawDecision(X_test,Y_test,attributes,remaining_attributes,index_of_decision_attribute,rule)
            stack.pop()
        elif 'attribute' in node:
            #Append attribute to stack
            stack.append(node['attribute'])
            #Iterating through attribute subnodes(attribute values)
            for subnode in node['nodes']:
                #Append subnode to stack
                stack.append(subnode)
                #Iterating through subnodes
                rulesSet(node['nodes'][subnode], stack)
                stack.pop()
            stack.pop()

    rulesSet(node,stack)
    rules=np.array(rules)
    decision=drawDecision(X_test,Y_test,attributes,remaining_attributes,index_of_decision_attribute,rules)
    Accuracy=accuracy(Y_test,decision)

    return Accuracy
'''
    Drawing decision atrribute value by using decision rule
    Parameters used:
        X_test =Testing data which contains attribute values excluding decision attribute values
        Y_test =Testing data which contains decision attribute values
        attributes=It is a array of attribute values
        remaining_attributes=It is a array which contains attributes other than decision attribute.
        index_of_decision_attribute=Represents index of decision attribute in a dataset.
        node=It is a dictionary which contains decision tree

'''
def drawDecision(X_test,Y_test,attributes,remaining_attributes,index_of_decision_attribute,rules):
    #print()
    k=0
    rule_info={}
    for rule in rules:

        #Calculating number of attributes in a rule array
        number_of_attributes=int((len(rule)-1)/2)
    
        #Finiding attributes in a rule
        attribute=[]
        for i in range(number_of_attributes):
            attribute.append(rule[i*2])

        #Finiding poisition of decision in a rule array
        decision_position=len(rule)-1
        index=[]
    
        #Gives index of attributes that are considered for decision in a decision rule
        for i in range(len(attribute)):
            count=0
            for j in range(len(remaining_attributes)):
                if remaining_attributes[j]==attribute[i]:
                    break
                count+=1
            index.append(count)

        #Drawing attribute values in a rule
        #In every rule array,odd index shows attribute values
        values=[]
        for i in range(len(index)):
            values.append(rule[(i*2)+1]) 
    
        #if j not in rule_info.keys():
        rule_info[k] = {
            'number_of_attributes':number_of_attributes,#list(),
            'attribute':attribute,#list(),
            'decision_position':decision_position,#list(),
            'index':index,#list(),
            'values':values#list()
        }
        #rule_info[k]['number_of_attributes'].append(number_of_attributes)
        #rule_info[k]['attribute'].append(attribute)
        #rule_info[k]['decision_position'].append(decision_position)
        #rule_info[k]['index'].append(index)
        #rule_info[k]['values'].append(values)
        k+=1

    #Represents decision for each X_test
    decision={}
    
    #Predicting values for test data
    for i in range(len(X_test)):
        #Checking for all rules
        for j in range(len(rule_info)):
            #Used for decision making
            flag=0
            #Represents attribute values which are required for matching decision rule 
            X_test_attribute_value=[]            
            #Stroing X_test attribute values 
            for k in rule_info[j]['index']:
                X_test_attribute_value.append(X_test[i,k])
            
            #Comparing values of X_test attributes and decision rule attribute values 
            z=0
            for v in rule_info[j]['values']:
                if (X_test_attribute_value[z]==v): 
                    z+=1
                    flag=0
                else:
                    #If one attibute value is new and not matching,considering which are matching.
                    if(z>=(len(rule_info[j]['values'])-1)):
                        flag=0
                        break
                    else:
                        flag=1
                        break
            if(flag==0):
                #Considering rule for which Attribute values are matched
                rule=rules[j]
                decision_position=rule_info[j]['decision_position']
                #Storing results 
                decision[i] = {
                    'decision':rule[decision_position]
                }     
    return decision

'''
    Calculating accuracy
    Parameters used:
        Y_test=Testing data which contains decision attribute values
        X_test_decision=Gobal array which represents decision attribute values drawn for X_test data 
'''
def accuracy(Y_test,decision):
    correct = 0
    #print("Y_test"+repr(len(Y_test))+"Decision"+repr(len(decision)))
    for i in range(len(Y_test)):
        if Y_test[i] == decision[i]['decision']:
            #Finding correctness 
            correct += 1
    return (correct/float(len(Y_test))) * 100.0     
