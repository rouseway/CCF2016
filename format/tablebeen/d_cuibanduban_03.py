#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-22

import utils

# 03_S_INFO_OVERSEE.TSV 催办督办信息表 （共计10个字段）
class CuiBanDuBan():
    def __init__(self, elem_lst):
        self.app_no = elem_lst[0]               #工单受理唯一标识号

        self.oversee_time = None                #催办督办时间
        self.oversee_time = utils.convert_to_datetime('03_S_INFO_OVERSEE.TSV', elem_lst[1])

        self.cust_no = elem_lst[2]              #客户编号
        self.cust_name = elem_lst[3]            #来电客户姓名

        self.oversee_reason = None              #催办督办原因
        self.oversee_reason = utils.gbk2utf(elem_lst[4])
        self.oversee_content = None             #催办督办内容
        self.oversee_content = utils.gbk2utf(elem_lst[5])


        self.oversee_app_no = elem_lst[6]       #被催办督办工单编号
        self.org_or_dept = elem_lst[7]          #被催办督办单位或部门
        self.app_busi_type_code = elem_lst[8]   #被催办工单类型
        self.org_no = elem_lst[9]               #供电单位



    def get_oversee_month(self):
        if self.oversee_time != None:
            return int(self.oversee_time.month)
        else:
            return -1




