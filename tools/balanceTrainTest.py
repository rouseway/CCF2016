#-*- coding:utf-8 -*-

import sys,random

zero_lst = []
fin = open('./format-train.csv')
sline = fin.readline()
print sline.strip()
while True:
    sline = fin.readline()
    if not sline:
        break
    elem_lst = sline.split(',')
    if elem_lst[1] == '1':
        print sline.strip()
    else:
        zero_lst.append(sline.strip())
fin.close()

if sys.argv[1] == '1':
    zero_lst = random.sample(zero_lst, 80025)
elif sys.argv[1] == '2':
    zero_lst = random.sample(zero_lst, 160050)
elif sys.argv[1] == '3':
    zero_lst = random.sample(zero_lst, 240075)
elif sys.argv[1] == '4':
    zero_lst = random.sample(zero_lst, 320100)
elif sys.argv[1] == '5':
    zero_lst = random.sample(zero_lst, 400125)
elif sys.argv[1] == '6':
    zero_lst = random.sample(zero_lst, 480150)
elif sys.argv[1] == '7':
    zero_lst = random.sample(zero_lst, 560175)

for sline in zero_lst:
    print sline
