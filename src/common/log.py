import logging
from inspect import getframeinfo, stack
import subprocess
import os


USE_STYLING = True
DEFAULT_STACK_NUMBER = 2
extra = {}
LAUNCH_DIR = os.getcwd()
max_file_path_length = len(LAUNCH_DIR) + 20 + 26 + 2


class bcolors:
    CYAN = '\033[36m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def caller(stack_number=DEFAULT_STACK_NUMBER):
    caller = getframeinfo(stack()[stack_number][0])
    # print("max_file_path_length: ", max_file_path_length)
    res = f' {caller.filename}:{caller.lineno} '  # "%s:%d" % (caller.filename, caller.lineno)
    # print("res: ", len(res))
    diff = max_file_path_length - len(res)
    if diff > 0:
        res += ' ' * diff
    return res


def get_git_revision_short_hash():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode("utf-8")
    except ValueError:
        return 'no_commit'
    except FileNotFoundError:
        return 'no_git'
    except subprocess.CalledProcessError as e:
        print(e)
        return 'no_git'


class CustomFormatter:

    def __init__(self, logging):
        super()

        CYAN = '\033[36m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

        # best base format for automation systems
        if USE_STYLING:
            FORMAT = (
                '\033[1m[%(levelname)7s]\033[0m\033[4m[%(src)s]\033[0m: %(message)s'
            )
        else:
            FORMAT = (
                '[%(levelname)7s][%(src)s]: %(message)s'
            )

        self.FORMATS = {
            logging.DEBUG: OKBLUE + FORMAT + ENDC,
            logging.EXPLAIN: CYAN + FORMAT + ENDC,
            logging.INFO: FORMAT,
            logging.WARNING: WARNING + FORMAT + ENDC,
            logging.ERROR: FAIL + FORMAT + ENDC,
            logging.CRITICAL: BOLD + FAIL + FORMAT + ENDC + ENDC,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present 

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
       raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
       raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
       raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


# здесь уже начинаем инициализацию логгера

BASE_LOGGING_LEVEL = logging.INFO

EXPLAIN_LEVEL_NUMBER = 9 

addLoggingLevel("EXPLAIN", EXPLAIN_LEVEL_NUMBER, methodName="explain")


qa_automation_logger = logging.getLogger('qa_automation_logger')
qa_automation_logger.setLevel(BASE_LOGGING_LEVEL)
formatter = CustomFormatter(logging)

ch = logging.StreamHandler()
ch.setFormatter(formatter)

qa_automation_logger.addHandler(ch)


def set_log_level(log_level):
    levels = {
        "debug": logging.DEBUG,
        "explain": EXPLAIN_LEVEL_NUMBER,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }
    log_level = log_level.lower()
    if log_level in levels:
        qa_automation_logger.setLevel(levels[log_level])
    else:
        qa_automation_logger.setLevel(BASE_LOGGING_LEVEL)


def info(message, stack_number=0):
    extra['src'] = caller(stack_number=DEFAULT_STACK_NUMBER+stack_number)
    qa_automation_logger.info(message, extra=extra)


def debug(message, stack_number=0):
    extra['src'] = caller(stack_number=DEFAULT_STACK_NUMBER+stack_number)
    qa_automation_logger.debug(message, extra=extra)


def explain(message, stack_number=0):
    extra['src'] = caller(stack_number=3+stack_number)
    set_log_level("explain")
    qa_automation_logger.explain(message, extra=extra)


def warning(message, stack_number=0):
    extra['src'] = caller(stack_number=DEFAULT_STACK_NUMBER+stack_number)
    qa_automation_logger.warning(message, extra=extra)


def error(message, stack_number=0):
    extra['src'] = caller(stack_number=DEFAULT_STACK_NUMBER+stack_number)
    qa_automation_logger.error(message, extra=extra)


def critical(message, stack_number=0):
    extra['src'] = caller(stack_number=DEFAULT_STACK_NUMBER+stack_number)
    qa_automation_logger.critical(message, extra=extra)
