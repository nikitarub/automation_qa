from common import log
from common.explain import explain, set_explain_mode

"""
# смотрим как работает explain
"""

set_explain_mode(True)

log.info("SOMETHING")

print("\n\n\n\n\n\n\n")

@explain(what_to_return=1)
def some_func(a):
    print("sooooome: ", a)
    return 1

print("11:____ ", some_func('1'))

print("\n\n\n")

@explain("lllllllll", what_to_return=1)
def some_func_2(a):
    print("sooooome: ", a)
    return 1

print("22:____ ", some_func_2('4'))


def some_func_3(a):
    print("sooooome: ", a)
    return 1

smth = explain('explainingggg', what_to_return=1)(some_func_3)(a='888')

print("33:____ ", smth)


smth_2 = some_func_3('888')
print(smth_2)
