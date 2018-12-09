# -*- coding: utf-8 -*-

from pyhanlp import *

from magina import app
from magina.models import Keyword


def hanlp_parse(sentence, keywords):
    """
    hanlp test
    """

    if not isThreadAttachedToJVM():
        attachThreadToJVM()

    id_scorer = JClass('com.hankcs.hanlp.suggest.scorer.lexeme.IdVectorScorer')()
    id_scorer.addSentence(sentence)
    scores = {}

    for keyword in keywords:
        # res_score = id_scorer.computeScore(keyword)
        res_score = id_scorer.computeScore(keyword.word)
        value = float(str(res_score.get(sentence)) if str(res_score.get(sentence)) != 'None' else 0)
        # if keyword in sentence:
        if keyword.word in sentence:
            value = 10.0
        scores[keyword] = value
    return [item[0] for item in scores.items() if item[1] > 0.5]


if __name__ == '__main__':
    print(hanlp_parse('什么', ['']))


def matched_emails(topic: str) -> list:
    emails = []
    keywords = [item for item in Keyword.query.all()]
    for keyword in hanlp_parse(topic, keywords):
        emails += [user.email for user in keyword.users]
    # for keyword in keywords:
    #     if is_keyword_match(topic, keyword.word):
    #         emails += [user.email for user in keyword.users]
    return emails
