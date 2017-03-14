#-*- coding:gbk -*-
#author: raosiwei
#date: 2016-12-14

import sys

vote_result = []
for i in range(201246):
    vote_result.append([0, 0])

for i in range(5):
    fin = open('./predict-'+str(i+1)+'.txt')
    idx = 0
    while True:
        sline = fin.readline()
        if not sline:
            break
        prob_0,prob_1 = sline.strip().split('\t')
        if float(prob_1) > 0.4:
            vote_result[idx][1] += 1
        else:
            vote_result[idx][0] += 1
        idx += 1
    fin.close()

for vote in vote_result:
    sys.stderr.write("%d\t%d\n" % (vote[0], vote[1]))
    if vote[0] > vote[1]:
        print '0'
    else:
        print '1'

