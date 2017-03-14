#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-23

import sys
import utils

'''
import gongdan,kehutonghua,tingdianshijian,cuibanduban
import yongdiankehu,yonghudianjia,dibaohu,feikongyonghu
import shishoudianfei,yingshoudianfei
import dianbiaoshishu,yunxingdianneng,shoufeijilu
'''

# 00 读取加载工单信息表数据 （每行唯一） #train:  | test: 423728
def load_GongDan_table(app_gongdan, filepath):
    print "[00] 读取工单信息表 ......"
    fin = open(filepath)
    fin.readline()
    cnt = 0
    while True:
        sline = fin.readline()
        if not sline:
            break
        cnt += 1
        if cnt % 100000 == 0:
            print cnt
        elem_lst = sline.strip('\n').split('\t')
        if len(elem_lst) != 13:
            sys.stderr.write("[WRONG FORMAT]: "+filepath+"  "+sline+"\n")
            continue

        app_no = elem_lst[0]
        #app_gongdan[app_no] = gongdan.GongDan(filepath, elem_lst)
        app_gongdan[app_no] = sline.strip('\n')
    fin.close()
    print "[00] 工单信息表读取完成"


# 01 读取加载客户通话信息表 （有重复） #1593088
def load_KeHuTongHua_table(id_kehutonghua):
    print "[01] 读取客户通话信息表 ......"
    fin = open("./data/01_s_comm_rec.tsv")
    fin.readline()
    cnt = 0
    while True:
        sline = fin.readline()
        if not sline:
            break
        cnt += 1
        if cnt % 100000 == 0:
            print cnt
        elem_lst = sline.strip('\n').split('\t')
        if len(elem_lst) != 8:
            sys.stderr.write("[WRONG FORMAT]: ./data/01_s_comm_rec.tsv  "+sline+"\n")
            continue

        _id = elem_lst[0]
        #id_kehutonghua[_id] = kehutonghua.KeHuTongHua(elem_lst)
        id_kehutonghua[_id] = sline.strip('\n') #1584351
    fin.close()
    print "[01] 客户通话信息表读取完成"


# 02 读取加载停电事件信息表 （每行唯一） #282206
def load_TingDianShiJian_table(poweroff_tingdianshijian):
    print "[02] 读取停电事件信息表 ......"
    fin = open("./data/02_s_region_outage.tsv")
    fin.readline()
    cnt = 0
    while True:
        sline = fin.readline()
        if not sline:
            break
        cnt += 1
        if cnt % 100000 == 0:
            print cnt
        elem_lst = sline.strip('\n').split('\t')
        if len(elem_lst) < 32:
            sys.stderr.write("[WRONG FORMAT]: ./data/02_s_region_outage.tsv  "+sline+"\n")
            continue

        poweroff_id = elem_lst[0]
        #poweroff_tingdianshijian[poweroff_id] = tingdianshijian.TingDianShiJian(elem_lst)
        poweroff_tingdianshijian[poweroff_id] = sline.strip('\n')
    fin.close()
    print "[02] 停电时间信息表读取完成"


# 03 读取催办督办信息表 （每行唯一） #15913
def load_CuiBanDuBan_table(app_cuibanduban):
    print "[03] 开始读取催办督办信息表 ......"
    fin = open("./data/03_s_info_oversee.tsv")
    fin.readline()
    cnt = 0
    while True:
        sline = fin.readline()
        if not sline:
            break
        cnt += 1
        if cnt % 100000 == 0:
            print cnt
        elem_lst = sline.strip('\n').split('\t')
        if len(elem_lst) != 10:
            sys.stderr.write("[WRONG FORMAT]: ./data/03_s_info_oversee.tsv  "+sline+"\n")
            continue

        app_no = elem_lst[0]
        #app_cuibanduban[app_no] = cuibanduban.CuiBanDuBan(elem_lst)
        app_cuibanduban[app_no] = sline.strip('\n')
    fin.close()
    print "[03] 催办督办信息表读取完成"


