import numpy as np

class Node:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.title = ''
        self.branch_name = ''

    def add_child(self, obj):
        self.children.append(obj)

    def add_node_title(self, title):
        self.title = title

    def get_node_title(self):
        if self.title != '':
            return self.title
        return None
    
    def add_branch_name(self, name):
        self.branch_name = name

    def get_branch_name(self):
        if self.branch_name != '':
            return self.branch_name
        return None

    def get_data(self):
        return self.data


data = [[ 'sunny', "sunny", 'overcast', 'rain', 'rain', 'rain', 'overcast', 'sunny', 'sunny', 'rain', 'sunny', 'overcast', 'overcast' ],
        [ 'hot', 'hot', 'hot', 'mild', 'cool', 'cool', 'cool', 'mild', 'cool', 'mild', 'mild', 'mild', 'hot' ],
        [  'high', 'high', 'high', 'high', 'normal', 'normal', 'normal', 'high', 'normal', 'normal', 'normal', 'high', 'normal'],
        [ 'false', 'true', 'false', 'false', 'false', 'true', 'true', 'false', 'false', 'false', 'true', 'true', 'false']
        ]
data = np.array(data)

Decision = np.array([ 'n', 'n', 'p', 'p', 'p', 'n', 'p', 'n', 'p', 'p', 'p', 'p', 'p'])

titles = np.array(['Outlook', 'Temprature', 'Humidity', 'Windy'])



#Calculates entropy of the specified list.
def entropy(attribute_list):

    result = 0
    values, amounts = np.unique(attribute_list, return_counts=True)

    #basically (p/(p+n)) and (n/(p+n)) are being premptivily calculated in this step and stored in a new array.
    fraction_amounts = amounts / len(attribute_list)

    for i in fraction_amounts:
        if i != 0:
            result-= i * np.log2(i)
    return result


#stores each values' indices from the attribute list in a dictionary structure.
def split(attribute):
    
    indices ={}

    for i in np.unique(attribute):
        indices[i] = np.where(attribute == i)[0]
        
    return indices


# returns a gain value for the attribute list.
def info_gain(class_attribute,  attribute):
    result = entropy(class_attribute)
    #splitting the selected attributes by the different values and also having the amount of times each type of value occurs stored in fraction_amounts.
    values, amounts = np.unique(attribute, return_counts=True)
    fraction_amounts = amounts / len(attribute)

    # Finds entropy of each attribute list the entropy function is passed a list of class_attribute values in a list
    # that are split apart depending upon the value at each position, so if windy is true it finds all p and n's for that value and multiplies it by i
    # which is the total amount of times the value appears in the list.
    for i, j in zip(fraction_amounts, values):
        result-= i * entropy(class_attribute[attribute == j])
    return result


def isPure(class_attribute):
    class_attribute = np.unique(class_attribute)

    if len(class_attribute) == 1:
        return 1
    return None


def recursive_tree_creation(attributes, class_attribute, titles):
    
    #base case
    if(len(class_attribute) == 0 or isPure(class_attribute)):
        return Node(class_attribute)

    all_gains = np.zeros(len(attributes))
    #change this range since you have to cut attributes off
    for i in range (0, len(attributes)):
        all_gains[i] = info_gain(class_attribute, attributes[i])
    
    if np.all(all_gains < 1e-6):
       return Node(class_attribute)

    selected_attribute = np.argmax(all_gains)
    
    dict = split(attributes[selected_attribute])

    Title = titles[selected_attribute]
    
    #deletes the selected attribute from the data
    attributes = np.delete(attributes, selected_attribute, axis=0)
    titles = np.delete(titles, selected_attribute, axis=0)
  
    root = Node(class_attribute)
    root.title = Title

    for i, j in dict.items():
        class_attribute_subset = class_attribute[j]

        # create a new data array with the selected attribute column removed.
        new_data = np.empty([len(attributes), len(j)]) 
        new_data = np.ndarray.tolist(new_data) 

        for t in range(0, len(attributes)):
            new_data[t] = attributes[t][j]

        new_data = np.array = new_data
        #recursive step to create tree and pass in split data after.
        child = recursive_tree_creation(new_data, class_attribute_subset, titles)
        child.add_branch_name(i)
        root.add_child(child)
    return root

# prints each node and its values, also labels terminal nodes and gives total amount of nodes.
def print_tree(node, counter = 0):

    #base case and for terminal nodes printing
    if len(node.children) == 0:
        print("Branch:", node.branch_name)
        node.data = np.unique(node.data)
        print("Values:", node.data)
        print("Terminal Node", "\n")
        return counter
    
    if(node.branch_name != ''):
        print("Branch: ", node.branch_name)

    if(node.title != ''):
        print(node.title)

    print("Values:", node.data,"\n")
    counter+=1
    for i in node.children:
        counter = print_tree(i, counter)
        counter+=1
    return counter


def main():
    root = recursive_tree_creation(data, Decision, titles)
    node_counter = print_tree(root)
    print('Amount of nodes:', node_counter)
    
if __name__ == "__main__":
    main()
