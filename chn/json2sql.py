"""
created on 11/2/2017
由json转出的files文件夹转为sql
"""
# coding: utf-8
from pipe_sql import *
from analyze import *
import os

rootdir = "files/"
l = []
i = 0
sum_length = 0
for parent, dirname, filenames in os.walk(rootdir):
    for filename in filenames:
        source = read_file('files/' + filename)
        gather = {}
        gather, length = read_source(gather, source, 4)
        sum_length += length
        try:
            write_sql(gather)
            print(i)
            i += 1
        except:
            continue
open("length", 'a').write(str(sum_length))
