Source codes for History Time Machine
---


[History Time Machine](http://www.historymining.org/timemachine/) is a learning environment designed for studying historical causations.
Although the current system only supports Japanese, it will be available in English.  


This system uses the following two programs:

1. Document classification (classification.py)  
  We implemented a Naive Bayes classifier.

2. Detecting historical causations similar to a present one (Matching.java)  
  We implemented a matrix multiplication for this. 
  First, we make a feature matrix from what categories all causations are assigned.  
  Then, the matrix is multiplicated by its transported matrix.


Libraries Used
---

- Python
  1. [MeCab](http://mecab.googlecode.com/svn/trunk/mecab/doc/index.html?sess=3f6a4f9896295ef2480fa2482de521f6)
  2. [mojimoji](https://pypi.python.org/pypi/mojimoji/0.0.5)


Usage
---

- Build a Naive Bayes classifier  
  `python classification`

- Use the classifier  
  `python classification.py labelling '(sentences)'`

- Detecting historical causations  
  `java Matching '(category information of all issues)'　k`  
  Note that it is assumed that 0/1 represent whether a category is assigned to any issue or not.  
  For each causation, a feature vector whose size is the same as the number of using categories (each element is represented by 0 or 1) is created.  
  In one feature vector, each 0/1 is divided by ", ".  
  In addition, the feature vectors are divided by " ... ".  
  The second argument (k) means how many historical causations are gotten.  
  For example, let us consider a case where we use two historical data whose feature vectores are "0, 0, 1" and "1, 1, 1" and one present data whose feature vector is "1, 1, 0". Then, the following command outputs a result.  
  `java Matching '0, 0, 1 ... 1, 1, 1 ... 1, 1, 0' 2`


Reference
---

 Y. Sumikawa and R. Ikejiri, 
 "Mining Historical Social Issues" , 
 Intelligent Decision Technologies, Smart Innovation, Systems and Technologies, 
 Vol. 39, Springer International Publishing, 2015, pp. 587--597.   
 [paper](http://link.springer.com/chapter/10.1007%2F978-3-319-19857-6_50)



License
---

GPL and BSD Licenses for History Time Machine
Copyright (c) 2016-present, Yasunobu Sumikawa, All rights reserved.

Redistribution and use in source form, with or without modification,
are permitted provided that the following conditions are met:
 * Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
 * No the name Yasunobu Sumikawa may be used to endorse or promote products derived
   from this software without specific prior written permission.
   
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Developers
---
 - The main developer
  - [Yasunobu Sumikawa](http://www.cs.is.noda.tus.ac.jp/~yas/en/index_en.html)

 - Contributer
  - [Ryohei Ikejiri](http://www.ikejiri-lab.net/)
