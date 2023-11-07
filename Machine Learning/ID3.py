# A Python program to take training data about Spotify songs, turn its data into a decision tree to determine if a
# specific song will be liked or dislike, then uses test data to go through the decision tree and predict if that
# song will be liked or disliked by a suer based on its attributes. ID3 algorithm used to create tree.

# Author: Brent Hasseman
import pandas as pd
import math
import sys

train_file = '../Recommender/train.csv'
test_file = '../Recommender/test.csv'
first = True
attrsToCheck = []


class Node:
    # Class to hold values, create decision tree
    def __init__(self):
        self.root = None
        self.children = None
        self.next = None


class ID3Tree:
    # Class to create the tree, find entropy/info gain values
    def __init__(self, columnVals, likeOrDislike, columns):
        self.node = Node()
        self.attributeVals = columnVals  # Array of each row's values at all attributes (except class)
        self.classVals = likeOrDislike  # Each row's value for class
        self.attributeNames = columns  # Proper header names of each attribute
        self.classOptions = list(set(likeOrDislike))  # All options for class (e or p)
        self.classOptionsCounts = []  # Number of e, number of p

        for option in self.classOptions:
            self.classOptionsCounts.append(list(likeOrDislike).count(option))

        classValArr = []  # All 6000 rows
        for x in range(len(self.classVals)):
            classValArr.append(x)

        self.entropy = self.calculateEntropy(classValArr)  # Overall entropy of the system

    def calculateEntropy(self, classValues):
        # Idea for vals & classValCounts from
        # https://stackoverflow.com/questions/37839866/calculating-the-entropy-of-a-specific-attribute
        vals = []  # Each row's value for class
        for value in classValues:
            vals.append(self.classVals[value])

        classValCounts = []  # Number of e, number of p
        for option in self.classOptions:
            classValCounts.append(vals.count(option))

        entropy = 0
        for count in classValCounts:
            if count:
                entropy += -(count / len(classValues) * math.log(count / len(classValues), 2))  # Formula for entropy

        return entropy

    def tree(self):
        attributes = []  # Holds the 22 attributes for the tree
        for name in range(len(self.attributeNames)):
            attributes.append(name)

        rows = []  # Holds all 6000 rows
        for row in range(len(self.attributeVals)):
            rows.append(row)

        self.node = self.ID3Algorithm(self.node, rows, attributes)  # Creates root node of tree

    def ID3Algorithm(self, node, rows, attributes):  # Algorithm modeled off of pseudocode from Decision Tree slides
        if not node:  # Initializes node if need be
            node = Node()

        eOrP = []  # Each row's value for class
        for row in rows:
            eOrP.append(self.classVals[row])

        if len(set(eOrP)) == 1:  # If there is only 1 value for the class (homogeneous)
            node.root = self.classVals[rows[0]]
            return node

        # Gets the attribute that gives the most information as well as which index it is
        attributeWithMaxGain, attributeWithMaxGainID = self.findAttributeWithMaxGain(rows, attributes)

        rowAttributeValues = []  # Each row's value for the current max gain attribute
        for row in rows:
            rowAttributeValues.append(self.attributeVals[row][attributeWithMaxGainID])

        attributeOptions = list(set(rowAttributeValues))  # Gets each unique value for this attribute

        node.children = []  # Array for root node's children
        node.root = attributeWithMaxGain  # Makes the root node the attribute that gives the most info

        for option in attributeOptions:  # Loop to add each possible option for this attribute to the tree
            child = Node()
            child.root = option
            node.children.append(child)

            rowsWithOption = []  # Finds every row that has this value at this attribute
            for row in rows:
                if self.attributeVals[row][attributeWithMaxGainID] == option:
                    rowsWithOption.append(row)

            if attributeWithMaxGainID in attributes:  # Removes the attribute once it has been fully read
                attributeToRemove = attributes.index(attributeWithMaxGainID)
                # Removes the current attribute, looks for next attribute with max gain, reruns process
                attributes.pop(attributeToRemove)

            # Apply ID3 to each child of the root node
            child.next = self.ID3Algorithm(child.next, rowsWithOption, attributes)

        return node

    def calculateInfoGain(self, rows, attributeNumber):
        global first

        columnVals = []
        for row in rows:
            columnVals.append(self.attributeVals[row][attributeNumber])  # Get every row's value for this attribute

        attributeOptions = list(set(columnVals))  # Get the options for this attribute

        attributeCount = []
        for option in attributeOptions:
            attributeCount.append(columnVals.count(option))  # Get the counts of each option

        rowWithAttributeOption = []
        for option in attributeOptions:  # Get each row that has this option for this attribute
            temp = []
            for row, rowOption in enumerate(columnVals):
                if option == rowOption:
                    temp.append(rows[row])
            rowWithAttributeOption.append(temp)

        attributeEntropy = 0
        for attCounts, rowIDs in zip(attributeCount, rowWithAttributeOption):  # Calculate this attribute's entropy
            attributeEntropy += attCounts / len(rows) * self.calculateEntropy(rowIDs)

        infoGain = self.calculateEntropy(rows)
        infoGain -= attributeEntropy  # Get overall info gain from this attribute

        if first:  # Print each attribute's entropy on first iteration only
            print('Attribute {} entropy: {:.8f}'.format(self.attributeNames[attributeNumber], attributeEntropy))

        return infoGain

    def findAttributeWithMaxGain(self, rows, attributeNumber):
        global first

        attributeGains = []
        for attribute in attributeNumber:  # Get each attribute's gain
            attributeInfoGain = self.calculateInfoGain(rows, attribute)
            attributeGains.append(attributeInfoGain)
        # Error catch for when a tree couldn't be made
        if len(attributeNumber) == 0:
            print("Error occurred: A tree could not be created as another split could not be made. Please try to improve"
                  " training data.")
            sys.exit()
        maxInfoGainAttribute = attributeNumber[attributeGains.index(max(attributeGains))]  # Get attribute with max gain
        if first:  # Print each attribute's info gain on first iteration only
            print('___________________________________________________________________________')
            for i, gain in enumerate(attributeGains):
                print('Attribute {} info gain: {:.8f}'.format(self.attributeNames[i], gain))
            print('Attribute {} was chosen for the root node as it gives the most information gain.'.format(
                self.attributeNames[maxInfoGainAttribute]))
            print('___________________________________________________________________________')
            first = False
        attrsToCheck.append(self.attributeNames[maxInfoGainAttribute])
        return self.attributeNames[maxInfoGainAttribute], maxInfoGainAttribute

    def printTree(self):
        nodes = [self.node]  # Holds all nodes in the tree
        while len(nodes) > 0:
            node = nodes.pop(0)

            if node.children:
                for child in node.children:  # Runs through all children of current node, decides if the node is
                                             # poisonous, edible, or needs more information
                    if child.next.root == "l":
                        printstr = 'If {} is ({}) then the user will like it'.format(node.root, child.root)
                    elif child.next.root == "d":
                        printstr = 'If {} is ({}) then the user will dislike it'.format(node.root, child.root)
                    else:
                        printstr = 'If {} is ({}) then check its {}'.format(node.root, child.root, child.next.root)

                    print(printstr)

                    nodes.append(child.next)


