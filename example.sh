#!/bin/sh

cp corpus/category_text/example/* corpus/category_text/
cp corpus/train_text/example/* corpus/train_text/
cp corpus/test_data/example/* corpus/test_data/

echo "====== Training a document classifier ======"
echo "Train and save a Naive Bayes classifier."
echo "> python classification.py"
python classification.py

echo ""
echo "Assign a label to a text file using the classifier"
echo "> python classification.py labelling 'hello world!'"
python classification.py labelling 'hello world!'

echo ""
echo "====== Detecting historical causations ======"
echo "In this example, we use following assumptions."
echo "h1 and h2: historical causations."
echo "p1: a present issue."
echo "c1, c2, and c3: categories."
echo ""
echo "Above the causations and issue are assigned categories as follows:"
echo "------ table of  ------"
echo "Name | c1 | c2 | c3"
echo "h1   | 0  | 0  | 1"
echo "h2   | 1  | 1  | 1"
echo "p1   | 1  | 1  | 0"
echo 
echo "From this data set, let's get top k ranked historical causations."
echo "> java Matching '0, 0, 1 ... 1, 1, 1 ... 1, 1, 0' 2 (k = 2)"
java Matching '0, 0, 1 ... 1, 1, 1 ... 1, 1, 0' 2

rm corpus/category_text/c.txt
rm corpus/category_text/d.txt
rm corpus/train_text/c1.txt
rm corpus/train_text/c2.txt
rm corpus/train_text/d1.txt
rm corpus/train_text/d2.txt
rm corpus/test_data/test1.txt
