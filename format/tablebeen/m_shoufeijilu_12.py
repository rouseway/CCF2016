#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-22

import utils


# 12_A_PAY_FLOW.TSV  收费记录表 （共计5个字段）
class ShouFeiJiLu():
    def __init__(self, elem_lst):
        self.cons_no = elem_lst[0]          #用户编号
        self.org_no = elem_lst[1]           #供电单位代码

        self.charge_ym = None               #收费年月
        self.charge_ym = utils.convert_to_date_YM('12_A_PAY_FLOW.TSV', elem_lst[2])

        self.charge_date = None             #收费日期
        self.charge_date = utils.convert_to_datetime('12_A_PAY_FLOW.TSV', elem_lst[3])

        self.pay_mode = utils.convert_to_int(elem_lst[4])    #缴费方式


    def get_charge_month(self):
        if self.charge_ym == None:
            return -1
        else:
            return int(self.charge_ym.month)

    def check_charge_at_month_end(self):
        if self.charge_date != None and self.charge_date.day > 21:
            return True
        else:
            return False


'''
供电单位编号 414
缴费方式 11
'''