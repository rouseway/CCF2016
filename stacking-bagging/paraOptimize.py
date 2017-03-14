#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-12-14


def load_std_answer(std_answers):
    for i in range(5):
        fin = open('./data/std-'+str(i+1)+'.txt')
        while True:
            sline = fin.readline()
            if not sline:
                break
            std_answers[i].append(int(sline.strip()))
        fin.close()


def load_result(filepath):
    predict_prob = []
    fin = open(filepath)
    while True:
        sline = fin.readline()
        if not sline:
            break
        label,prob_str = sline.strip().split('\t')
        if label == '1':
            predict_prob.append((1-float(prob_str), float(prob_str)))
        else:
            predict_prob.append((float(prob_str), 1-float(prob_str)))
    fin.close()
    return predict_prob


def calculate_w_x_models(para_dict, idx, lr_result, rf_result, gbdt_result, tree_result):
    return para_dict['lr']*lr_result[idx][1] + para_dict['rf']*+rf_result[idx][1] + \
            para_dict['gbdt']*gbdt_result[idx][1] + para_dict['tree']*tree_result[idx][1]


def get_alg_precit_prob(alg, i, lr_result, rf_result, gbdt_result, tree_result):
    if alg == 'lr':
        return lr_result[i][1]
    elif alg == 'rf':
        return rf_result[i][1]
    elif alg == 'gbdt':
        return gbdt_result[i][1]
    else:
        return tree_result[i][1]



def update_parameters(para_dict, lr_result, rf_result, gbdt_result, tree_result, std_answer):
    delta_para_dict = { 'lr':0.0, 'rf':0.0, 'gbdt':0.0, 'tree':0.0 }
    for i in range(len(std_answer)):
        if std_answer[i] == 1:
            a = calculate_w_x_models(para_dict, i, lr_result, rf_result, gbdt_result, tree_result)
            for alg in para_dict:
                b = get_alg_precit_prob(alg, i, lr_result, rf_result, gbdt_result, tree_result)
                delta_para_dict[alg] += b / (a+0.000001)

    stop = 0
    for alg in para_dict:
        delta = 1.0/62000000 * delta_para_dict[alg]
        print delta
        if delta < 0.0001:
            stop += 1
        para_dict[alg] += delta
    if stop == 4:
        return True
    else:
        return False


def normalize_para_dict(para_dict):
    sum_weight = 0
    for alg in para_dict:
        sum_weight += para_dict[alg]
    for alg in para_dict:
        para_dict[alg] = para_dict[alg]/sum_weight


def display_iteration_info(idx, iter_num, para_dict):
    print "="+str(idx+1)+"==="+str(iter_num)+' LR='+str(para_dict['lr'])+' RF='+str(para_dict['rf'])+\
        ' GBDT='+str(para_dict['gbdt'])+' TREE='+str(para_dict['tree'])


def optimize_by_group():
    std_answers = [[],[],[],[],[]]
    load_std_answer(std_answers)

    for i in range(5):
        print "迭代计算第"+str(i+1)+"个数据块上的模型权重......"
        lr_result = load_result('./lab/lr-'+str(i+1)+'.txt')
        rf_result = load_result('./lab/rf-'+str(i+1)+'.txt')
        gbdt_result = load_result('./lab/gbdt-'+str(i+1)+'.txt')
        tree_result = load_result('./lab/tree-'+str(i+1)+'.txt')

        #初始化模型权重参数（均分）
        para_dict = { 'lr':0.25, 'rf':0.25, 'gbdt':0.25, 'tree':0.25 }
        iter_num = 0
        while True:
            flag = update_parameters(para_dict, lr_result, rf_result, gbdt_result, tree_result, std_answers[i])
            display_iteration_info(i, iter_num, para_dict)
            iter_num += 1
            if flag == True or iter_num > 100000:
                normalize_para_dict(para_dict)
                fout = open('./lab/para-'+str(i+1)+'.txt', 'w')
                for alg in para_dict:
                    fout.write("%s\t%f\n" % (alg, para_dict[alg]))
                fout.close()
                break


if __name__ == "__main__":
    optimize_by_group()
