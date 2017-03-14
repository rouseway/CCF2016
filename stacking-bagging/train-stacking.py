#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-12-14


def load_orig_features(filepath):
    fin = open(filepath)
    orig_feat_lst = []
    fin.readline()
    while True:
        sline = fin.readline()
        if not sline:
            break
        orig_feat_lst.append(sline.strip())
    fin.close()
    return orig_feat_lst


def load_remain_feature_idx():
    fin = open('./title.txt')
    title_lst = fin.readlines()
    fin.close()

    fin = open('remain-feat.txt')
    feat_title_lst = []
    feat_idx_lst = []
    while True:
        sline = fin.readline()
        if not sline:
            break
        idx = int(sline.strip()) - 1
        feat_idx_lst.append(idx)
        feat_title_lst.append(title_lst[idx].strip())
    fin.close()
    return feat_title_lst,feat_idx_lst


def load_cv_predict_result(alg, filepath, alg_predict_result):
    fin = open(filepath)
    final_prob_result = []
    while True:
        sline = fin.readline()
        if not sline:
            break
        label,prob = sline.strip().split('\t')
        ret = [0, 0]
        if label == '1':
            ret[0] = 1 - float(prob)
            ret[1] = float(prob)
        else:
            ret[0] = float(prob)
            ret[1] = 1 - float(prob)
        final_prob_result.append(ret)
    fin.close()
    alg_predict_result[alg] = final_prob_result



def produce_remain_feature(feat_lst, orig_features, remain_feat_idx, idx):
    elem_lst = orig_features[idx].split(',')
    feat_lst.append(elem_lst[0]) #用户编号
    feat_lst.append(elem_lst[1]) #标签
    for remain_feat in remain_feat_idx:
        feat_lst.append(elem_lst[remain_feat])


def produce_alg_stacking_feature(feat_lst, alg_predict_result, idx):
    alg_lst = ['lr', 'rf', 'gbdt', 'tree']
    for alg in alg_lst:
        predict_prob = alg_predict_result[alg][idx]
        feat_lst.append(predict_prob[0])
        feat_lst.append(predict_prob[1])



def produce_new_features(fout, orig_features, alg_predict_result, remain_feat_idx):
    for i in range(len(alg_predict_result['lr'])):
        feat_lst = []
        produce_remain_feature(feat_lst, orig_features, remain_feat_idx, i)
        produce_alg_stacking_feature(feat_lst, alg_predict_result, i)
        for i in range(len(feat_lst)-1):
            fout.write("%s," % feat_lst[i])
        fout.write("%s\n" % feat_lst[len(feat_lst)-1])


def output_title(fout, feat_title_lst):
    fout.write("%s" % "ID,LABEL")
    for title in feat_title_lst:
        fout.write(",%s" % title)
    fout.write("%s\n" % ",LR-0,LR-1,RF-0,RF-1,GBDT-0,GBDT-1,TREE-0,TREE-1")


def stacking_feature():
    fout = open('./stacking-format-train.csv', 'w')
    feat_title_lst,feat_idx_lst = load_remain_feature_idx()
    output_title(fout, feat_title_lst)

    for i in range(5):
        alg_predict_result = {}
        load_cv_predict_result('lr', './lab/lr-'+str(i+1)+'.txt', alg_predict_result)
        load_cv_predict_result('rf', './lab/rf-'+str(i+1)+'.txt', alg_predict_result)
        load_cv_predict_result('gbdt', './lab/gbdt-'+str(i+1)+'.txt', alg_predict_result)
        load_cv_predict_result('tree', './lab/tree-'+str(i+1)+'.txt', alg_predict_result)

        test_file = './data/test-'+str(i+1)+'.csv'
        orig_features = load_orig_features(test_file)

        produce_new_features(fout, orig_features, alg_predict_result, feat_idx_lst)

    fout.close()


if __name__ == "__main__":
    stacking_feature()