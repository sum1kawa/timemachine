#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*- 

import os
import re
import sys
import codecs
import math
import subprocess
from collections import defaultdict
from StopWord import StopWords
import MeCab
import mojimoji

# For text preproces.
mecab = None
sw = StopWords()

# For semi-supervised training.
num_assign_data = 5
topk = 5
lambda_val = 1.0

# Instance of Naive Bayes class.
nb = None 

# Set category information.
categories = []
for filename in os.listdir("corpus/category_text"):
    if not filename.endswith(".txt"):
        continue
    categories.append(filename[:filename.find(".txt")])

labelled_path = "corpus/train_text"
unlabelled_path = "corpus/unlabelled_data"


def get_bow(content):
    """
    We assume that the argument is written in Japanese.
    """

    # Convert full-width to half-width.
    content = mojimoji.zen_to_han(content.decode('utf-8')).encode('utf-8').lower() # 

    # Morphological analysis
    bow = mecab.parse(content.lower())
    rst = []
    for w in bow['nouns']+bow['verbs']: # Extract nouns and verbs.
        if not sw.is_stop_word(w):
            rst.append(w)
    return rst

class SemiSupervisedTraining:
    def __init__(self):
        self.labeled_data = []
        self.unlabeled_data = []

    def invoke(self):
        """
        We use EM algorithm for training a Naive Bayes classifier by semi-supervised learning.
        """
        # print "@ train of classification" # For debug.
        not_labeled_data_num = len(os.listdir(unlabelled_path))
        nb.train()
        num = 1

        while not_labeled_data_num > 0 and num > 0: # Check whether training classifier phase is invoked.
            # print "E-step" # For debug.
            self.multilabeling_all_category()

            nolabel_num = len(os.listdir(unlabelled_path))
            if (nolabel_num == not_labeled_data_num):
                break;
            else:
                not_labeled_data_num = nolabel_num

            num -= 1
            # print "M-step" # For debug.
            nb.train()


        nb.recordModel()


    def multilabeling_all_category(self):
        """
        Get top k documents, and then assign categories to them.
        """
        # print "@ multilabeling_all_category" # For debug.
        score_list_map = {}
        file_list_map = {}
        category_list_map = {}
        for cat in categories:
            score_list = []
            file_list = []
            category_list = []
            i = 0
            while i < num_assign_data:
                score_list.append(-1)
                file_list.append("-")
                category_list.append("-")
                i += 1
            score_list_map[cat] = score_list
            file_list_map[cat] = file_list
            category_list_map[cat] = category_list

        for filename in os.listdir(unlabelled_path):
            if not filename.endswith(".txt"):
                continue
            content = ""
            for line in codecs.open(unlabelled_path+"/"+filename, "r", "utf-8"):
                content += line.rstrip()
            bow = get_bow(content.encode("utf-8"))
            label, score = nb.predict(bow)

            score_list = score_list_map[label]
            file_list = file_list_map[label]
            category_list = category_list_map[label]

            # Record this file for labelling if the score is in the top k.
            i = 0
            while i < num_assign_data:
                if score_list[i] < score:
                    j = num_assign_data  - 1
                    while i < j:
                        score_list[j] = score_list[j-1]
                        category_list[j] = category_list[j-1]
                        file_list[j] = file_list[j-1]
                        j -= 1
                    score_list[j] = score
                    category_list[j] = label
                    file_list[j] = filename
                    break
                i += 1

        for cat in categories:
            score_list = score_list_map[cat]
            file_list = file_list_map[cat]
            category_list = category_list_map[cat]
            i = 0

            # Assign a label for top k documents.
            while i < topk:
                if score_list[i] == -1:
                    break
                filename = file_list[i]
                label = category_list[i]
                new_file_name = label + str(self.count_category_file_num(label)+1) + ".txt"

                cmd = "mv " + unlabelled_path + "/" + filename + " " + labelled_path + "/" + new_file_name
                subprocess.call(cmd.strip().split(" "))
                i += 1

    def count_category_file_num(self, category):
        """
        This method counts the number of labeled data.
        """
        num = 0
        for filename in os.listdir(labelled_path):
            if filename.find(category) >= 0:
                num += 1
        return num

