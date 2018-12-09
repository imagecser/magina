"""
created on 10/19/2017

based on ../chn/main.cpp

"""
# !/usr/bin/env python3
# coding: utf-8
import math
import time
import collections
import pipe_sql

PARAS = {
    "source_file": "sc.txt",
    "output_file": "sc.output",
    "input": "南京大学坐落于钟灵毓秀、虎踞龙蟠的金陵古都",
    "max_word_length": 4
}


def is_chinese(uchar):
    """判断一个 unicode 是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def remove_symbol(source):
    """
    remove invalid character
    :para source: 源文件内容
    :returns: 格式化后的源文件内容
    """
    dest = ""
    removed_character = "“‘”【】『』'\"[]{}"
    for char in source:
        if char in removed_character:
            char = ''
        elif not is_chinese(char):
            char = ' '
        dest += char
    return dest


def read_file(file_name):
    """
    read in file and formatted
    :para file_name: 源文件名
    :returns: 格式化后的文本
    """
    # print("loading source file...")
    with open(file_name, 'r') as file_handler:
        return remove_symbol(file_handler.read())


def read_sentence(sentence, maps, max_word_length):
    """
    录入内容
    :para sentence: 单句
    :para max_word_length: 最大识别字符长度
    :returns: 词典，字串数据
    maps: {"字串": [频数, 频率, 凝聚程度, 自由程度, 前一字符, 后一字符], ...}
    """
    length = len(sentence)
    for start in range(length):
        for len_word in range(1, max_word_length + 1):
            if start + len_word < length + 1:
                word = sentence[start:start + len_word]
                if word in maps:
                    maps[word][0] += 1
                    if start > 0:
                        maps[word][4].append(sentence[start - 1])
                    if start + len_word < length:
                        maps[word][5].append(sentence[start + len_word])
                else:
                    maps[word] = [
                        1, 0, 1, 0,
                        [sentence[start - 1]] if start > 0 else [],
                        [sentence[start + len_word]] if start +
                                                        len_word < length else []
                    ]
    return maps


def read_source(maps, source, max_word_length=2):
    """
    被空格分割的格式化的源文件，生成统计字典
    :para source: 被空格分割的格式化过的源文件
    :returns: 源文件生成的统计过频数的集合
    """
    # print("loading file content...")
    setup = time.time()
    sentence_list = source.split()
    for sentence in sentence_list:
        read_sentence(sentence, maps, max_word_length)
    # print("time: %.4fs" % (time.time() - setup))
    return maps, len(source)


def calc_freq(maps, length):
    """
    计算统计字典的词频
    :para maps: 统计字典
    :para length: 源文件总长度
    :returns: 计算出词频的统计字典
    """
    print("calculating word frequences...")
    for key in maps.keys():
        maps[key][1] = float(maps[key][0]) / length


def calc_condensation_degree(maps):
    """
    计算统计字典的凝聚程度
    :para maps: 统计字典
    :returns: 计算出凝聚程度的统计字典
    """
    print("calculating condensation degrees...")
    for key in maps.keys():
        length_word = len(key)
        if length_word > 1:
            ''' degs = []
            for index in range(1, length_word):
                div = 10000 * (maps[key[:index]][1] * maps[key[index:]][1])
                result = maps[key][1] / div
                degs.append(result)
            maps[key][2] = min(degs)'''
            front_deg = maps[key][1] / \
                        (maps[key[:1]][1] * maps[key[1:]][1] * 10000)
            back_deg = maps[key][1] / \
                       (maps[key[:-1]][1] * maps[key[-1:]][1] * 10000)
            maps[key][2] = min([front_deg, back_deg])


def calc_freedom_degree(maps):
    """
    计算统计字典的自由程度
    :para maps: 统计字典
    :returns: 计算出自由程度的统计字典
    """  # calc_freq(GATHER, LENGTH)
    # calc_condensation_degree(GATHER)
    # calc_freedom_degree(GATHER)
    print("calculating freedom degrees...")
    for key in maps.keys():
        degs = []
        for index in range(4, 6):
            deg = 0
            freq_counter = collections.Counter(maps[key][index])
            data_length = len(maps[key][index])
            for value in freq_counter.values():
                freq = float(value) / data_length
                deg -= math.log(freq) * freq
            # print(key, freq_counter, deg)
            degs.append(deg)
        maps[key][3] = min(degs)

    # for key, value in maps.items():
    #     print(key + str(value))
    return maps


def adjust_ratio(maps):
    sum_free = 0
    sum_cond = 0
    for value in maps.values():
        sum_cond += value[2]
        sum_free += value[3]
    ratio = sum_free / sum_cond
    for value in maps.values():
        value[2] *= ratio


def filter_map(maps):
    """
    输出指定筛选结果
    :para maps:统计字典
    """
    result = {}
    print("filtering special condition...")
    for key, value in maps.items():
        if len(key) > 1:
            result[key] = value
    del (maps)
    ordered = {}
    for key, value in result.items():
        ordered[key] = [value[1], value[2] * value[3]]
        # print(key + ": %.8f, %.2f, %.2f" % (value[1], value[2], value[3]))
    res = sorted(ordered.items(), key=lambda x: -x[1][1])
    del (ordered)
    words = []
    for item in res:
        words.append(item[0])
    # print(words)
    # print(words)
    # return words
    ret = []
    for item in res:
        ret.append(str(item[0]) + str(item[1]))
    return ret, words
    # ordered = [0]
    # for key, value in maps.items():
    #     ordered.append(value[3])
    # ordered = sorted(ordered)max_len_word
    # for item in ordered:
    #    print(item)


def write_output(iter, file_name):
    """
    将筛选结果输出到指定文件
    :para iter: 筛选结果迭代器
    :para file_name: 输出文件名
    """
    with open(file_name, "w") as f:
        for item in iter:
            f.write(item + '\n')
    f.close()


def get_result(input, words):
    for word in words:
        rep = [ch for ch in word]
        rep = ' ' + '.'.join(rep) + ' '
        if input.count(word) > 0:
            input = input.replace(word, rep)
            print(input)
    input = input.replace('.', '').replace('  ', ' ')
    print(input)


def run():
    """
    template
    """
    # SOURCE = read_file(PARAS["source_file"])
    # GATHER = {}
    # GATHER, LENGTH = read_source(GATHER, SOURCE, PARAS["max_word_length"])
    # LENGTH = len(SOURCE) - SOURCE.count(' ')
    # calc_freq(GATHER, LENGTH)
    # calc_condensation_degree(GATHER)
    # calc_freedom_degree(GATHER)
    # OUTPUT_ITER = filter_map(GATHER)
    # write_output(OUTPUT_ITER, PARAS["output_file"])
    GATHER = pipe_sql.read_sql()
    LENGTH = 1000000
    calc_freq(GATHER, LENGTH)
    calc_condensation_degree(GATHER)
    calc_freedom_degree(GATHER)
    # pipe_sql.write_sql(GATHER)
    adjust_ratio(GATHER)
    OUTPUT_ITER, WORDS = filter_map(GATHER)
    write_output(OUTPUT_ITER, PARAS['output_file'])
    # WORDS = filter_map(GATHER)
    # get_result(PARAS['input'], WORDS)
    # write_output(OUTPUT_ITER, PARAS['output_file'])
    # for key, value in gather.items():
    #     print(key, value)
