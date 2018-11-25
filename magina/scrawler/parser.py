# coding=utf-8
"""Part of Tuanwei."""

from magina import app
from magina.models import TuanweiInfo, db, JiaowuInfo
from magina.scrawler.utils import *


def get_tuanwei():
    """
    main part of module tuanwei.
    """
    tuanwei_error_warning = 0
    messages = []
    website_tuanwei = "https://tuanwei.nju.edu.cn/component/tags/tag/21"
    crawler_tuanwei = get_page(website_tuanwei)
    text_re = "<h3>\n\t\t\t\t\t<a href=\"/article/(.*)\">\n\t\t\t\t\t\t(.*)\t\t\t\t\t</a>\n\t\t\t\t</h3>"

    if crawler_tuanwei[1] is 'wrong':
        current_app.logger.warning('error: cant connect to tuanwei.')
        tuanwei_error_warning += 1
        send_update_mail(current_app.config['MAIL_USERNAME'],
                         '团委',
                         'tuanwei connection error!',
                         '',
                         'error')

    else:
        # mail_list = User.get_all_email()
        match_list = re_findall(text_re, crawler_tuanwei[0])
        # match_list是通过正则表达式筛选网页源代码后的到的url和title组成的元组组成的列表

        latest_url = []
        title = []
        length = len(match_list)
        for length_1 in range(0, length):
            latest_url.append('https://tuanwei.nju.edu.cn/article/%s' % match_list[length_1][0])
            title.append(match_list[length_1][1])
        # 从match_list中分离出url和title

        url_before = TuanweiInfo.query.filter_by(class_=1).with_entities(TuanweiInfo.url).all()
        url_before = [item[0] for item in url_before]
        num = 0
        for url in latest_url:
            if url not in url_before:
                num += 1
                index_of_url = latest_url.index(url)
                website_url = latest_url[index_of_url]
                messages.append({
                    'url': website_url,
                    'title': title[index_of_url]
                })
                # data = [(0, title[index_of_url], latest_url[index_of_url], 1)]
                # sql_insert_table('tuanwei_info', data)
                info_insert = TuanweiInfo(title=title[index_of_url], url=latest_url[index_of_url], class_=1)
                db.session.add(info_insert)
                db.session.commit()

        # 对比新获得的url和已有的

        if num is 0:
            current_app.logger.info('Youth League not updated')
        else:
            current_app.logger.info('Youth League updated %s notifications' % str(num))
    return messages


def get_jiaowu():
    """
    main part of module jiaowu.
    """
    jiaowu_error_warning = 0
    messages = []
    website_jiaowu = "http://jw.nju.edu.cn/allContentList.aspx?MType=PX-WZSY-ZXTZ"
    crawler_jiaowu = get_page(website_jiaowu)
    text_re_top = "<a href='(.*?)'><span class='top'>.*?</span>(.*?)</a>"
    text_re_not_top = "<a href='(.*?)'>(.*?)</a><span class='time_l'>"

    if crawler_jiaowu[1] is 'wrong':
        current_app.logger.warning('error: cant connect to jiaowu.')
        jiaowu_error_warning += 1
        send_update_mail(current_app.config['MAIL_USERNAME'],
                         '教务',
                         'jiaowu connection error!',
                         '',
                         'error')

    else:
        # 第一部分
        # mail_list = sql_get_mail_address_list()
        # mail_list = User.get_all_email()
        match_list_top = re_findall(text_re_top, crawler_jiaowu[0])
        match_list_not_top = re_findall(text_re_not_top, crawler_jiaowu[0])
        # match_list是通过正则表达式筛选网页源代码后的到的url和title组成的元组组成的列表

        # 第二部分：获取置顶通知
        latest_url_top = []
        title_top = []
        length = len(match_list_top)
        for length_variable in range(0, length):
            latest_url_top.append('http://jw.nju.edu.cn/%s' % match_list_top[length_variable][0])
            title_top.append(match_list_top[length_variable][1])
        # 从match_list中分离出url和title

        url_before_top = JiaowuInfo.query.filter_by(class_=1).with_entities(JiaowuInfo.url).all()
        url_before_top = [item[0] for item in url_before_top]
        num_top = 0
        for url in latest_url_top:
            if url not in url_before_top:
                num_top += 1
                index_of_url = latest_url_top.index(url)
                web_url = latest_url_top[index_of_url]
                messages.append({
                    'url': web_url,
                    'title': title_top[index_of_url]
                })
                # data_top = [(0, title_top[index_of_url],
                #              latest_url_top[index_of_url], 1)]
                # sql_insert_table('jiaowu_info', data_top)
                info_insert = JiaowuInfo(title=title_top[index_of_url], url=latest_url_top[index_of_url], class_=1)
                db.session.add(info_insert)
                db.session.commit()
        # 对比新获得的url和已有的

        # 第三部分：获取非置顶通知
        latest_url_not_top = []
        title_not_top = []
        top_feature = '''<span class='top'>'''
        i = 0
        while i < len(match_list_not_top):
            if top_feature in match_list_not_top[i][1]:
                del match_list_not_top[i]
            else:
                i += 1
        length = len(match_list_not_top)
        for length_variable in range(0, length):
            latest_url_not_top.append('http://jw.nju.edu.cn/ContentList.aspx?mtype=PX-WZSY-ZXTZ&FType=WZSY&%s' %
                                      match_list_not_top[length_variable][0])
            title_not_top.append(match_list_not_top[length_variable][1])
        # 从match_list中分离出url和title

        url_before_not_top = JiaowuInfo.query.filter_by(class_=0).with_entities(JiaowuInfo.url).all()
        url_before_not_top = [item[0] for item in url_before_not_top]
        num_not_top = 0
        for url in latest_url_not_top:
            if url not in url_before_not_top:
                num_not_top += 1
                index_of_url = latest_url_not_top.index(url)
                web_url = latest_url_not_top[index_of_url]
                messages.append({
                    'url': web_url,
                    'title': title_not_top[index_of_url]
                })
                # data_not_top = [(0, title_not_top[index_of_url],
                #                  latest_url_not_top[index_of_url], 0)]
                # sql_insert_table('jiaowu_info', data_not_top)
                info_insert = JiaowuInfo(title=title_not_top[index_of_url],
                                         url=latest_url_not_top[index_of_url], class_=0)
                db.session.add(info_insert)
                db.session.commit()
        # 对比新获得的url和已有的

        if num_top + num_not_top is 0:
            current_app.logger.info('Academic Affairs not updated')
        else:
            current_app.logger.info('Academic Affairs updated %s notifications' % str(num_top + num_not_top))
    return messages