# Function to make a prediction for the row on whether the user will like the song with the given attribute values
def predict(row, tree, checkedAttr, attrIndex):
    prediction = ""
    # type is ID3Tree on first call, every other time it's a node
    if type(tree) is ID3Tree:
        currentNode = tree.node
    else:
        currentNode = tree
    # Error catch, shouldn't ever not meet this condition
    if currentNode.children:
        # Iterate through each potential leaf
        for child in currentNode.children:
            # Matching attribute value
            if child.root == row[checkedAttr]:
                # The matching node will either be a leaf or need further checking
                if child.next.root == "l":
                    prediction = "like"
                elif child.next.root == "d":
                    prediction = "dislike"
                else:
                    attrIndex += 1
                    prediction = predict(row, child.next, attrsToCheck[attrIndex], attrIndex)

    return prediction


class Main:
    # Create the train and test dataframes
    trainDataframe = pd.read_csv(train_file, header=None)
    testDataframe = pd.read_csv(test_file, header=None)

    # Rename the columns of the dataframes
    trainDataframe.columns = ['like-or-dislike', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                              'instrumentalness', 'liveness', 'valence', 'tempo']

    testDataframe.columns = ['like-or-dislike', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                             'instrumentalness', 'liveness', 'valence', 'tempo']

    testColumns = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                   'instrumentalness', 'liveness', 'valence', 'tempo']

    # Print the tables
    print("Training table:")
    print(trainDataframe)
    print("___________________________________________________________________________")
    print("Testing table:")
    print(testDataframe)
    print("___________________________________________________________________________")

    # Print the attributes
    print("Attributes:")
    for attr in trainDataframe.columns:
        print(attr)
    print("___________________________________________________________________________")

    # Get the values of each attribute except the class, get the values for the class, and get the column names
    # Idea to split the dataframe in this fashion to convert to numpy array from https://stackoverflow.com/a/59261795
    trainNoClass = trainDataframe[testColumns]
    trainClassOnly = trainDataframe['like-or-dislike']
    values = trainNoClass.to_numpy()
    classValues = trainClassOnly.to_numpy()
    columnHeaders = list(trainNoClass.columns)

    # Create the tree of the training data, print its entropy/the decisions themselves
    tree = ID3Tree(columnVals=values, likeOrDislike=classValues, columns=columnHeaders)
    tree.tree()
    print("Training data tree:")
    print("Entropy: {:.8f}".format(tree.entropy))
    tree.printTree()
    print("___________________________________________________________________________")

    # Prints the attributes that will be checked by the tree
    print("Attributes to be checked: ", attrsToCheck)
    testNoClass = testDataframe[testColumns]
    predictedValues = []
    # Iterates over each row, makes a prediction for the row, prints the prediction
    for rowIndex in range(len(testNoClass.index)):
        row = testNoClass.iloc[rowIndex]
        prediction = predict(row, tree, attrsToCheck[0], 0)
        if prediction == "like":
            print("User is predicted to like song #{}.".format(rowIndex + 1))
            predictedValues.append("l")
        else:
            predictedValues.append("d")
            print("User is predicted to dislike song #{}.".format(rowIndex + 1))

    # Gets accuracy
    correct = 0
    totalRows = len(testDataframe.index)
    for rowIndex in range(len(testDataframe.index)):
        row = testDataframe.iloc[rowIndex]
        if row['like-or-dislike'] == predictedValues[rowIndex]:
            correct += 1
    accuracy = correct/totalRows
    accuracy *= 100
    print("Accuracy of predictions: {}%.".format(accuracy))
