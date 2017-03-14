#-*- coding:gbk -*-
#author: raosiwei
#date: 2016-12-14

import sys
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


def load_model_weight():
    model_weights = []
    for i in range(5):
        fin = open('./lab/para-'+str(i+1)+'.txt')
        section_models = {}
        while True:
            sline = fin.readline()
            if not sline:
                break
            model,weight = sline.strip().split('\t')
            section_models[model] = float(weight)
        fin.close()
        model_weights.append(section_models)
    return model_weights



def refine_model_predict_prob(idx, model_weights, lr_predict, rf_predict, gbdt_predict, tree_predict):
    weight_dict  = model_weights[idx]
    prob = [0, 0]
    for i in range(2):
        prob[i] = weight_dict['lr']*lr_predict[i] + weight_dict['rf']*rf_predict[i] + \
            weight_dict['gbdt']*gbdt_predict[i] + weight_dict['tree']*tree_predict[i]
    return prob


def multi_model_predict():
    model_weights = load_model_weight()
    test = pd.read_csv('./data/new-format-test.csv')
    features = test.columns[2:]

    vote_result = []
    for i in range(201246):
        vote_result.append([0, 0])

    for i in range(5):
        lr_predict_result = lr_models[i].predict_proba(norm_models[i].transform(test[features]))
        rf_predict_result = rf_models[i].predict_proba(test[features])
        gbdt_predict_result = gbdt_models[i].predict_proba(test[features])
        tree_predict_result = tree_models[i].predict_proba(test[features])

        fout = open('./predict-'+str(i+1)+'.txt', 'w')
        for j in range(len(lr_predict_result)):
            prob = refine_model_predict_prob(i, model_weights, lr_predict_result[j], \
                    rf_predict_result[j], gbdt_predict_result[j], tree_predict_result[j])
            if prob[0] > prob[1]:
                vote_result[j][0] += 1
            else:
                vote_result[j][1] += 1
            fout.write("%f\t%f\n" % (prob[0], prob[1]))
        fout.close()

    for vote in vote_result:
        sys.stderr.write("%d\t%d\n" % (vote[0], vote[1]))
        if vote[0] > vote[1]:
            print '0'
        else:
            print '1'



if __name__ == "__main__":
    load_model_by_group()
    multi_model_predict()




