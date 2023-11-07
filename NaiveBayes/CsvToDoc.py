import os
import csv
train_file = os.path.join(os.path.dirname(__file__),'../Recommender/train.csv')
test_file = os.path.join(os.path.dirname(__file__),'../Recommender/test.csv')
NAMELIST = {0: "", 1: "danceability", 2: "energy", 3: "loudness", 4: "speechiness", 5: "acousticness", 6: "instrumentalness", 7: "liveness", 8: "valence" , 9: "tempo"}
TEMPOLIST = {'l': "Largo-", 'o': "Larghetto-", 'a': "Adagio-", 'e':"Adante-", 'm': "Moderato-", 'r': "Allegro-", 'p': "Presto-", 'i': "Prestissimo-"}
LEVELLIST = {"l": "Low-", "m": "Medium-", "h":"High-"}

def docPush(line):
    pDoc = ""
    for i in range(1, len(line)):
        if i == 9:
            pDoc += (TEMPOLIST[line[i]] + NAMELIST[i] + "\n")
        else:
            pDoc += (LEVELLIST[line[i]]+NAMELIST[i] + " ")
    return pDoc

# This open code was referenced from https://stackoverflow.com/questions/46614526/how-to-import-a-csv-file-into-a-data-array

with open(train_file, newline='') as csvfile:
    data = list(csv.reader(csvfile))
print(data)

with open(test_file, newline='') as csvfile:
    data = list(csv.reader(csvfile))
print(data)

likeFileTrain = open(os.path.relpath('../Data/bayesTrainLike.txt'), "w")
dislikeFileTrain = open(os.path.relpath('../Data/bayesTrainDislike.txt'), "w")

likeFileTest = open(os.path.relpath('../Data/bayesTestLike.txt'), "w")
dislikeFileTest = open(os.path.relpath('../Data/bayesTestDislike.txt'), "w")

#Seperate into like and dislie

for line in data:
    if line[0] == 'l':
        likeFileTrain.writelines(docPush(line))
    else:
        dislikeFileTrain.writelines(docPush(line))

for line in data:
    if line[0] == 'l':
        likeFileTest.writelines(docPush(line))
    else:
        dislikeFileTest.writelines(docPush(line))
        

likeFileTrain.close()
dislikeFileTrain.close()
likeFileTest.close()
dislikeFileTest.close()


