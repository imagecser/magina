from threading import Timer

from flask import current_app

from magina import app, mail
from magina.scrawler import parser, matcher
from magina.scrawler.utils import get_message


class Scheduler:
    def __init__(self, _timer, _function):
        self.func = _function
        self.timer = _timer
        self.task: Timer = None
        self.func()

    def start(self):
        if self.task is None:
            self.task = Timer(self.timer, self._run)
            self.task.start()
        else:
            raise Exception('Task already running')

    def _run(self):
        self.func()
        self.task = Timer(self.timer, self._run)
        self.task.start()

    def stop(self):
        if self.task is not None:
            self.task.cancel()
            self.task = None


times = 0


def func():
    global times
    msgs = parser.get_tuanwei() + parser.get_jiaowu()
    mail_msgs_map = {}
    for msg in msgs:
        emails = matcher.matched_emails(msg['title'])
        for email in emails:
            if mail_msgs_map.get(email) is None:
                mail_msgs_map[email] = [msg]
            else:
                mail_msgs_map[email].append(msg)

    for email, msgs in mail_msgs_map.items():
        message = get_message(msgs, email)
        mail.send(message)

    times += 1
    current_app.logger.info("running %d" % times)


app.app_context().push()
scheduler = Scheduler(current_app.config['SCHEDULER_TIMER'], func)
