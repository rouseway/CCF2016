#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-22


# 11_C_METER.TSV 运行电能信息表 （共计6个字段） （处理5个）
class YunXingDianNeng():
    def __init__(self, elem_lst):
        self.cons_id = elem_lst[5]      #用户标识
        self.meter_id = elem_lst[0]     #电能表标识
        self.org_no = elem_lst[1]       #供电单位编号
        self.sort_code = elem_lst[3]    #电能表类别
        self.type_code = elem_lst[4]    #电能表类型


'''
供电单位编号 984
电能表类型 55
电能表类别 6
'''