# 04 读取加载用电客户信息表 cons_no -> Set<cons_id>（每个用户信息重复3次，cons_no可唯一） #656282*3
def load_YongDianKeHu_table(cons_yongdiankehu):
    print "[04] 开始读取用电客户信息表 ......"
    fin = open("./data/04_c_cons.tsv")
    fin.readline()
    cnt = 0
    while True:
        sline = fin.readline()
        if not sline:
            break
        cnt += 1
        if cnt % 100000 == 0:
            print cnt
        elem_lst = sline.strip('\n').split('\t')
        if len(elem_lst) != 12:
            sys.stderr.write("[WRONG FORMAT]: ./data/04_c_cons.tsv  "+sline+"\n")
            continue

        cons_no = elem_lst[1]
        #cons_yongdiankehu[cons_no] = yongdiankehu.YongDianKeHu(elem_lst)
        utils.add_dict_dict(cons_yongdiankehu, cons_no, sline.strip('\n'))
    fin.close()
    print "[04] 用电客户信息表读取完成"


# 05 读取加载用户电价信息表   #8077443个id
def load_YongHuDianJia_table(id_yonghudianjia):
    print "[05] 开始读取用户电价信息表 ......"
    fin = open("./data/05_c_cons_prc.tsv")
    fin.readline()
    cnt = 0
    while True:
        sline = fin.readline()
        if not sline:
            break
        cnt += 1
        if cnt % 100000 == 0:
            print cnt
        elem_lst = sline.strip('\n').split('\t')
        if len(elem_lst) != 3:
            sys.stderr.write("[WRONG FORMAT]: ./data/05_c_cons_prc.tsv  "+sline+"\n")
            continue

        cons_id = elem_lst[0]
        #cons_yonghudianjia[cons_id] = yonghudianjia.YongHuDianJia(elem_lst)
        id_yonghudianjia[cons_id] = sline.strip('\n')
    fin.close()
    print "[05] 用户电价信息表读取完成"


# 06 读取加载低保户信息表 （有重复）
def load_DiBaoHu_table(cons_dibaohu):
    print "[06] 开始读取低保户信息表 ......"
    fin = open("./data/06_cont_info.tsv")
    fin.readline()
    cnt = 0
    while True:
        sline = fin.readline()
        if not sline:
            break
        cnt += 1
        if cnt % 100000 == 0:
            print cnt
        elem_lst = sline.strip('\n').split('\t')
        if len(elem_lst) != 4:
            sys.stderr.write("[WRONG FORMAT]: ./data/06_cont_info.tsv  "+sline+"\n")
            continue

        cons_no = elem_lst[0]
        #cons_dibaohu[cons_no] = dibaohu.DiBaoHu(elem_lst)
        cons_dibaohu[cons_no] = sline.strip('\n')
    fin.close()
    print "[6] 低保户信息表读取完成"


# 07 读取加载费控用户信息表 （每行唯一）
def load_FeiKongYongHu_table(cons_feikongyonghu):
    print "[7] 开始读取费控用户信息表 ......"
    fin = open("./data/07_c_rca_cons.tsv")
    fin.readline()
    cnt = 0
    while True:
        sline = fin.readline()
        if not sline:
            break
        cnt += 1
        if cnt % 100000 == 0:
            print cnt
        elem_lst = sline.strip('\n').split('\t')
        if len(elem_lst) != 4:
            sys.stderr.write("[WRONG FORMAT]: ./data/07_c_rca_cons.tsv  "+sline+"\n")
            continue

        cons_no = elem_lst[0]
        #cons_feikongyonghu[cons_no] = feikongyonghu.FeiKongYongHu(elem_lst)
        cons_feikongyonghu[cons_no] = sline.strip('\n')
    fin.close()
    print "[7] 费控用户信息表读取完成"


# 08 读取加载实收电费信息表  （用户->List<实收电费信息>）#282152个用户 3249742条收费信息
def load_ShiShouDianFei_table(cons_shishoudianfei):
    print "[08] 开始读取实收电费信息表 ......"
    fin = open("./data/08_a_rcved_flow.tsv")
    fin.readline()
    cnt = 0
    while True:
        sline = fin.readline()
        if not sline:
            break
        cnt += 1
        if cnt % 100000 == 0:
            print cnt
        elem_lst = sline.strip('\n').split('\t')
        if len(elem_lst) != 9:
            sys.stderr.write("[WRONG FORMAT]: ./data/08_a_rcved_flow.tsv  "+sline+"\n")
            continue

        cons_no = elem_lst[1]
        #cons_shishoudianfei[cons_no] = shishoudianfei.ShiShouDianFei(elem_lst)
        utils.add_dict_list(cons_shishoudianfei, cons_no, sline.strip('\n'))
    fin.close()
    print "[08] 实收电费信息表读取完成"


