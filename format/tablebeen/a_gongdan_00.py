#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-22

import re
import utils

# 00_ARC_S_95598_WKST_TRAIN/TEST.TSV 工单信息表 （共计13个字段）
class GongDan():
    def __init__(self, elem_lst):
        self.app_no = elem_lst[0]               #工单受理唯一标识号
        self._id = elem_lst[1]                  #工单唯一标识
        self.busi_type_code = elem_lst[2]       #业务类型编码 "010 003 001 007 015 005 018 009 008 006"
        self.urban_rural_flag = elem_lst[3]     #城乡类别标识
        self.org_no = elem_lst[4]               #供电单位编码

        self.handle_time = None                 #工单受理时间
        self.handle_time = utils.convert_to_datetime("00_ARC_S_95598_WKST_*.TSV",elem_lst[5])

        self.accept_content = None              #工单受理内容
        self.accept_content = utils.gbk2utf(elem_lst[6])

        self.handle_opinion = elem_lst[7]       #受理意见
        self.calling_no = elem_lst[8]           #主叫号码

        self.elec_type = elem_lst[9]            #用电类别
        if len(elem_lst[9]) == 0:
            self.elec_type = "null"

        self.cust_no = elem_lst[10]             #客户编号 （！！！！结果提交字段）
        self.prov_org_no = elem_lst[11]         #所属省（市）公司供电单位编码
        self.city_org_no = elem_lst[12]         #所属市（区）公司供电单位编码

        self.poweroff_ids = []                  #从content中抽取poweroffid


    def extract_poweroff(self, app_poweroff):
        id_pattern = re.compile('15[0-9]{10}')
        match_lst = id_pattern.findall(self.accept_content)
        for ret in match_lst:
            self.poweroff_ids.append(ret)
        app_poweroff[self.app_no] = self.poweroff_ids



'''
用电类别 20
所属省（市）公司供电单位编码 1
供电单位编码 184
业务类型编码 10
所属市（区）公司供电单位编码 12
城乡类别标识 3
'''


