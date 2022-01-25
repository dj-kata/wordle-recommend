# このスクリプトは?
wordleで次に入力すべき単語をリコメンドしてくれるスクリプトです。  
緑色、黄色、灰色のリストから次に入力すべき単語をリコメンドします。  
要はインチキってことです。  

あまりしっかり作り込んでいませんが、最低限のことはできると思います。

# how to use
まず最初に```wget https://slc.is/data/wordles.txt```しておいてください。

```
./recommend.py:
  -c,--correct: correct list (a-z or "."  ex: ..GA. )
    (default: '.....')
  -p,--present: present list (a-z ex:SU)
    (default: '')
  -a,--absent: absent list (a-z ex:SU)
    (default: '')
```
上から順に、文字も位置も正しいもの(緑色)、位置は違うが文字が含まれるもの(黄色)、文字が含まれないもの(灰色)。
緑色のやつのフォーマットは```S..G.```のように、分かっていないものは```.```としてください。

動作中は以下のようなCLIで動きます。  
uで最新の状態を入力して、sでリコメンド、という具合に使えばよいです。
```
cmd? (q:quit, d:disp, c:correct, p:present, a:absent, u:update all, s:search) :
```

# オープニング戦略
AEROS, UNLITが最強なのか？