# 09 读取加载应收电费信息表  （用户->List<应收电费信息>）#555748个用户  #6466655条电费信息
def load_YingShouDianFei_table(cons_yingshoudianfei):
    print "[09] 开始读取应收电费信息表 ......"
    fin = open("./data/09_arc_a_rcvbl_flow.tsv")
    fin.readline()
    cnt = 0
    while True:
        sline = fin.readline()
        if not sline:
            break
        cnt += 1
        if cnt % 100000 == 0:
            print cnt
        elem_lst = sline.strip('\n').split('\t')
        if len(elem_lst) != 15:
            sys.stderr.write("[WRONG FORMAT]: ./data/09_arc_a_rcvbl_flow.tsv   "+sline+"\n")
            continue

        cons_no = elem_lst[0]
        #cons_yingshoudianfei[cons_no] = yingshoudianfei.YingShouDianFei(elem_lst)
        utils.add_dict_list(cons_yingshoudianfei, cons_no, sline.strip('\n'))
    fin.close()
    print "[09] 应收电费信息表读取完成"


# 10 读取加载电表示数信息表 （电表->List<示数信息>）  #25809334个电表  40821270条示数信息
def load_DianBiaoShiShu_table(meter_dianbiaoshishu):
    print "[10] 开始读取电表示数信息表 ......"
    fin = open("./data/10_c_meter_read.tsv")
    fin.readline()
    cnt = 0
    while True:
        sline = fin.readline()
        if not sline:
            break
        cnt += 1
        if cnt % 100000 == 0:
            print cnt
        elem_lst = sline.strip('\n').split('\t')
        if len(elem_lst) != 2:
            sys.stderr.write("[WRONG FORMAT]: ./data/10_c_meter_read.tsv   "+sline+"\n")
            continue

        meter_id = elem_lst[0]
        #meter_dianbiaoshishu[meter_id] = dianbiaoshishu.DianBiaoShiShu(elem_lst)
        utils.add_dict_list(meter_dianbiaoshishu, meter_id, sline.strip('\n'))
    fin.close()
    print "[10] 电表示数信息表读取完成"


# 11 读取加载运行电能信息表 （每行唯一） #25807825
def load_YunXingDianNeng_table(id_yunxingdianneng):
    print "[11] 开始读取运行电能信息表 ......"
    fin = open("./data/11_c_meter.tsv")
    cnt = 0
    fin.readline()
    while True:
        sline = fin.readline()
        if not sline:
            break
        cnt += 1
        if cnt % 100000 == 0:
            print cnt
        elem_lst = sline.strip('\n').split('\t')
        if len(elem_lst) != 6:
            sys.stderr.write("[WRONG FORMAT]: ./data/11_c_meter.tsv   "+sline+"\n")
            continue

        cons_id = elem_lst[5]
        #id_yunxingdianneng[cons_id] = yunxingdianneng.YunXingDianNeng(elem_lst)
        id_yunxingdianneng[cons_id] = sline
    fin.close()
    print "[11] 运行电能信息表读取完成"


# 12 读取加载收费记录表 （用户->List<缴费纪录>） #431833个用户  5483789条缴费纪录
def load_ShouFeiJiLu_table(cons_shoufeijilu):
    print "[12] 开始读取收费记录表 ......"
    fin = open("./data/12_a_pay_flow.tsv")
    cnt = 0
    fin.readline()
    while True:
        sline = fin.readline()
        if not sline:
            break
        cnt += 1
        if cnt % 100000 == 0:
            print cnt
        elem_lst = sline.strip('\n').split('\t')
        if len(elem_lst) != 5:
            sys.stderr.write("[WRONG FORMAT]: ./data/12_a_pay_flow.tsv   "+sline+"\n")
            continue

        cons_no = elem_lst[0]
        #cons_shoufeijilu[cons_id] = shoufeijilu.ShouFeiJiLu(elem_lst)
        utils.add_dict_list(cons_shoufeijilu, cons_no, sline.strip('\n'))
    fin.close()
    print "[12] 收费记录表读取完成"


