#!/usr/bin/python3
from collections import defaultdict
import pandas as pd
import itertools

df_prob = pd.read_csv('problem.txt')
df_cand = pd.read_csv('cand.txt')
df_prob.columns=['name']
df_cand.columns=['name']

c_stat = defaultdict(int)
pos_stat = [defaultdict(int) for i in range(5)]

for w in df_prob['name']:
    for i,c in enumerate(w):
        c_stat[c] += 1
        pos_stat[i][c] += 1

c_sorted = sorted(c_stat.items(), key=lambda x:x[1], reverse=True)

print(f'stats for chars:         {c_sorted[:10]}')
for i in range(5):
    pos_sorted = sorted(pos_stat[i].items(), key=lambda x:x[1], reverse=True)
    print(f'stats for chars at pos{i+1}: {pos_sorted[:10]}')

#### 問題の分析
prob_size = df_prob.shape[0]

from tqdm import tqdm
# 1手目での評価値
window_1st = 1 # 最初の何手まで見るか
eval1 = {}
for tmp in tqdm(itertools.combinations(df_cand['name'],window_1st)):
    query = ~df_prob['name'].str.contains(tmp[0])
    for c in ''.join(tmp):
        query &= ~df_prob['name'].str.contains(c)
    score = prob_size - df_prob[query].shape[0]
    eval1['_'.join(tmp)] = score
eval1_sorted = sorted(eval1.items(), key=lambda x:x[1], reverse=True)
print(eval1_sorted[:20])
