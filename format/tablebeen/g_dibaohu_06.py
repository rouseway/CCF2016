#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-22


# 06_CONT_INFO.TSV  低保户用户信息表 （共计4个字段）
class DiBaoHu():
     def __init__(self, elem_lst):
        self.cons_no = elem_lst[0]          #用户编号
        self.appr_opinion = elem_lst[1]     #申请状态
        self.cont_type = elem_lst[2]        #低保户类型
        self.status = elem_lst[3]           #用户状态


'''
低保户类型 2
申请状态 9
用户状态 2
'''