"""
created on 2018/3/16
jieba test
"""
# coding: utf-8
import jieba.analyse

sentence = '''
关于邵进同志赴美参加“2018哈佛中国教育论坛”的公示'''
seq = jieba.analyse.extract_tags(sentence)
for i in seq:
    print(i)