class NaiveBayes:
    def __init__(self):
        self.file2wordlist = {}
        self.vocabularies = set()
        self.wordcount = {}
        self.denominator = {}
        self.catcount = {}
        self.ti = None

    def setData(self):
        for cat in categories:
            self.catcount[cat] = 0

        for filename in os.listdir(labelled_path):
            if not filename.endswith(".txt"):
                continue
            for cat in categories:
                if filename.find(cat)>-1:
                    self.catcount[cat] += 1
                    break
            content = ""
            for line in codecs.open(labelled_path+"/"+filename, "r", "utf-8"):
                content += line.rstrip()
            bow = get_bow(content.encode("utf-8"))
            self.file2wordlist[filename] = bow
            self.ti = TfIdf(self.file2wordlist)


    def train(self):
        # print "@ train naive bayes classifier"
        self.file2wordlist = {}
        self.vocabularies = set()
        self.wordcount = {}
        self.denominator = {}
        self.catcount = {}

        self.setData()
        for cat in categories:
            self.wordcount[cat] = defaultdict(int)

        for f in self.file2wordlist:
            category = ""
            for cat in categories:
                if f.find(cat)>-1:
                    category = cat
                    break

            wl = self.file2wordlist[f]
            for word in wl:
                self.wordcount[category][word] += 1
                self.vocabularies.add(word)

        for c in self.wordcount:
            for w in self.wordcount[c]:
                if self.wordcount[c][w] < 2:
                    self.wordcount[c][w] = 0
                else:
                    self.wordcount[category][word] = self.ti.tfidf(word,wl)

        for cat in categories:
            self.denominator[cat] = sum(self.wordcount[cat].values()) + len(self.vocabularies)

    def predict(self, wordlist):
        # print "@ predict"
        best_category = None
        max = -sys.maxint

        for cat in self.catcount:
            p = self.score(wordlist, cat)
            # print "category:", cat.rstrip(), ", score:", p
            if p > max:
                max = p
                best_category = cat
        return best_category, max

    def wordProb(self, word, cat):
        return float(self.wordcount[cat][word]+1) / float(self.denominator[cat])


    def score(self, wordlist, cat):
        total = sum(self.catcount.values())
        score = float(self.catcount[cat]) / total 

        for word in wordlist:
            score += self.wordProb(word, cat)
        return score


    def printModel(self):
        """
        For debug.
        """
        for cate in self.wordcount:
            for w in self.wordcount[cate]:
                if self.wordcount[cate][w] > 0:
                    tval = self.wordcount[cate][w]
                    print "P(" + cate + "|" + w.encode('utf8') + ") = " + str(tval)


    def recordModel(self):
        """
        We record our model of Naive Bayes classifier in xml file.
        """
        # self.printModel()
        import xml.dom.minidom

        doc = xml.dom.minidom.Document()

        root = doc.createElement('model')
        doc.appendChild(root)

        totalDocNum = doc.createElement('totaldocnum')
        root.appendChild(totalDocNum)
        totalDocNum.appendChild(doc.createTextNode(str(sum(self.catcount.values()))))

        for cate in self.wordcount:
            category = doc.createElement('category')
            category.appendChild(doc.createTextNode(cate))
            root.appendChild(category)

            docNum = doc.createElement('docnum')
            category.appendChild(docNum)
            docNum.appendChild(doc.createTextNode(str(self.catcount[cate])))

            deno = doc.createElement('denominator')
            category.appendChild(deno)
            deno.appendChild(doc.createTextNode(str(self.denominator[cate])))

            for w in self.wordcount[cate]:
                if self.wordcount[cate][w] < 0:
                    continue
                tval = self.wordcount[cate][w]
                elem = doc.createElement('elem')
                category.appendChild(elem)
                word = doc.createElement('word')
                elem.appendChild(word)
                word.appendChild(doc.createTextNode(w))
                val = doc.createElement('val')
                elem.appendChild(val)
                val.appendChild(doc.createTextNode(str(tval)))

        f1 = open('naive_bayes_model.xml','w')
        f1.write(doc.toprettyxml(' ','\n','utf-8'))
        f1.close()


    def readModel(self):
        """
        Read xml file recording a Naive Bayes classifier.
        """
        # print "@ readModel"
        contents = []
        for line in codecs.open('naive_bayes_model.xml', "r", "utf-8"):
            contents.append(line.replace(" ", ""))

        i = 0
        cat = ""
        word = ""

        while i < len(contents):
            if contents[i].startswith("<category>"):
                cat = contents[i+1].encode("utf-8").rstrip()
                self.wordcount[cat] = defaultdict(int)
                i += 1

            if contents[i].startswith("<docnum>"):
                self.catcount[cat] = int(contents[i+1])
                i += 1

            if contents[i].startswith("<denominator>"):
                self.denominator[cat] = float(contents[i+1])
                i += 1

            if contents[i].startswith("<word>"):
                word = contents[i+1].rstrip()
                i += 1

            if contents[i].startswith("<val>"):
                self.wordcount[cat][word] = float(contents[i+1])
                i += 1

            i += 1



