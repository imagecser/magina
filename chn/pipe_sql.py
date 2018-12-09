#! python3
# coding: utf-8
"""
created on 10/23/2017

read & write sql

"""
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import time
import pandas as pd

PARAS = {
    "table": "test"
}


def write_sql(maps):
    """
    将统计字典写入mysql
    存入数据结构的表结构：
    +-----------+--------+-----------+----------+----------+
    |   index   |  word  | frequency |  prefix  |  suffix  |
    +-----------+--------+-----------+----------+----------+
    :paras maps: 待写入统计集合
    """
    engine = sqlalchemy.create_engine(
        "mysql+pymysql://root:root@localhost/chn?charset=utf8", echo=False)
    engine.execute("create TABLE if not exists " + PARAS['table'] + "( \
                    id bigint AUTO_INCREMENT primary key, \
                    word text not null, \
                    frequency bigint not null, \
                    prefix text not null, \
                    suffix text not null, \
                    idf int not null) character set utf8; \
                   ")
    # engine.execute("TRUNCATE TABLE " + PARAS['table'] + ";")
    result_word = [item[0] for item in maps.items()]
    result_frequency = [value[0] for key, value in maps.items()]
    result_prefix = [','.join(value[4]) for key, value in maps.items()]
    result_suffix = [','.join(value[5]) for key, value in maps.items()]
    result_idf = [1] * len(maps)
    dataframe = pd.DataFrame({'word': result_word, 'frequency': result_frequency,
                              'prefix': result_prefix, 'suffix': result_suffix, 'idf': result_idf})
    dataframe.to_sql(PARAS['table'], engine, if_exists='append', index=False)


def read_sql():
    """
    从mysql读入未分析的统计字典
    :returns: 读入的统计字典
    """
    engine = sqlalchemy.create_engine(
        "mysql+pymysql://root:root@localhost/chn?charset=utf8", echo=True)
    dataframe = pd.read_sql(
        "SELECT word, frequency, prefix, suffix FROM " + PARAS['table'], engine)
    maps = {}
    for item in dataframe.itertuples():
        maps[item[1]] = [item[2], 0, 1, 0,
                         list(filter(lambda x: x, item[3].split(','))), list(filter(lambda x: x, item[4].split(',')))]
    return maps


def run():
    """
    template
    """
    GATHER = {}
    SOURCE = analyze.read_file(analyze.PARAS["source_file"])
    GATHER = analyze.read_source(GATHER, SOURCE, 4)
    write_sql(GATHER)


def combine_sql():
    """
    将数据库中的相同词语项合并
    """
    engine = sqlalchemy.create_engine(
        "mysql+pymysql://root:root@localhost/chn?charset=utf8", echo=True)
    engine.execute("drop table if exists output;")
    engine.execute("create table output(select word, sum(frequency) as frequency, group_concat(prefix, ',') as prefix, group_concat(suffix, ',') as suffix from test group by word);")
