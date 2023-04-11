from common import log
from common.explain import explain
from common.cmd import cmd

from common.fs import Fs

from modules.base import BaseModule
from modules.test import Test
from modules.github import Github
from modules.deploy import Deploy

# модуль запуска сценариев автоматизации по шагам

class Scenario(BaseModule):

    # статический метод, который добавляет нужные ниже функциям аргументы к cli режиму в виде kwargs
    @staticmethod
    def _argparse(parser):
        pass


    @staticmethod
    def release_backend(options, config):
        log.info("Starting release backend scenario")
        path = Fs.wd()
        log.info(f'Path is: {path}')

        log.info("Step 1: Repository")
        Github("clone", options, config)
        
        log.info("Step 2: Working dir")
        Fs.cd(config.github.clone_path)
        
        log.info("Step 3: Branch")
        Github("checkout", options, config)

        log.info("Step 4: Branch")
        Github("pull", options, config)

        log.info("Step 5: Tests")
        Test("unit", options, config)

        log.info("Step 6: Deploy")
        Deploy("backend", options, config)

        log.info("Step 7: Teardown")
        Fs.cd_root()
        
