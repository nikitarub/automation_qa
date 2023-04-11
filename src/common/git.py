from common import fs
from common import log
from common.cmd import cmd
from common.explain import explain
# общий модуль работы с git


class Git():
    @staticmethod
    def clone(url, clone_path):
        log.info(f"Clonning {url} to path: {clone_path}")
        explain()(cmd)(f"git clone {url} {clone_path}")


    @staticmethod
    def checkout(branch):
        log.info(f"Checkout {branch}")
        explain()(cmd)(f"git checkout {branch}")
    

    @staticmethod
    def pull():
        log.info("Pulling git repository")
        explain()(cmd)(f"git pull")

