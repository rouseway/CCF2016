#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-24

import sys,gc

import loadtables,utils
import tablebeen.a_gongdan_00
import tablebeen.b_kehutonghua_01
import tablebeen.c_tingdianshijian_02
import tablebeen.d_cuibanduban_03
import tablebeen.e_yongdiankehu_04
import tablebeen.f_yonghudianjia_05
import tablebeen.g_dibaohu_06
import tablebeen.h_feikongyonghu_07
import tablebeen.i_shishoudianfei_08
import tablebeen.j_yingshoudianfei_09
import tablebeen.l_yunxingdianneng_11
import tablebeen.m_shoufeijilu_12

import features

cust2feat = {}
cust2app = {}


onelabel = {}
def load_one_label():
    fin = open("./data/train-1.txt")
    while True:
        sline = fin.readline()
        if not sline:
            break
        onelabel[sline.strip()] = 1
    fin.close()


content_keywords = {}
def load_content_keywords():
    fin = open("./data/content-tag.txt")
    idx = 0
    while True:
        sline = fin.readline()
        if not sline:
            break
        if sline.strip() not in content_keywords:
            content_keywords[sline.strip()] = idx
            idx += 1
    fin.close()


reason_keywords = {}
def load_reason_keywords():
    fin = open("./data/reason-tag.txt")
    idx = 0
    while True:
        sline = fin.readline()
        if not sline:
            break
        if sline.strip() not in reason_keywords:
            reason_keywords[sline.strip()] = idx
            idx += 1
    fin.close()


def create_cust2app(app_gongdan):
    print "创建用户编号与工单号/工单ID的关联关系，工单号与停电事件号的关联关系 ......"
    app_id = {}
    app_poweroff = {}
    for app_no in app_gongdan:
        gongdan = tablebeen.a_gongdan_00.GongDan(app_gongdan[app_no].split('\t'))
        gongdan.extract_poweroff(app_poweroff)
        utils.add_dict_dict(cust2app, gongdan.cust_no, gongdan.app_no)
        app_id[app_no] = gongdan._id
    return app_id,app_poweroff



def deal_with_00_gongdan_table(app_gongdan):
    print "开始提取工单信息表 00_ARC_S_95598_WKST_TRAIN/TEST.TSV 的特征 ......"
    for cust in cust2app:
        for app in cust2app[cust]:
            gongdan = tablebeen.a_gongdan_00.GongDan(app_gongdan[app].split('\t'))
            cust2feat[cust].update_gongdan(gongdan, content_keywords)



def deal_with_01_kehutonghua_table(id_kehutonghua, app_id):
    print "开始提取客户通话信息表 01_S_COMM_REC.TSV 的特征 ......"
    for cust in cust2app:
        for app in cust2app[cust]:
            _id = app_id[app]
            if _id in id_kehutonghua:
                kehutonghua = tablebeen.b_kehutonghua_01.KeHuTongHua(id_kehutonghua[_id].split('\t'))
                cust2feat[cust].update_kehutonghua(kehutonghua.calculate_calling_miniute())


#不处理停电事件表
'''
def deal_with_02_tingdianshijian_table(poweroff_tingdianshijian, app_poweroff):
    print "开始提取停电事件信息表 02_S_REGION_OUTRAGE.TSV 的特征 ......"
    for cust in cust2app:
        for app in cust2app[cust]:
            poweroff_lst = app_poweroff[app]
            for poweroff in poweroff_lst:
                if poweroff in poweroff_tingdianshijian:
                    tingdianshijian = tablebeen.c_tingdianshijian_02.TingDianShiJian(\
                        poweroff_tingdianshijian[poweroff].split('\t'))
                    cust2feat[cust].update_tingdianshijian(tingdianshijian)
'''


def deal_with_03_cuibanduban_table(app_cuibanduban):
    print "开始提取催办督办信息表 03_S_INFO_OVERSEE.TSV 的特征 ......"
    for cust in cust2app:
        for app in cust2app[cust]:
            if app in app_cuibanduban:
                cuibanduban = tablebeen.d_cuibanduban_03.CuiBanDuBan(app_cuibanduban[app].split('\t'))
                cust2feat[cust].update_cuibanduban(cuibanduban, reason_keywords)



def deal_with_04_yongdiankehu_table(cons_yongdiankehu, cons_id):
    print "开始提取用电客户信息表 04_C_CONS.TXT 的特征 ......"
    for cust in cust2app:
        if cust in cons_yongdiankehu:
            for sline in cons_yongdiankehu[cust]:
                yongdiankehu = tablebeen.e_yongdiankehu_04.YongDianKeHu(sline.split('\t'))
                utils.add_dict_list(cons_id, cust, yongdiankehu.cons_id)
                cust2feat[cust].update_yongdiankehu(yongdiankehu)



