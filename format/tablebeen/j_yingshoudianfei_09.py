#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-22

import utils


# 09_ARC_A_RCVBL_FLOW.TSV 应收电费信息表 （共计13个字段）
class YingShouDianFei():
    def __init__(self, elem_lst):
        self.cons_no = elem_lst[0]              #用户编号

        self.ymrcvbl_ym = None                  #应收年月
        self.ymrcvbl_ym = utils.convert_to_date_YM('09_ARC_A_RCVBL_FLOW.TSV', elem_lst[1])

        self.org_no = elem_lst[2]               #供电单位编号
        self.pay_code = elem_lst[3]             #缴费方式

        self.t_pq = 0.0                         #总电量
        self.t_pq = utils.convert_to_float(elem_lst[4])

        self.rcvbl_amt = 0.0                    #应收金额
        self.rcvbl_amt = utils.convert_to_float(elem_lst[5])

        self.rcved_amt = 0.0                    #实收金额
        self.rcved_amt = utils.convert_to_float(elem_lst[6])

        self.status_code = elem_lst[7]          #费用状态

        self.rcvbl_penalty = 0.0                #应收违约金
        self.rcvbl_penalty = utils.convert_to_float(elem_lst[8])

        self.rcved_penalty = 0.0                #实收违约金
        self.rcved_penalty = utils.convert_to_float(elem_lst[9])

        self.risk_level_code = elem_lst[10]     #风险等级

        self.owe_amt = 0.0                      #电费金额
        self.owe_amt = utils.convert_to_float(elem_lst[11])

        self.cons_sort_code = elem_lst[12]      #用户分类
        self.elec_type_code = elem_lst[13]      #用电类别
        self.ctl_mode = elem_lst[14]            #费控方式


    def get_rcvbl_month(self):
        if self.ymrcvbl_ym == None:
            return -1
        else:
            return int(self.ymrcvbl_ym.month)


'''
供电单位编号 754
用电类别 17
用户分类 4
缴费方式 9
费用状态 1
'''