#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-12-14

import pandas as pd
from numpy import *
from sklearn.externals import joblib


def read_data(train_file, test_file):
    train = pd.read_csv(train_file)
    test = pd.read_csv(test_file)
    return train,test


def refine_label(result_prob):
    final_result = []
    one_cnt = 0
    for ret in result_prob:
        if ret[0] > 0.5:
            final_result.append((0, ret[0]))
        else:
            one_cnt += 1
            final_result.append((1, ret[1]))
    return final_result,one_cnt


def logisitc_regression(train, test, idx):
    print "开始LOGISTIC REGRESSION训练，第"+str(idx+1)+"组......"
    from sklearn import preprocessing
    from sklearn.linear_model import LogisticRegression
    features = train.columns[2:]
    min_max_scaler = preprocessing.MinMaxScaler()
    prep = min_max_scaler.fit(train[features],train["LABEL"])
    joblib.dump(prep, './lab/norm-'+str(5-idx)+'.model')

    clf = LogisticRegression(C=1.0)
    clf.fit(prep.transform(train[features]),train["LABEL"])
    joblib.dump(clf, './lab/lr-'+str(5-idx)+'.model')
    result_prob = clf.predict_proba(prep.transform(test[features]))
    final_result,one_cnt = refine_label(result_prob)

    fout = open('./lab/lr-'+str(5-idx)+'.txt', 'w')
    for ret in final_result:
        fout.write("%s\t%f\n" % (ret[0], ret[1]))
    fout.close()
    print "预测为1的个数为: "+str(one_cnt)


def random_forest(train, test, idx):
    print "开始RANDOM FOREST训练，第"+str(idx+1)+"组......"
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(max_depth=50, n_estimators=200)
    features = train.columns[2:]
    clf.fit(train[features],train["LABEL"])
    joblib.dump(clf, './lab/rf-'+str(5-idx)+'.model')
    result_prob = clf.predict_proba(test[features])
    final_result,one_cnt = refine_label(result_prob)

    fout = open('./lab/rf-'+str(5-idx)+'.txt', 'w')
    for ret in final_result:
        fout.write("%s\t%f\n" % (ret[0], ret[1]))
    fout.close()
    print "预测为1的个数为: "+str(one_cnt)


def gradient_boosting_decision_tree(train, test, idx):
    print "开始GRADIENT BOOSTING DECISION TREE训练，第"+str(idx+1)+"组......"
    from sklearn.ensemble import GradientBoostingClassifier
    features = train.columns[2:]
    clf = GradientBoostingClassifier(n_estimators=150)
    clf.fit(train[features],train["LABEL"])
    joblib.dump(clf, './lab/gbdt-'+str(5-idx)+'.model')
    result_prob = clf.predict_proba(test[features])
    final_result,one_cnt = refine_label(result_prob)

    fout = open('./lab/gbdt-'+str(5-idx)+'.txt', 'w')
    for ret in final_result:
        fout.write("%s\t%f\n" % (ret[0], ret[1]))
    fout.close()
    print "预测为1的个数为: "+str(one_cnt)


def decision_tree(train, test, idx):
    print "开始DECISION TREE训练，第"+str(idx+1)+"组......"
    from sklearn import tree
    features = train.columns[2:]
    clf = tree.DecisionTreeClassifier(max_depth=50)
    clf.fit(train[features],train["LABEL"])
    joblib.dump(clf, './lab/tree-'+str(5-idx)+'.model')
    result_prob = clf.predict_proba(test[features])
    final_result,one_cnt = refine_label(result_prob)

    fout = open('./lab/tree-'+str(5-idx)+'.txt', 'w')
    for ret in final_result:
        fout.write("%s\t%f\n" % (ret[0], ret[1]))
    fout.close()
    print "预测为1的个数为: "+str(one_cnt)



def cross_validation():
    print "开始多模型交叉验证..."
    for i in range(5):
        train_file = './data/train-except-'+str(5-i)+'.csv'
        test_file = './data/test-'+str(5-i)+'.csv'
        train,test = read_data(train_file, test_file)
        logisitc_regression(train, test, i)
        random_forest(train, test, i)
        gradient_boosting_decision_tree(train, test, i)
        decision_tree(train, test, i)



if __name__ == "__main__":
    cross_validation()