def deal_with_05_yonghudianjia_table(id_yonghudianjia, cons_id):
    print "开始提取用户电价信息表 05_C_CONS_PRC.TSV 的特征 ......"
    for cust in cust2app:
        if cust in cons_id:
            id_lst = cons_id[cust]
            for _id in id_lst:
                if _id in id_yonghudianjia:
                    yonghudianjia = tablebeen.f_yonghudianjia_05.YongHuDianJia(id_yonghudianjia[_id].split('\t'))
                    cust2feat[cust].update_yonghudianjia(yonghudianjia)



def deal_with_06_dibaohu_table(cons_dibaohu):
     print "开始提取低保户信息表 06_CONT_INFO.TSV 的特征 ......"
     for cust in cust2app:
         if cust in cons_dibaohu:
             dibaohu = tablebeen.g_dibaohu_06.DiBaoHu(cons_dibaohu[cust].split('\t'))
             cust2feat[cust].update_dibaohu(dibaohu)



def deal_with_07_feikongyonghu_table(cons_feikongyonghu):
     print "开始提取费控用户信息表 07_C_RCA_CONS.TSV 的特征 ......"
     for cust in cust2app:
         if cust in cons_feikongyonghu:
             feikongyonghu = tablebeen.h_feikongyonghu_07.FeiKongYongHu(cons_feikongyonghu[cust].split('\t'))
             cust2feat[cust].update_feikongyonghu(feikongyonghu)



def deal_with_08_shishoudianfei_table(cons_shishoudianfei): #cons_shishoudianfei {cons -> List<PayRecord>}
     print "开始提取实收电费信息表 08_A_RCVED_FLOW.TSV 的特征 ......"
     for cust in cust2app:
         if cust in cons_shishoudianfei:
             pay_lst = cons_shishoudianfei[cust]
             for pay in pay_lst:
                shishoudianfei = tablebeen.i_shishoudianfei_08.ShiShouDianFei(pay.split('\t'))
                cust2feat[cust].update_shishoudianfei(shishoudianfei)



def deal_with_09_yingshoudianfei_table(cons_yingshoudianfei): #cons_yingshoudianfei {cons -> List<PayRecord>}
    print "开始提取应收电费信息表 09_ARC_A_RCVBL_FLOW.TSV 的特征 ......"
    for cust in cust2app:
        if cust in cons_yingshoudianfei:
            pay_lst = cons_yingshoudianfei[cust]
            for pay in pay_lst:
                yingshoudianfei = tablebeen.j_yingshoudianfei_09.YingShouDianFei(pay.split('\t'))
                cust2feat[cust].update_yingshoudianfei(yingshoudianfei)



def deal_with_11_yunxingdianneng_table(id_yunxingdianneng, cons_id):
    print "开始提取运行电能表信息表 11_C_METER.TSV 的特征 ......"
    for cust in cust2app:
        if cust in cons_id:
            id_lst = cons_id[cust]
            for _id in id_lst:
                if _id in id_yunxingdianneng:
                    yunxingdianneng = tablebeen.l_yunxingdianneng_11.YunXingDianNeng(id_yunxingdianneng[_id].split('\t'))
                    cust2feat[cust].update_yunxingdianneng(yunxingdianneng)



def deal_with_12_shoufeijilu_table(cons_shoufeijilu): #cons_shoufeijilu {cons -> List<PayRecord>}
    print "开始提取收费记录信息表 12_A_PAY_FLOW.TSV 的特征 ......"
    for cust in cust2app:
        if cust in cons_shoufeijilu:
            pay_lst = cons_shoufeijilu[cust]
            for pay in pay_lst:
                shoufeijilu = tablebeen.m_shoufeijilu_12.ShouFeiJiLu(pay.split('\t'))
                cust2feat[cust].update_shoufeijilu(shoufeijilu)



def output_features(flag):
    print len(cust2feat)
    fout = None
    if flag == 'train':
        fout = open("./data/format-train.csv", 'w')
    else:
        fout = open("./data/format-test.csv", 'w')
    features.feat.output_feature_title(fout, content_keywords, reason_keywords)
    for cust in cust2feat:
        label = 0
        if cust in onelabel:
            label = 1
        fout.write("%s,%d," % (cust,label))
        cust2feat[cust].output_features(fout)
        fout.write('\n')
    fout.close()



