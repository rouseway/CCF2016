#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-22

import utils

# 07_C_RCA_CONS.TSV 费控用户信息表 （共计4个字段）
class FeiKongYongHu():
    def __init__(self, elem_lst):
        self.cons_no = elem_lst[0]          #用户编号

        self.cons_status = elem_lst[3]      #费控用户状态
        if len(elem_lst[3]) == 0:
            self.cons_status = "null"

        self.org_no = elem_lst[1]           #供电单位编码

        self.rca_flag = None                #费控标志
        self.rca_flag = utils.convert_to_int(elem_lst[2])



'''
供电单位编码 726
费控用户状态 3
费控标志 2
'''