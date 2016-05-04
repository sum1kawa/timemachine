歴史タイムマシーンのコアプログラム

---

[歴史タイムマシーン](http://www.historymining.org/timemachine/)で使用しているプログラムのソースコードです。  
公開しているソースコードは次の2つです。

1. 入力文章へのカテゴリの付与 (classification.py)  
  単純ベイズ分類器を実現し、文章中に出現する単語から、最も適切だと思われるカテゴリを決定します。

2. 現代の問題に類似する過去の問題の抽出 (Matching.java)  
  現代の問題と比較して、同じカテゴリが付与されている数が多い順に過去の問題を出力します。  
  このプログラムは、各問題のカテゴリから特徴行列を作成し、その転置行列との積を計算することで結果を得ています。


使い方

---

- 単純ベイズ分類器の作成  
  python classification

- 単純ベイズ分類器の使用  
  python classification.py labelling '（カテゴリを付与したい文章）'

- 過去の問題の抽出  
  java Matching '（すべての問題のカテゴリ）'  
  なお、1つの問題にカテゴリが付与されているかどうかを0（付与されていない） or 1（付与されている）で表すこと。  
  1つの問題に対して、0/1を", "で区切り、問題ごとのカテゴリは、" ... "で区切ること。  
  例： java Matching '0, 0, 1 ... 1, 1, 1 ... 1, 1, 0' 


参考文献

---

 Y. Sumikawa and R. Ikejiri, 
 "Mining Historical Social Issues" , 
 Intelligent Decision Technologies, Smart Innovation, Systems and Technologies, 
 Vol. 39, Springer International Publishing, 2015, pp. 587--597. 


ライセンス

---

GPL and BSD Licenses for History Timemachine
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

Contributer:
  - Ryohei Ikejiri
