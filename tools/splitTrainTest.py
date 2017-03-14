#-*- coding:utf-8 -*-

import sys,random

one_lst = []
zero_lst = []
fin = open(sys.argv[1])
title = fin.readline()
while True:
    sline = fin.readline()
    if not sline:
        break
    elem_lst = sline.split(',')
    if elem_lst[1] == '1':
        one_lst.append(sline)
    else:
        zero_lst.append(sline)
fin.close()

one_test_lst = random.sample(one_lst, int(len(one_lst)*0.2))
zero_test_lst = random.sample(zero_lst, int(len(zero_lst)*0.2))
fout = open(sys.argv[1]+'_test.csv', 'w')
fout.write('%s' % title)
for sline in one_test_lst:
    fout.write('%s' % sline)
for sline in zero_test_lst:
    fout.write('%s' % sline)
fout.close()

one_test_dict = dict(zip(one_test_lst, [0]*len(one_test_lst)))
zero_test_dict = dict(zip(zero_test_lst, [0]*len(zero_test_lst)))
fout = open(sys.argv[1]+'_train.csv', 'w')
fout.write('%s' % title)
for sline in one_lst:
    if sline not in one_test_dict:
        fout.write('%s' % sline)
for sline in zero_lst:
    if sline not in zero_test_dict:
        fout.write('%s' % sline)
fout.close()
