#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-22


# 05_C_CONS_PRC.TSV 用户电价信息表 （共计3个字段）
class YongHuDianJia():
    def __init__(self, elem_lst):
        self.cons_id = elem_lst[0]      #用户标识
        self.org_no = elem_lst[2]       #供电单位代码
        self.tf_flag = elem_lst[1]      #是否执行峰谷标识

'''
是否执行峰谷标识 2 (true/false)
供电单位代码 260
'''