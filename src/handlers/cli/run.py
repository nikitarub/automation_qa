from common.explain import explain
from common import log

from modules.github import Github
from modules.deploy import Deploy
from modules.test import Test

from scenario.scenario import Scenario

from configs.config_switcher import config_switch

def stub():
    log.info("Stub")

# switcher команд
def run_cli(command, options):
    # parse command
    if len(command) < 3:
        log.error("Not full command")
        raise RuntimeError("not enough command arguments")

    project_name = command[0]
    module_name = command[1].lower()
    function_name = command[2]

    config = config_switch(project_name)

    if module_name == "github":
        Github(function_name, options, config)
    elif module_name == "deploy":
        Deploy(function_name, options, config)
    elif module_name == "test":
        Test(function_name, options, config)
    elif module_name == "scenario":
        Scenario(function_name, options, config)
    
    # log.info(f'_______command: {command}')
    # explain('will run stub')(stub)()
    
    return 