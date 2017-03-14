#-*- coding:utf-8 -*-
import sklearn
import pandas as pd
from numpy import *
import sys,types

std_one_cnt = 0    

def read_data():
    train = pd.read_csv(sys.argv[2])
    test = pd.read_csv(sys.argv[3])
    all_train = pd.read_csv(sys.argv[4])
    return train,test,all_train


def read_std_answer(filepath):
    stdanswer = []
    global std_one_cnt
    std_one_cnt = 0
    fin = open(filepath)
    fin.readline()
    while True:
        sline = fin.readline()
        if not sline:
            break
        elem_lst = sline.split(',')
        label = int(elem_lst[1])
        stdanswer.append(label)
        if label == 1:
            std_one_cnt += 1
    fin.close()
    return stdanswer


def check_correct(para, result, filepath):
    stdanswer = read_std_answer(filepath)
    global std_one_cnt
    correct_cnt = 0
    ret_one_cnt = 0
    for i in range(len(result)):
        if result[i] == 1:
            ret_one_cnt += 1
            if stdanswer[i] == 1:
                correct_cnt += 1
    if ret_one_cnt == 0:
        sys.stdout.write("算法：%s 判断为1个数：%d 正确个数：%d 标准答案：%d F1=%f\n" % \
                     (para,ret_one_cnt,correct_cnt,std_one_cnt,0))
    else:
        pre = correct_cnt*1.0 / ret_one_cnt
        recall = correct_cnt*1.0 / std_one_cnt
        f1 = (2*pre*recall)/(pre+recall)
        sys.stdout.write("算法：%s 判断为1个数：%d 正确个数：%d 标准答案：%d F1=%f\n" % \
                         (para,ret_one_cnt,correct_cnt,std_one_cnt,f1))


def naive_bayes(train, test, all_train):
    one_cnt = 0
    from sklearn import preprocessing
    from sklearn.naive_bayes import MultinomialNB
    features = train.columns[2:]
    min_max_scaler = preprocessing.MinMaxScaler()
    prep = min_max_scaler.fit(train[features],train["LABEL"])
    
    clf = MultinomialNB(alpha=0.01)
    clf.fit(prep.transform(train[features]),train["LABEL"])
    result = clf.predict(prep.transform(train[features]))
    check_correct("NAIVY BAYES 0.6",result,sys.argv[2])
    result = clf.predict(prep.transform(test[features]))
    check_correct("NAIVY BAYES 0.4",result,sys.argv[3])
    result = clf.predict(prep.transform(all_train[features]))
    check_correct("NAIVY BAYES 1.0",result,sys.argv[4])


def knn(train, test, all_train):
    one_cnt = 0
    from sklearn import preprocessing
    from sklearn.neighbors import KNeighborsClassifier
    features = train.columns[2:]
    min_max_scaler = preprocessing.MinMaxScaler()
    prep = min_max_scaler.fit(train[features],train["LABEL"])
    
    clf = KNeighborsClassifier()
    clf.fit(prep.transform(train[features]),train["LABEL"])
    result = clf.predict(prep.transform(test[features]))
    check_correct("KNN",result)


def decision_tree(train, test, all_train):
    one_cnt = 0
    from sklearn import tree
    features = train.columns[2:]
    clf = tree.DecisionTreeClassifier(max_depth=18)
    clf.fit(train[features],train["LABEL"])
    result = clf.predict(train[features])
    check_correct("DECISION TREE 0.6",result,sys.argv[2])
    result = clf.predict(test[features])
    check_correct("DECISION TREE 0.4",result,sys.argv[3])
    result = clf.predict(all_train[features])
    check_correct("DECISION TREE 1.0",result,sys.argv[4])


def gradient_boosting_decision_tree(train, test, all_train):
    one_cnt = 0
    from sklearn.ensemble import GradientBoostingClassifier
    features = train.columns[2:]
    clf = GradientBoostingClassifier(n_estimators=180)
    clf.fit(train[features],train["LABEL"])
    result = clf.predict(train[features])
    check_correct("GBDT 0.6",result,sys.argv[2])
    result = clf.predict(test[features])
    check_correct("GBDT 0.4",result,sys.argv[3])
    result = clf.predict(all_train[features])
    check_correct("GBDT 1.0",result,sys.argv[4])


