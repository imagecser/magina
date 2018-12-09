"""
合并所有word重复项
:input 未经合并的test表
:output 合并后的数据表outi
"""

# coding: utf-8
import sqlalchemy


def update(i):
    """
    合并两个数据表
    :input outi-1, ini两个表
    :output outi数据表
    """
    i = int(i)
    engine = sqlalchemy.create_engine(
        "mysql+pymysql://root:root@localhost/chn?charset=utf8", echo=True)
    engine.execute(
        "create table in" + str(i) +
        " character set utf8 collate utf8_unicode_ci(select * from test limit "
        + str(i - 1) + "000000, 1000000);")
    engine.execute(
        "create table com" + str(i) +
        "(select word, sum(frequency) as frequency, group_concat(prefix, ',') "
        "as prefix, group_concat(suffix, ',') as suffix, sum(idf) as idf from in"
        + str(i) + " group by word);")
    engine.execute(
        "insert into com" + str(i) +
        "(word, frequency, prefix, suffix, idf) select word, frequency, prefix, suffix, idf from out"
        + str(i - 1) + ";")
    engine.execute(
        "create table out" + str(i) +
        "(select word, sum(frequency) as frequency, group_concat(prefix, ',') as prefix, group_concat(suffix, ',') as suffix, sum(idf) as idf from com"
        + str(i) + " group by word);")
    engine.execute(
        "drop table in" + str(i) + ", com" + str(i) + ", out" + str(i - 1))


def clean(i):
    """
    清除频率为1的词
    """
    i = int(i)
    engine = sqlalchemy.create_engine(
        "mysql+pymysql://root:root@localhost/chn?charset=utf8", echo=True)
    engine.execute("delete from out" + str(i) +
                   " where char_length(word) > 2 and frequency = 1;")


for i in range(22, 51):
    """
    将数据表分段合并，每3次update进行一次clean
    """
    update(i)
    if i % 3 == 0:
        clean(i)
