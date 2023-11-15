import os

from common import log
from common.explain import explain
# нужен модуль работы с файловой системой

LAUNCH_DIR = os.getcwd()

class Fs():

    @staticmethod
    def cd(path):
        # проверка на существование пути
        log.info(f"Changing path to: {path}")
        if not explain(what_to_return=True)(os.path.isdir)(path):
            log.error(f"Such path: {path} does not exist")
            raise FileNotFoundError(path)
        # переход в папку
        explain(what_to_return=path)(os.chdir)(path)
    

    @staticmethod
    def cd_root():
        Fs.cd(LAUNCH_DIR)
        
    

    @staticmethod
    def wd():
        return explain("Asking for current path", what_to_return=LAUNCH_DIR)(os.getcwd)()
    

    @staticmethod
    def exists(path):
        return explain(f"Checking if {path} exists", what_to_return=False)(os.path.exists)(path)