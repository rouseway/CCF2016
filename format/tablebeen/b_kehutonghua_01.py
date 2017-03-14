#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-22

import utils

# 01_S_COMM_REC.TSV  客户通话信息表 （共计8个字段）
class KeHuTongHua():
    def __init__(self, elem_lst):
        self.app_no = elem_lst[0]               #工单受理唯一标识号
        self.handle_id = elem_lst[1]            #工单处理编号
        self.comm_no = elem_lst[2]              #通讯号码

        self.req_begin_date = None              #申请的提交时间
        self.req_begin_date = utils.convert_to_datetime('01_S_COMM_REC.TSV', elem_lst[3])

        self.req_finish_date = None             #服务请求结束时间
        self.req_finish_date = utils.convert_to_datetime('01_S_COMM_REC.TSV', elem_lst[4])

        self.org_no = elem_lst[5]               #供电单位
        self.busi_type_code = elem_lst[6]       #受理业务类型
        self.wkst_busi_type_code = elem_lst[7]  #工单业务类型


    def calculate_calling_miniute(self):
        if self.req_begin_date == None or self.req_finish_date == None:
            return 0
        else:
            return round((self.req_finish_date-self.req_begin_date).seconds/60.0, 2)


