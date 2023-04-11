import subprocess
from common.explain import explain
from common import log

# запуск bash команд

def cmd(bash_command, check=True, text=True):
    # log.info(f"Running bash {bash_command}")
    result = explain(f"Running bash `{bash_command}` \t| with check={check}, text={text}",
                      what_to_return = ""
                     )(subprocess.run)(bash_command.split(' '), check=check, text=text)
    return result
