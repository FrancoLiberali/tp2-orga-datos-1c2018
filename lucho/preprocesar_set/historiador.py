#!/usr/bin/python3

'''
Una función de print un poco más avanzada
'''

import time

def get_ms(epoch_s):
    return ('00' + str(int((epoch_s - int(epoch_s)) * 1000)))[::-1][:3]

def log(*args, **kwargs):
    '''
    print en esteroides.
    Ver documentación de print.
    '''
    
    if kwargs.pop('no_mostrar_hora', False):
        print(*args, **kwargs)
        return

    epoch_s = time.time()

    hora = time.strftime('%H:%M:%S.{}', time.localtime(epoch_s)).format(get_ms(epoch_s))
    sep = ' '
    if not 'sep' in kwargs:
        sep = ''
    
    print('[' + hora + ']' + sep, *args, **kwargs)