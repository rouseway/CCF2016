#-*- coding:utf-8 -*-
import pandas as pd
from numpy import *
import sys



def read_data():
    train = pd.read_csv(sys.argv[2])
    test = pd.read_csv(sys.argv[3])
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

	
	
def naive_bayes(train, test):
    from sklearn import preprocessing
    from sklearn.naive_bayes import MultinomialNB
    features = train.columns[2:]
    min_max_scaler = preprocessing.MinMaxScaler()
    prep = min_max_scaler.fit(train[features],train["LABEL"])
    
    clf = MultinomialNB(alpha=0.01)
    clf.fit(prep.transform(train[features]),train["LABEL"])
    result_prob = clf.predict_proba(prep.transform(test[features]))
    final_result,one_cnt = refine_label(result_prob)
    for ret in final_result:
        sys.stdout.write("%s\t%f\n" % (ret[0], ret[1]))
    sys.stderr.write("%d\n" % one_cnt)



def knn(train, test):
    from sklearn import preprocessing
    from sklearn.neighbors import KNeighborsClassifier
    features = train.columns[2:]
    min_max_scaler = preprocessing.MinMaxScaler()
    prep = min_max_scaler.fit(train[features],train["LABEL"])
    
    clf = KNeighborsClassifier()
    clf.fit(prep.transform(train[features]),train["LABEL"])
    result_prob = clf.predict_proba(prep.transform(test[features]))
    final_result,one_cnt = refine_label(result_prob)
    for ret in final_result:
        sys.stdout.write("%s\t%f\n" % (ret[0], ret[1]))
    sys.stderr.write("%d\n" % one_cnt)



def decision_tree(train, test):
    from sklearn import tree
    features = train.columns[2:]
    clf = tree.DecisionTreeClassifier(max_depth=18)
    clf.fit(train[features],train["LABEL"])
    result_prob = clf.predict_proba(test[features])
    final_result,one_cnt = refine_label(result_prob)
    for ret in final_result:
        sys.stdout.write("%s\t%f\n" % (ret[0], ret[1]))
    sys.stderr.write("%d\n" % one_cnt)

	

def gradient_boosting_decision_tree(train, test):
    from sklearn.ensemble import GradientBoostingClassifier
    features = train.columns[2:]
    clf = GradientBoostingClassifier(n_estimators=150)
    clf.fit(train[features],train["LABEL"])
    result_prob = clf.predict_proba(test[features])
    final_result,one_cnt = refine_label(result_prob)
    for ret in final_result:
        sys.stdout.write("%s\t%f\n" % (ret[0], ret[1]))
    sys.stderr.write("%d\n" % one_cnt)



def logisitc_regression(train, test):
    from sklearn import preprocessing
    from sklearn.linear_model import LogisticRegression
    features = train.columns[2:]
    min_max_scaler = preprocessing.MinMaxScaler()
    prep = min_max_scaler.fit(train[features],train["LABEL"])
    
    clf = LogisticRegression(C=1.0)
    clf.fit(prep.transform(train[features]),train["LABEL"])
    result_prob = clf.predict_proba(prep.transform(test[features]))
    final_result,one_cnt = refine_label(result_prob)
    for ret in final_result:
        sys.stdout.write("%s\t%f\n" % (ret[0], ret[1]))
    sys.stderr.write("%d\n" % one_cnt)



def random_forest(train, test):
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(max_depth=30, n_estimators=150)
    features = train.columns[2:]
    clf.fit(train[features],train["LABEL"])
    result_prob = clf.predict_proba(test[features])
    final_result,one_cnt = refine_label(result_prob)
    for ret in final_result:
        sys.stdout.write("%s\t%f\n" % (ret[0], ret[1]))
    sys.stderr.write("%d\n" % one_cnt)



def stochastic_gradient_descent(train, test):
    from sklearn import preprocessing
    from sklearn.linear_model import SGDClassifier
    features = train.columns[2:]
    min_max_scaler = preprocessing.MinMaxScaler()
    prep = min_max_scaler.fit(train[features],train["LABEL"])

    clf = SGDClassifier(loss="modified_huber", penalty='l2')
    clf.fit(prep.transform(train[features]),train["LABEL"])
    result_prob = clf.predict_proba(prep.transform(test[features]))
    final_result,one_cnt = refine_label(result_prob)
    for ret in final_result:
        sys.stdout.write("%d\t%f\n" % (ret[0],ret[1]))
    sys.stderr.write("%d\n" % one_cnt)



def extreme_gradient_boosting(train, test):
    from sklearn.ensemble import GradientBoostingClassifier
    features = train.columns[2:]
    clf = GradientBoostingClassifier(learning_rate=0.2)
    clf.fit(train[features],train["LABEL"])
    result_prob = clf.predict_proba(test[features])
    final_result,one_cnt = refine_label(result_prob)
    for ret in final_result:
        sys.stdout.write("%d\t%f\n" % (ret[0],ret[1]))
    sys.stderr.write("%d\n" % one_cnt)



def ada_boosting(train, test):
    from sklearn.ensemble import AdaBoostClassifier
    clf = AdaBoostClassifier(n_estimators=150,learning_rate=0.01)
    features = train.columns[2:]
    clf.fit(train[features],train["LABEL"])
    result_prob = clf.predict_proba(test[features])
    final_result,one_cnt = refine_label(result_prob)
    for ret in final_result:
        sys.stdout.write("%s\t%f\n" % (ret[0], ret[1]))
    sys.stderr.write("%d\n" % one_cnt)



def supported_vector_machine(train, test):
    from sklearn import preprocessing
    from sklearn import svm
    features = train.columns[2:]
    min_max_scaler = preprocessing.MinMaxScaler()
    prep = min_max_scaler.fit(train[features],train["LABEL"])
    
    clf =svm.SVC(kernel='rbf',probability=True).fit(prep.transform(train[features]),train["LABEL"])
    result_prob = clf.predict_proba(prep.transform(test[features]))
    final_result,one_cnt = refine_label(result_prob)
    for ret in final_result:
        sys.stdout.write("%s\t%f\n" % (ret[0], ret[1]))
    sys.stderr.write("%d\n" % one_cnt)


	

if __name__ == "__main__":
    train,test = read_data()

    if sys.argv[1] == 'lr':
        logisitc_regression(train, test)
    elif sys.argv[1] == 'rf':
        random_forest(train, test)
    elif sys.argv[1] == 'sgd':
        stochastic_gradient_descent(train, test)
    elif sys.argv[1] == 'gbdt':
        gradient_boosting_decision_tree(train, test)
    elif sys.argv[1] == 'xgb':
        extreme_gradient_boosting(train, test)
    elif sys.argv[1] == 'svm':
        supported_vector_machine(train, test)
    elif sys.argv[1] == 'knn':
        knn(train, test)
    elif sys.argv[1] == 'bayes':
        naive_bayes(train, test)
    elif sys.argv[1] == 'ada':
        ada_boosting(train, test)
    elif sys.argv[1] == 'tree':
        decision_tree(train, test)