def deal(flag):
    #加载训练数据标签和关键词资源
    load_one_label()
    load_content_keywords()
    load_reason_keywords()

    #创建用户->工单号的映射关系
    app_gongdan = {}
    if flag == 'train':
        loadtables.load_GongDan_table(app_gongdan, "./data/00_arc_s_95598_wkst_train.tsv")
    else:
        loadtables.load_GongDan_table(app_gongdan, "./data/00_arc_s_95598_wkst_test.tsv")
    app_id,app_poweroff = create_cust2app(app_gongdan)
    print "需要处理 "+str(len(cust2app))+" 名用户......"

    #初始化用户->特征的映射关系
    for cust in cust2app:
        cust2feat[cust] = features.feat(cust, len(content_keywords), len(reason_keywords))

    #提取 00 表的特征，事后释放app_gongdan
    deal_with_00_gongdan_table(app_gongdan)
    app_gongdan.clear()
    del(app_gongdan)
    gc.collect()


    #提取 01 表的特征，事后释放id_kehutonghua
    id_kehutonghua = {}
    loadtables.load_KeHuTongHua_table(id_kehutonghua)
    deal_with_01_kehutonghua_table(id_kehutonghua, app_id)
    id_kehutonghua.clear()
    del(id_kehutonghua)
    gc.collect()


    '''不处理停电信息表
    #提取 02 表的特征，事后释放poweroff_tingdianshijian
    poweroff_tingdianshijian = {}
    loadtables.load_TingDianShiJian_table(poweroff_tingdianshijian)
    deal_with_02_tingdianshijian_table(poweroff_tingdianshijian, app_poweroff)
    poweroff_tingdianshijian.clear()
    app_poweroff.clear()
    del(poweroff_tingdianshijian)
    del(app_poweroff)
    gc.collect()
    '''

    #提取 03 表的特征，事后释放app_cuibanduban
    app_cuibanduban = {}
    loadtables.load_CuiBanDuBan_table(app_cuibanduban)
    deal_with_03_cuibanduban_table(app_cuibanduban)
    app_cuibanduban.clear()
    del(app_cuibanduban)
    gc.collect()

    #提取 04 表的特征，事后释放cons_yongdiankehu
    cons_id = {}
    cons_yongdiankehu = {}
    loadtables.load_YongDianKeHu_table(cons_yongdiankehu)
    deal_with_04_yongdiankehu_table(cons_yongdiankehu, cons_id)
    cons_yongdiankehu.clear()
    del(cons_yongdiankehu)
    gc.collect()

    #提取 05 表的特征，事后释放cons_yonghudianjia
    id_yonghudianjia = {}
    loadtables.load_YongHuDianJia_table(id_yonghudianjia)
    deal_with_05_yonghudianjia_table(id_yonghudianjia, cons_id)
    id_yonghudianjia.clear()
    del(id_yonghudianjia)
    gc.collect()

    #提取 06 表的特征，事后释放cons_dibaohu
    cons_dibaohu = {}
    loadtables.load_DiBaoHu_table(cons_dibaohu)
    deal_with_06_dibaohu_table(cons_dibaohu)
    cons_dibaohu.clear()
    del(cons_dibaohu)
    gc.collect()

    #提取 07 表的特征，事后释放cons_feikongyonghu
    cons_feikongyonghu = {}
    loadtables.load_FeiKongYongHu_table(cons_feikongyonghu)
    deal_with_07_feikongyonghu_table(cons_feikongyonghu)
    cons_feikongyonghu.clear()
    del(cons_feikongyonghu)
    gc.collect()

    #提取 08 表的特征，事后释放cons_shishoudianfei
    cons_shishoudianfei = {}
    loadtables.load_ShiShouDianFei_table(cons_shishoudianfei)
    deal_with_08_shishoudianfei_table(cons_shishoudianfei)
    cons_shishoudianfei.clear()
    del(cons_shishoudianfei)
    gc.collect()


    #提取 09 表的特征，事后释放cons_yingshoudianfei
    cons_yingshoudianfei = {}
    loadtables.load_YingShouDianFei_table(cons_yingshoudianfei)
    deal_with_09_yingshoudianfei_table(cons_yingshoudianfei)
    cons_yingshoudianfei.clear()
    del(cons_yingshoudianfei)
    gc.collect()


    #提取 11 表的特征，事后释放meter_yunxingdianneng
    id_yunxingdianneng = {}
    loadtables.load_YunXingDianNeng_table(id_yunxingdianneng)
    deal_with_11_yunxingdianneng_table(id_yunxingdianneng, cons_id)
    id_yunxingdianneng.clear()
    del(id_yunxingdianneng)
    gc.collect()


    #提取 12 表的特征，事后释放cons_shoufeijilu
    cons_shoufeijilu = {}
    loadtables.load_ShouFeiJiLu_table(cons_shoufeijilu)
    deal_with_12_shoufeijilu_table(cons_shoufeijilu)
    cons_shoufeijilu.clear()
    del(cons_shoufeijilu)
    gc.collect()


    #输出特征
    output_features(flag)




if __name__ == "__main__":
    deal(sys.argv[1])
