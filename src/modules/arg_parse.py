from modules.github import Github
from modules.deploy import Deploy
from modules.test import Test

from scenario.scenario import Scenario


def add_module_args(parser):
    Github._argparse(parser)
    Deploy._argparse(parser)
    Test._argparse(parser)
    Scenario._argparse(parser)