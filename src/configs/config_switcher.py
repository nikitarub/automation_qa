from configs.target import TargetProject
from configs.stub import StubProject

# переклюючатель конфигов

def config_switch(project_name):
    if project_name == "target":
        return TargetProject()
    if project_name == "stub":
        return StubProject()
