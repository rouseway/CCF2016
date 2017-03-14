#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-12-14

zero_lst = []
one_lst = []

def load_data(filepath):
    fin = open(filepath)
    title = fin.readline()
    while True:
        sline = fin.readline()
        if not sline:
            break
        elem_lst = sline.split(',')
        if elem_lst[1] == '1':
            one_lst.append(sline)
        else:
            zero_lst.append(sline)
    fin.close()
    return title


def split_data(split_lst, split_result):
    list_len = len(split_lst)
    unit_size = list_len / 5
    for i in range(5):
        for j in range(i*unit_size, (i+1)*unit_size):
            if j < list_len:
                split_result[i].append(split_lst[j])
        if i == 4 and j+1 < list_len:
            j += 1
            while j < list_len:
                split_result[i].append(split_lst[j])
                j += 1


def reconstruct_train():
    title = load_data('./data/new-format-train.csv')
    split_result_one = [[],[],[],[],[]]
    split_data(one_lst, split_result_one)
    split_result_zero = [[],[],[],[],[]]
    split_data(zero_lst, split_result_zero)

    for i in range(5):
        fout_train = open("./data/train-except-"+str(5-i)+'.csv', 'w')
        fout_train.write("%s" % title)
        fout_test = open("./data/test-"+str(5-i)+'.csv', 'w')
        fout_test.write("%s" % title)
        for j in range(5):
            if j != 4-i:
                for sline in split_result_one[j]:
                    fout_train.write("%s" % sline)
                for sline in split_result_zero[j]:
                    fout_train.write("%s" % sline)
            else:
                for sline in split_result_one[j]:
                    fout_test.write("%s" % sline)
                for sline in split_result_zero[j]:
                    fout_test.write("%s" % sline)
        fout_train.close()
        fout_test.close()


if __name__ == "__main__":
    reconstruct_train()
