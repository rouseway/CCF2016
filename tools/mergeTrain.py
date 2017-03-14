#-*- coding:utf-8 -*-
import sys

blacklist_dict = {}
fin = open('./blacklist_29in160k.csv')
while True:
    sline = fin.readline()
    if not sline:
        break
    blacklist_dict[sline.strip()] = 1
fin.close()

fin = open('./format-test.csv')
sline = fin.readline()
print sline.strip()
while True:
    sline = fin.readline()
    if not sline:
        break
    elem_lst = sline.split(',')
    if elem_lst[0] not in blacklist_dict:
        print sline.strip()
    else:
        sys.stderr.write("%s" % sline)
fin.close()

    
