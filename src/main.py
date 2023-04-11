import argparse
from common import log
from common.explain import set_explain_mode
from modules.arg_parse import add_module_args
from handlers.cli.run import run_cli
from handlers.github_webhook.run import run_webhook
import asyncio


# обработка режимов запуска инструмента автоматизации
"""
# 2 режима – 2 обработчика (handlers):

1. CLI – запуск отдельно стоящих команд
2. webhook handler – реагирование на webhook при действии в репозитории 
"""


parser = argparse.ArgumentParser(description='Automation tool')

parser.add_argument('-m', dest='mode', action='store',
                    default="cli",
                    help='mode for automation: cli, webhook')
parser.add_argument('--explain', dest='explain', action='store_true',
                    default=False,
                    help='flag to explain the command')
parser.add_argument('command', nargs='*')

add_module_args(parser)



args = parser.parse_args()

set_explain_mode(args.explain)
options = vars(args).copy()
del options['mode']
del options['command']
del options['explain']


# запуск нужного режима
if args.mode == "cli":
    log.info("starting cli")
    run_cli(args.command, options)
elif args.mode == "webhook":
    log.info("starting webhook")
    if __name__ == "__main__":
        asyncio.run(run_webhook())
else:
    log.error(f"ERROR: mode '{args.mode}' is unsupported, choose any of: webhook, cli")


# from configs.target import TargetRepo

# target_repo = TargetRepo()

# print(target_repo)
# log.explain("er")

# print(target_repo.project_name)
# print(target_repo.github)
# print(target_repo.telegram)
