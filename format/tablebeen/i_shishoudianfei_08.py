#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-22

import utils

# 08_A_RCVED_FLOW.TSV 实收电费信息表 （共计9个字段）
class ShiShouDianFei():
    def __init__(self, elem_lst):
        self.cons_no = elem_lst[1]          #用户编号
        self.org_no = elem_lst[0]           #供电单位编号


        self.rcved_ym = None                #实收年月
        self.rcved_ym = utils.convert_to_date_YM('08_A_RCVED_FLOW.TSV', elem_lst[2])

        self.rcved_date = None              #实收日期
        self.rcved_date = utils.convert_to_date_YMD('08_A_RCVED_FLOW.TSV', elem_lst[3])

        self.this_rcved_amt = elem_lst[4]   #本次实收电费
        self.this_penalty = elem_lst[5]     #本次实收违约金
        self.owe_amt = elem_lst[6]          #金额

        self.rcvbl_ym = None                #应收年月
        self.rcvbl_ym = utils.convert_to_date_YM('08_A_RCVED_FLOW.TSV', elem_lst[7])


        self.rcvbl_penalty = elem_lst[8]    #应收违约金


    def is_delay(self):
        if self.rcvbl_ym == None or self.rcved_ym == None:
            return False
        elif self.rcved_ym > self.rcvbl_ym:
            return True

    def get_charge_month(self):
        if self.rcved_ym == None:
            return -1
        else:
            return int(self.rcved_ym.month)