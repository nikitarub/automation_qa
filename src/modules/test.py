from common import log
from common.explain import explain
from common.cmd import cmd

from common.fs import Fs

from modules.base import BaseModule

# модуль запуска тестов

class Test(BaseModule):

    # статический метод, который добавляет нужные ниже функциям аргументы к cli режиму в виде kwargs
    @staticmethod
    def _argparse(parser):
        pass


    @staticmethod
    def unit(options, config):
        path = Fs.wd()
        log.info(f'Path is: {path}')
        # Fs.cd("./workon_target")
        # path = Fs.wd()
        # log.info(f'Path is: {path}')
        log.info("Running unit tests")

