from collections import Counter
import os
#An artifact from the fact that my requests library is scuffed on my desktop
import pip._vendor.requests

# This time I switched to the _ notation over camel case, I heard that was a python best practice

# Simple Probability Calculation
def probability(doc, total_doc):
    prob = len(doc.splitlines())/ total_doc
    return prob

# Inital Calucaltions returns a tuple containing all probabilities
def cat_prob(neg_doc, pos_doc):
    total_words = len(neg_doc.splitlines()) + len(pos_doc.splitlines())
    neg_prob = probability(neg_doc, total_words)
    pos_doc = probability(pos_doc, total_words)
    return (neg_prob, pos_doc)

# Counts each word and adds to the count
def inc_count(total_count, spec_count, list):
    total_word_count = 0
    for word in list:
        spec_count[word] +=1
        total_count[word] +=1
        total_word_count +=1
    return total_word_count

# Returns a massive 7 element tuple in order of declaration
def full_count(neg_doc, pos_doc):
    total_counter = Counter()
    neg_counter = Counter()
    pos_counter = Counter()
    num_neg = 0
    num_pos = 0

    # Convert each doc to a list of words
    neg_list = neg_doc.split()
    pos_list = pos_doc.split()

    num_neg = inc_count(total_counter, neg_counter, neg_list)
    num_pos = inc_count(total_counter, pos_counter, pos_list)

    return(total_counter, neg_counter, pos_counter, num_neg, num_pos)

def prob_calc(word_list, word_counter, gen_prob, word_total, size, alpha):
  prob_list_of_words = gen_prob
  for word in word_list:
    if word in word_counter:
      numerator =  word_counter[word]+alpha
    else:
      numerator = alpha
    
    denominator = word_total + alpha*size
    word_prob  = numerator / denominator

    prob_list_of_words = prob_list_of_words* word_prob


  return prob_list_of_words

def predict(test_doc, cata_prob, gen_prob, real_cat, preds, alpha):
    for line in test_doc.splitlines():        
        wordsInList = line.split()
        #Matched
        neg_prob = prob_calc(wordsInList, gen_prob[1], cata_prob[0], gen_prob[3], len(gen_prob[0]), alpha)
        #It matches now??!
        pos_prob = prob_calc(wordsInList, gen_prob[2], cata_prob[1], gen_prob[4], len(gen_prob[0]), alpha)

        if neg_prob > pos_prob:
            pred_cat = "-ve"
        else:
            pred_cat = "+ve"

        preds.append((line, real_cat, pred_cat))
        print("predicted sentiment: ", pred_cat)

def accuracy(predict_list):
    correct_pred = 0
    total_test_case = 0
    for pred in predict_list:
        (cat, real_cat, pred_cat) = pred
        if real_cat == pred_cat:
            correct_pred+=1
        total_test_case +=1

    accuracy = correct_pred/ total_test_case
    print("Accuracy : ", accuracy *100, " %")

negative_train = open(os.path.relpath("../Data/bayesTrainDislike.txt"), "r").read()
positive_train = open(os.path.relpath("../Data/bayesTrainLike.txt"), "r").read()

negative_test = open(os.path.relpath("../Data/bayesTestDislike.txt"), "r").read()
positive_test = open(os.path.relpath("../Data/bayesTestLike.txt"), "r").read()


alpha = 2.0
total_words = 0
predictions = []
cata_prob = cat_prob(negative_train, positive_train)

# (total_counter, neu_counter, neg_counter, pos_counter, num_neu, num_neg, num_pos)
gen_prob = full_count(negative_train, positive_train)

predict(negative_test, cata_prob, gen_prob, "-ve", predictions, alpha)
predict(positive_test, cata_prob, gen_prob, "+ve", predictions, alpha)
accuracy(predictions)





