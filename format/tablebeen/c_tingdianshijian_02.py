#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-22

import utils

# 02_S_REGION_OUTRAGE.TSV 停电事件信息表 （共计51个字段） 从前32个提取11个
class TingDianShiJian():
    def __init__(self, elem_lst):
        self.poweroff_id = elem_lst[0]          #停电信息唯一标识号
        self.app_no = elem_lst[1]               #申请编号

        self.start_time = None                  #停电开始时间
        self.start_time = utils.convert_to_datetime('02_S_REGION_OUTRAGE.TSV', elem_lst[3])

        self.stop_date = None                   #停电结束时间
        self.stop_date = utils.convert_to_datetime('02_S_REGION_OUTRAGE.TSV', elem_lst[4])

        self.org_no = elem_lst[5]               #停电所属供电单位
        self.type_code = elem_lst[6]            #停电类型
        self.poweroff_reason = elem_lst[8]      #停电原因

        self.power_time = None                  #现场送电时间
        self.power_time = utils.convert_to_datetime('02_S_REGION_OUTRAGE.TSV', elem_lst[31])

        self.poweroff_area = elem_lst[7]        #停电范围
        self.poweroff_scope = elem_lst[2]       #停电区域


    def get_outage_month(self):
        if self.start_time != None:
            return int(self.start_time.month)
        else:
            return -1

    def calculate_outage_miniute(self):
        if self.start_time == None or self.stop_date == None:
            return 0
        else:
            return round((self.stop_date-self.start_time).seconds/60.0, 2)

