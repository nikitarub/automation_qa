from common import log
from common.explain import explain

# базовый модуль в котором прописываем инициализацию
# она же явлется модулем для запуска функций

class BaseModule():
    # статический метод, который добавляет нужные ниже функциям аргументы к cli режиму в виде kwargs
    @staticmethod
    def _argparse(parser):
        pass


    def __init__(self, function_name, options, config):
        # инииализация в данном случае выступает как переключатель комманд – единая точка входа в этот модуль
        avaliable_functions = [f for f in dir(self) if not f.startswith('_')]
        if not "_argparse" in dir(self):
            log.warning(F"Module {self.__class__} does not have arg_parse init func", stack_number=1)
        if function_name not in avaliable_functions:
            log.error(f"Unknown function {function_name}. Use one of {avaliable_functions}")
            raise RuntimeError(f"Unknown function {function_name}")
        function_to_run = getattr(self, function_name)
        log.debug(f"Running `{function_name}` function")
        function_to_run(options, config)
