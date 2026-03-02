from random import choices
from sys import modules

SIMPLE = list(range(0x41, 0x5a)) + list(range(0x61, 0x7a))
SIMPLE_LEN = 8
COMPLEX = list(range(0x41, 0x7e))
COMPLEX_LEN = 12


def gen(passType = 'simple'):
    ''' генерация пароля'''
    if passType not in ['simple', 'complex']:
        raise ValueError('Неправильно указан тип пароля')
    passType = passType.upper()

    s = getattr(modules[__name__], passType)
    l = getattr(modules[__name__], passType + '_LEN')
    return ''.join([chr(c) for c in choices(s, k=l)])