class Mecab:
    def __init__(self):
        self.mc = MeCab.Tagger('-Ochasen')

    def parse(self, sentence):
        node = self.mc.parseToNode(sentence)
        words = []
        nouns = []
        verbs = []
        adjs = []
        while node:
            pos = node.feature.split(",")[0]
            word = node.surface.decode("utf-8")
            if pos == "名詞": # nouns.
                nouns.append(word)
            elif pos == "動詞": # verbs.
                verbs.append(word)
            elif pos == "形容詞": # adverbs.
                adjs.append(word)
            words.append(word)
            node = node.next
            parsed_words_dict = {
                "all": words[1:-1], # Eliminate empty character
                "nouns": nouns,
                "verbs": verbs,
                "adjs": adjs
                }
        return parsed_words_dict

class TfIdf:
    def __init__(self, docMap):
        self.docMap = docMap


    def freq(self, word, wordlist):
        return wordlist.count(word)

        
    def wordCount(self, wordlist):
        return len(wordlist)

           
    def containingDocNum(self, word):
        count = 0

        for doc in self.docMap:
            if self.freq(word,self.docMap[doc]):
                count += 1
        return count


    def tf(self, word, wordlist):
        return (self.freq(word,wordlist) / float(self.wordCount(wordlist)))


    def idf(self, word):
        return (math.log(len(self.docMap) / self.containingDocNum(word)))


    def tfidf(self, word, wordlist):
        return (self.tf(word,wordlist) * self.idf(word))

if __name__ == "__main__":
    argv = sys.argv
    mecab = Mecab()
    nb = NaiveBayes()
    c = SemiSupervisedTraining()
    if len(argv) > 1 and argv[1] == "labelling":
        if len(argv) > 2:
            bow = get_bow(argv[2])
            # Load classifier, and then assign labels to the inputed sentence.
            nb.readModel()
            label, score = nb.predict(bow)
            print label
        else:
            nb.readModel()
            for filename in os.listdir("corpus/test_data"):
                if not filename.endswith(".txt"):
                    continue
                print 
                print "file:", filename
                cont = ""
                for line in codecs.open("corpus/test_data/"+filename, "r", "utf-8"):
                    cont += line.rstrip()
                bow = get_bow(cont.encode("utf-8"))
                label, score = nb.predict(bow)
                print "label:", label
    else:
        c.invoke()
