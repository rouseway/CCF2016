#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-22

import sys,datetime


def convert_to_date_YM(filepath, t_str):
    dt = None
    try:
        dt = datetime.datetime.strptime(t_str, '%Y%m')
    except ValueError as e:
        sys.stderr.write("[DATE WRONG FORMAT]: "+filepath+"  "+t_str+"\n")
    return dt


def convert_to_date_YMD(filepath, t_str):
    dt = None
    try:
        dt = datetime.datetime.strptime(t_str, '%Y%m%d')
    except ValueError as e:
        sys.stderr.write("[DATE WRONG FORMAT]: "+filepath+"  "+t_str+"\n")
    return dt


def convert_to_datetime(filepath, t_str):
    dt = None
    try:
        dt = datetime.datetime.strptime(t_str, '%Y/%m/%d %H:%M:%S')
    except ValueError as e:
        sys.stderr.write("[DATE WRONG FORMAT]: "+filepath+"  "+t_str+"\n")
    return dt


def convert_to_int(i_str):
    num = 0
    if len(i_str) != 0:
        try:
            num = int(i_str)
        except ValueError as e:
            sys.stderr.write("[INT WRONG FORMAT]: "+i_str+"\n")
    return num


def convert_to_float(f_str):
    num = 0.0
    if len(f_str) != 0:
        try:
            num = float(f_str)
        except ValueError as e:
            sys.stderr.write("[Float WRONG FORMAT]: "+f_str+"\n")
    return num


def utf2gbk(gb_str):
    utf_str = ""
    try:
        utf_str = gb_str.decode('utf-8').encode('gb18030')
    except UnicodeDecodeError as e:
        sys.stderr.write("[TEXT WRONG CODE]: "+gb_str+"\n")
    return utf_str


def gbk2utf(utf_str):
    gb_str = ""
    try:
        gb_str = utf_str.decode('gb18030').encode('utf-8')
    except UnicodeDecodeError as e:
        sys.stderr.write("[TEXT WRONG CODE]: "+utf_str+"\n")
    return gb_str


def add_dict_list(dict_x, key, value):
    if key in dict_x:
        dict_x[key].append(value)
    else:
        dict_x[key] = [value]


def add_dict_dict(dict_x, key, value):
    if len(value) == 0:
        value = 'null'
    if key not in dict_x:
        dict_x[key] = {value:1}
    else:
        dict_x[key][value] = 1


def display_dict_dict(dict_x):
    for key in dict_x:
        print key,len(dict_x[key])
        sys.stderr.write("%s\t" % key)
        for elem in dict_x[key]:
            sys.stderr.write("%s " % elem)
        sys.stderr.write('\n')
