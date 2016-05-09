#!/bin/sh

mkdir corpus
mkdir corpus/test_data
mkdir corpus/category_text
mkdir corpus/train_text
mkdir corpus/unlabelled_data

mkdir corpus/test_data/example
mkdir corpus/category_text/example
mkdir corpus/train_text/example

cp ./example_files/c.txt corpus/category_text/example
cp ./example_files/d.txt corpus/category_text/example

cp ./example_files/c1.txt corpus/train_text/example
cp ./example_files/c2.txt corpus/train_text/example
cp ./example_files/d1.txt corpus/train_text/example
cp ./example_files/d2.txt corpus/train_text/example

cp ./example_files/test1.txt corpus/test_data/example

echo "Please set text files whose name represent categories in ./corpus/category_text."
echo "Please set labeled text files in ./corpus/train_text."
echo "Please set test text files in ./corpus/test_text."

