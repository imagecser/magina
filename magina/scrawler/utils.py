# coding=utf-8
"""The module used to send mail."""

import random
import re
import string
import time

import requests
from flask import current_app
from flask_mail import Message

from magina import mail


# def __get_connection():
#     return pymysql.connect(host='localhost',
#                            user='root',
#                            passwd='root',
#                            db='magina',
#                            charset='utf8')


# except Exception as e:
# logging.warning('mysql获取%s已获得类型%d通知失败\n'%(tablename, url_class))

# def sql_insert_table(tablename, data):
#     """The new url will get entered into the table library.
#     Where tablename is the table name and data
#     (Form:(id,title,url,class).Defaults:id=0,class=1.)
#     is the list of data to be stored.
#     """
#     # try:
#     conn = __get_connection()
#     cursor = conn.cursor()
#     cursor.executemany('insert into %s values' % tablename + '(%s,%s,%s,%s)', data)
#     conn.commit()
#     cursor.close()
#     conn.close()


def re_findall(text, website_source):
    """
    Text is a regular expression.
    Website is the site to match.
    The return value is a list of tuple,
    the first array in the two-dimensional array is the newly obtained url,
    and the second array is the title.
    """
    pattern = re.compile(text)
    my_page = website_source
    my_match = pattern.findall(my_page, re.S)
    return my_match


def get_page(website):
    """Get the web page source code."""
    connection_status = 'ok'
    pages = ""

    # noinspection PyBroadException
    try:
        pages = requests.get(website, timeout=5).text
    except Exception:
        connection_status = 'wrong'
        current_app.logger.warning('connection error:cannot connect to %s!' % website)
        localtime = time.asctime(time.localtime(time.time()))
        print(connection_status + ' ' + website)
        print('time: ' + localtime)

    return [pages, connection_status]


def get_message(messages, rec):
    return Message(
        subject='南大通知: %s 等%s' % (messages[0]['title'], ''.join(random.sample(string.ascii_letters, k=4))),
        html="""<html><body>
        您好, 您关注的南京大学通知信息更新了!
        %s
        <br><p>若有任何想法或建议，请联系我们:zhi.suun@gmail.com ^_^</p>
        </body></html>""" % (
            ''.join(['<p><a href="%s">%s</a></p>' % (item['url'], item['title']) for item in messages])),
        recipients=[rec]
    )


def send_update_mail(to_list, website, description, url, title):
    """
    to_list is the mail list.
    url is the url of the website.
    title is title.
    """
    message = Message(
        subject='%s更新: %s' % (website, title),
        html="""<html><head></head><body>
        <p>%s<br><a href="%s">%s</a><br></p>
        <p>--来自Nova.Studio,若有任何想法或建议，请联系我们:sme@nju.edu.cn ^_^</p>
        </body></html>""" % (
            description, url, title),
        recipients=to_list
    )
    # noinspection PyBroadException
    try:
        mail.send(message)
    except Exception:
        current_app.logger.warning('Send mail failed.')
