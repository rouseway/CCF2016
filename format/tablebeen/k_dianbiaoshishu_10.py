#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-22

import utils

# 10_C_METER_READ.TSV 电表示数信息表 （共计2个字段）
class DianBiaoShiShu():
    def __init__(self, elem_lst):
        self.meter_id = elem_lst[0]     #电能表标识
        self.org_no = elem_lst[1]       #供电单位代码
