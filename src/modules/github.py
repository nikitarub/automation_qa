from common import log
from common.explain import explain
from common.cmd import cmd
from common.fs import Fs
from common.git import Git

from modules.base import BaseModule

# модуль работы с гитхабом

class Github(BaseModule):

    # статический метод, который добавляет нужные ниже функциям аргументы к cli режиму в виде kwargs
    @staticmethod
    def _argparse(parser):
        parser.add_argument('--branch', dest='branch', action='store',
                            default='main',
                            help='Git branch to be used in git commands')


    @staticmethod
    def clone(options, config):
        url = f'https://{ config.github.pat_token }@github.com/{config.github.github_url_path}'
        clone_path = config.github.clone_path
        log.info(f"Cloning repository of {url} to {clone_path}")
        if Fs.exists(clone_path):
            log.info(f'Clone path `{clone_path}` already exists')
        else:
            Git.clone(url, clone_path)


    @staticmethod
    def checkout(options, config):
        if not "branch" in options:
            log.error("Branch must be specified")
            raise RuntimeError("Specify git branch to checkout")
        log.info(f"Checking out branch `{options['branch']}`")
        Git.checkout(options['branch'])


    @staticmethod
    def pull(options, config):
        log.info(f"Pulling repo")
        Git.pull()
