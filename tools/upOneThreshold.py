#!/usr/bin/python
#coding=utf8

import sys

user_id = []
fin = open(sys.argv[1])
fin.readline()
while True:
    sline = fin.readline()
    if not sline:
        break
    elem_lst = sline.split(',')
    user_id.append(elem_lst[0])
fin.close()

fin = open(sys.argv[2])
threshold_1 = float(sys.argv[3])
idx = 0
one_cnt = 0
while True:
    sline = fin.readline()
    if not sline:
        break
    label,prob = sline.strip().split('\t')
    if int(label) == 1 and float(prob) > threshold_1:
        print user_id[idx]
        one_cnt += 1
    idx += 1
fin.close()
sys.stderr.write("%d\n" % one_cnt)