def logisitc_regression(train, test, all_train):
    one_cnt = 0
    from sklearn import preprocessing
    from sklearn.linear_model import LogisticRegression
    features = train.columns[2:]
    min_max_scaler = preprocessing.MinMaxScaler()
    prep = min_max_scaler.fit(train[features],train["LABEL"])
    
    clf = LogisticRegression(C=1.0)
    clf.fit(prep.transform(train[features]),train["LABEL"])
    result = clf.predict(prep.transform(train[features]))
    check_correct("LOGISTIC REGRESSION 0.6",result,sys.argv[2])
    result = clf.predict(prep.transform(test[features]))
    check_correct("LOGISTIC REGRESSION 0.4",result,sys.argv[3])
    result = clf.predict(prep.transform(all_train[features]))
    check_correct("LOGISTIC REGRESSION 1.0",result,sys.argv[4])


depth = [10,15,20,25,30,35,40,45,50]
estimators = [60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]

def random_forest(train, test, all_train):
    one_cnt = 0
    from sklearn.ensemble import RandomForestClassifier
    for i in range(len(depth)):
        for j in range(len(estimators)):
            sys.stdout.write("PARAMETERS:\tmax_depth=%d, n_estimators=%d\n" % (depth[i], estimators[j]))
            clf = RandomForestClassifier(max_depth=depth[i], n_estimators=estimators[j])
            features = train.columns[2:]
            clf.fit(train[features],train["LABEL"])
            result = clf.predict(train[features])
            check_correct("RANDOM FOREST 0.6",result,sys.argv[2])
            result = clf.predict(test[features])
            check_correct("RANDOM FOREST 0.4",result,sys.argv[3])
            result = clf.predict(all_train[features])
            check_correct("RANDOM FOREST 1.0",result,sys.argv[4])


def ada_boosting(train, test, all_train):
    one_cnt = 0
    from sklearn.ensemble import AdaBoostClassifier
    clf = AdaBoostClassifier(n_estimators=150,learning_rate=0.01)
    features = train.columns[2:]
    clf.fit(train[features],train["LABEL"])
    result = clf.predict(train[features])
    check_correct("ADA BOOSTING 0.6",result,sys.argv[2])
    result = clf.predict(test[features])
    check_correct("ADA BOOSTING 0.4",result,sys.argv[3])
    result = clf.predict(all_train[features])
    check_correct("ADA BOOSTING 1.0",result,sys.argv[4])


def supported_vector_machine(train, test, all_train):
    one_cnt = 0
    from sklearn import preprocessing
    from sklearn import svm
    features = train.columns[2:]
    min_max_scaler = preprocessing.MinMaxScaler()
    prep = min_max_scaler.fit(train[features],train["LABEL"])
    
    clf =svm.SVC(kernel='rbf').fit(prep.transform(train[features]),train["LABEL"])
    result = clf.predict(prep.transform(test[features]))
    check_correct("SVM",result)


if __name__ == "__main__":
    train,test,all_train = read_data()
    if sys.argv[1] == 'lr':
        logisitc_regression(train, test, all_train)
    elif sys.argv[1] == 'rf':
        random_forest(train, test, all_train)
    elif sys.argv[1] == 'ada':
        ada_boosting(train, test, all_train)
    elif sys.argv[1] == 'svm':
        supported_vector_machine(train, test, all_train)
    elif sys.argv[1] == 'bayes':
        naive_bayes(train, test, all_train)
    elif sys.argv[1] == 'knn':
        knn(train, test, all_train)
    elif sys.argv[1] == 'tree':
        decision_tree(train, test, all_train)
    elif sys.argv[1] == 'gbdt':
        gradient_boosting_decision_tree(train, test, all_train)

        
    

