# режим работы команд и чего либо в explain
import logging
from common import log


"""
декоратор explain:
если включен режим эксплейн, то не запускает функцию, а логирует действие и возвращает заглушку 
"""


EXPLAIN_MODE = False


def set_explain_mode(explain_flag):
    log.info(f"Setting explain mode to {explain_flag}")
    global EXPLAIN_MODE
    if explain_flag:
        EXPLAIN_MODE = True
        log.qa_automation_logger.setLevel(logging.DEBUG)


def explain(explain_message=None, what_to_return=None):
    def wrap(func):
        def inner(*args, **kwargs):
            if EXPLAIN_MODE:
                
                if explain_message and type(explain_message) == str:
                    message_to_explain = ""
                    message_to_explain += f"{explain_message}"
                    if len(args):
                        message_to_explain += f" | with args: {args}"
                    if len(kwargs):
                        message_to_explain += f" | with kwargs: {kwargs}"
                    log.explain(message_to_explain)
                else:
                    message_to_explain = ""
                    message_to_explain += f"{func.__name__}"
                    if len(args):
                        message_to_explain += f" | with args: {args}"
                    if len(kwargs):
                        message_to_explain += f" | with kwargs: {kwargs}"
                    log.explain(message_to_explain)
                return what_to_return
            return func(*args, **kwargs)
        return inner
    if (type(explain_message) == str) or (explain_message is None):
        return wrap
    else:
        return wrap(explain_message)
