#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-12-14

for i in range(5):
    fin = open('./data/test-'+str(i+1)+'.csv')
    fout = open('./data/std-'+str(i+1)+'.txt', 'w')
    fin.readline()
    while True:
        sline = fin.readline()
        if not sline:
            break
        elem_lst = sline.split(',')
        fout.write("%s\n" % elem_lst[1])
    fin.close()
    fout.close()
