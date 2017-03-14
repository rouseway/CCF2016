#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-12-14

import pandas as pd
from numpy import *
from sklearn.externals import joblib

lr_models = []
rf_models = []
gbdt_models = []
tree_models = []
norm_models = []


def load_model(name_str, models_lst):
    for i in range(5):
        clf = joblib.load('./lab/'+name_str+str(i+1)+'.model')
        models_lst.append(clf)


def load_model_by_group():
    load_model('lr-', lr_models)
    load_model('rf-', rf_models)
    load_model('gbdt-', gbdt_models)
    load_model('tree-', tree_models)
    load_model('norm-', norm_models)



def refine_predict_prob(prob_result_lst, predict_prob):
    if len(prob_result_lst) == 0:
        for label,prob in predict_prob:
            ret = [0, 0]
            if label == 1:
                ret[0] = 1 - float(prob)
                ret[1] = float(prob)
            else:
                ret[0] = float(prob)
                ret[1] = 1 - float(prob)
            prob_result_lst.append(ret)
    else:
        for i in range(len(predict_prob)):
            if predict_prob[i][0] == 1:
                prob_result_lst[i][0] += 1 - predict_prob[i][1]
                prob_result_lst[i][1] += predict_prob[i][1]
            else:
                prob_result_lst[i][0] += predict_prob[i][1]
                prob_result_lst[i][1] += 1 - predict_prob[i][1]


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

    fin = open('./remain-feat.txt')
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


def output_title(fout, feat_title_lst):
    fout.write("%s" % "ID,LABEL")
    for title in feat_title_lst:
        fout.write(",%s" % title)
    fout.write("%s\n" % ",LR-0,LR-1,RF-0,RF-1,GBDT-0,GBDT-1,TREE-0,TREE-1")


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




def produce_stacking_format_test():
    test = pd.read_csv('./data/new-format-test.csv')
    features = test.columns[2:]

    lr_predict_result = []
    rf_predict_result = []
    gbdt_predict_result = []
    tree_predict_result = []

    for i in range(5):
        refine_predict_prob(lr_predict_result, lr_models[i].predict_proba(norm_models[i].transform(test[features])))
        refine_predict_prob(rf_predict_result, rf_models[i].predict_proba(test[features]))
        refine_predict_prob(gbdt_predict_result, gbdt_models[i].predict_proba(test[features]))
        refine_predict_prob(tree_predict_result, tree_models[i].predict_proba(test[features]))
    alg_predict_result = {'lr':lr_predict_result, 'rf':rf_predict_result, 'gbdt':gbdt_predict_result, \
                          'tree':tree_predict_result}

    fout = open('./stacking-format-test.csv', 'w')
    feat_title_lst,feat_idx_lst = load_remain_feature_idx()
    output_title(fout, feat_title_lst)

    orig_features = load_orig_features('./data/new-format-test.csv')

    produce_new_features(fout, orig_features, alg_predict_result, feat_idx_lst)
    fout.close()




if __name__ == "__main__":
    load_model_by_group()
    produce_stacking_format_test()
