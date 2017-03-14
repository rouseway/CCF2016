#-*- coding:utf-8 -*-

import jieba.posseg

import sys,re
import loadtables,utils
import tablebeen.a_gongdan_00
import tablebeen.d_cuibanduban_03


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

tag_dict  = {}
def update_dict(key):
    if key not in tag_dict:
        tag_dict[key] = 1
    else:
        tag_dict[key] += 1


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



def deal_with_03_cuibanduban_table(app_cuibanduban):
    print "开始提取催办督办信息表 03_S_INFO_OVERSEE.TSV 的特征 ......"
    bracket_pattern = re.compile(u'【(.+?)】')
    for cust in cust2app:
        if cust in onelabel:
            for app in cust2app[cust]:
                if app in app_cuibanduban:
                    cuibanduban = tablebeen.d_cuibanduban_03.CuiBanDuBan(app_cuibanduban[app].split('\t'))
                    m_result = bracket_pattern.findall(cuibanduban.oversee_reason.decode('utf-8'))
                    for ret in m_result:
                        update_dict(ret.encode('utf-8'))
                    '''
                    segs = jieba.posseg.cut(cuibanduban.oversee_reason)
                    jieba_seg_list = list(segs)
                    for i in range(len(jieba_seg_list)):
                        update_dict(jieba_seg_list[i].word.encode('utf-8'))
                    '''


def deal():
    #加载训练数据标签和关键词资源
    load_one_label()

    #创建用户->工单号的映射关系
    app_gongdan = {}
    loadtables.load_GongDan_table(app_gongdan, "./data/00_arc_s_95598_wkst_train.tsv")
    app_id,app_poweroff = create_cust2app(app_gongdan)
    print "需要处理 "+str(len(cust2app))+" 名用户......"


    #提取 03 表的特征，事后释放app_cuibanduban
    app_cuibanduban = {}
    loadtables.load_CuiBanDuBan_table(app_cuibanduban)
    deal_with_03_cuibanduban_table(app_cuibanduban)

    tag_sort_lst = sorted(tag_dict.iteritems(), key=lambda d:d[1], reverse=True)
    for tag,freq in tag_sort_lst:
        sys.stderr.write("%s,%d\n" % (tag.decode('utf-8').encode('gb18030'),freq))


if __name__ == "__main__":
    deal()