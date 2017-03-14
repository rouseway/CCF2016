#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-22

import utils

trade_dict = {'9910':0, '9920':0, '6530':0, '6510':0, '1710':0, '1810':0 }
sort_dict = { '00':0, '01':0, '02':0, '03':0 }

# 04_C_CONS.TXT  用电客户信息表 （共计12个字段）
class YongDianKeHu():
    def __init__(self, elem_lst):
        self.cons_no = elem_lst[1]              #用户编号（关联主键）
        self.cons_id = elem_lst[0]              #用户标识

        self.cons_sort_code = elem_lst[10]      #用户分类
        if elem_lst[10] not in sort_dict:
            self.cons_sort_code = "others"

        self.contract_cap = None                #合同容量
        self.contract_cap = utils.convert_to_float(elem_lst[5])

        self.elec_addr = elem_lst[2]            #用电地址
        self.elec_type_code = elem_lst[4]       #用电类别

        self.hec_industry_code = elem_lst[7]    #高耗能行业类别
        if len(elem_lst[7]) == 0:
            self.hec_industry_code = "null"

        self.load_attr_code = elem_lst[6]       #负荷性质
        if len(elem_lst[6]) == 0:
            self.load_attr_code = "null"

        self.org_no = elem_lst[9]               #供电单位编号

        self.status_code = elem_lst[8]          #用户状态
        if len(elem_lst[8]) == 0:
            self.status_code = "null"

        self.trade_code = elem_lst[3]           #行业分类
        if elem_lst[3] not in trade_dict:
            self.trade_code = "others"

        self.urban_rurl_flag = elem_lst[11]     #城乡类别
        if len(elem_lst[11]) == 0:
            self.urban_rurl_flag = "null"

'''
城乡类别 3
用电类别 19
行业分类 398
用户状态 3
用户分类 5
供电单位编号 949
负荷性质 3
高能耗行业类别 7
'''