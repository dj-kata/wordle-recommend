#!/usr/bin/python3
from collections import defaultdict
from absl import app, flags
FLAGS = flags.FLAGS
import re

def gendb():
    ret = []
    with open('wordles.txt') as f:
        line = f.readline()
        while line:
            if not line:
                break
            ret.append(line.strip())
            line = f.readline()
    return ret

def recommend(words, cand, cur, pre, abs):
    c_exist = set(pre+re.sub('\.', '', cur))
    stat = defaultdict(int)
    
    # 足りない文字の一覧(stat)を取得
    for w in cand:
        for i,c in enumerate(w):
            if c not in c_exist:
                stat[c] += 1

    # statを多くカバーする単語を抽出
    ret = {}
    pre_without_cur = set(pre) - set(cur)
    for w in words:
        eval = 0
        for i,c in enumerate(w):
            if c in stat:
                eval += 2
            if c in pre_without_cur:
                eval += 1
            if c in abs:
                eval -= 100
        if eval > 0:
            ret[w] = eval
    ret_sorted = sorted(ret.items(), key=lambda x:x[1], reverse=True)
    return ret_sorted

# current, presentを全て満たす単語リストを取得
def search_cand(words, cur, pre, abs):
    ret = {}
    for w in words:
        eval = 0
        cnt_pre = 0 # presentリストの文字が出た回数を数えておく。全て出ていないやつを弾く目的。
        for i, c in enumerate(w): # correct
            if c == cur[i]:
                eval += 10
            if (c!=cur[i]) and (cur[i] != '.'):
                eval -= 100
            if c in abs:
                eval -= 100
        for c in pre:
            if c in w:
                eval += 1
                cnt_pre += 1
        if eval > 0 and cnt_pre == len(pre):
            ret[w] = eval
    ret_sorted = sorted(ret.items(), key=lambda x:x[1], reverse=True)
    return ret_sorted, ret

def disp(cor, pre, abs):
    print(f'correct:{cor}, present:{pre}, absent:{abs}')

def main(argv):
    cor = FLAGS.correct.lower()
    pre = FLAGS.present.lower()
    abs  = FLAGS.absent.lower()
    words = gendb()

    while True:
        print('cmd? (q:quit, d:disp, c:correct, p:present, a:absent, u:update all, s:search) :')
        cmd = input()
        if cmd == 'q':
            break
        elif cmd == 'd':
            disp(cor, pre, abs)
        elif cmd == 'c':
            print('new correct? :')
            tmp = input().lower()
            if len(tmp) == 5:
                cor = tmp
                disp(cor, pre, abs)
            else:
                print('invalid format!')
        elif cmd == 'p':
            print('new present? :')
            pre = input().lower()
            disp(cor, pre, abs)
        elif cmd == 'a':
            print('new absent? :')
            abs = input().lower()
            disp(cor, pre, abs)
        elif cmd == 'u':
            print('new correct? :')
            tmp = input().lower()
            if len(tmp) == 5:
                cor = tmp
            else:
                print('invalid format!')
            print('new present? :')
            pre = input().lower()
            print('new absent? :')
            abs = input().lower()
            disp(cor, pre, abs)
            
        elif cmd == 's':
            tmp, org = search_cand(words, cor, pre, abs)
            rec = recommend(words, org.keys(), cor, pre, abs)
            print(f'candidates({len(tmp)}) = {tmp}')
            print(f'recommend({len(rec)}) = {rec[:10]}')

if __name__ == '__main__':
    flags.DEFINE_string('correct', '.....', 'correct list (a-z or "."  ex: ..GA. )', short_name='c')
    flags.DEFINE_string('present', '', 'present list (a-z ex:SU)', short_name='p')
    flags.DEFINE_string('absent', '', 'absent list (a-z ex:SU)', short_name='a')
    app.run(main)