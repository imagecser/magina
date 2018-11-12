# -*- coding: utf-8 -*-

from magina.scrawler.utils import *
from magina.models import User, Keyword
from magina import app


def is_keyword_match(topic: str, keyword: str) -> bool:
    return True
    # for word in keyword:
    #     if word not in topic:
    #         return False
    # return True


def matched_emails(topic: str) -> list:
    app.app_context().push()
    emails = []
    keywords = [item for item in Keyword.query.all()]
    for keyword in keywords:
        if is_keyword_match(topic, keyword.word):
            emails += [user.email for user in keyword.users]
    return emails
