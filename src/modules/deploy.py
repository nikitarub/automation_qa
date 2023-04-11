from common import log
from common.explain import explain
from common.cmd import cmd
from common.fs import Fs
from common.versioning import update_version

from modules.base import BaseModule

# модуль работы с выкаткой

class Deploy(BaseModule):

    # статический метод, который добавляет нужные ниже функциям аргументы к cli режиму в виде kwargs
    @staticmethod
    def _argparse(parser):
        parser.add_argument('--version', dest='version', action='store',
                            default="patch",
                            help='Updated version of the deployment')


    @staticmethod
    def backend(options, config):
        log.info("Rolling out backend")
        path = Fs.wd()
        log.info(f'Path is: {path}')
        log.info(f"Updating version to {options['version']}")
        update_version(options['version'], config.version_file)
        
