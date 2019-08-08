import re
import collections

PageSelect = collections.namedtuple('PageSelect', ('id_', 'start', 'end', 'rotate'))

T_ID = 'ID'
T_SHARP = 'SHARP'
T_START = 'START'
T_END = 'END'
T_ROTATE = 'ROTATE'
T_ATTR = 'ATTR'
T_SLICE = 'SLICE'
T_SPLIT = 'SPLIT'
T_EOF = 'EOF'
T_MISMATCH = 'MISMATCH'

_token_spec = (
        (T_SHARP, '#'),
        (T_START, '(?<=#)\d+'),
        (T_SLICE, ':'),
        (T_END, '(?<=:)\d+'),
        (T_ID, '\d+'),
        (T_ROTATE, '(?<==)r-?\d+'),
        (T_ATTR, '='),
        (T_SPLIT, ','),
        (T_EOF, '$'),
        (T_MISMATCH, '.'))

_token_re = '|'.join('(?P<{}>{})'.format(*pair) for pair in _token_spec)

_tokens = (T_ID, T_SHARP, T_START, T_END, T_ROTATE, T_SLICE, T_SPLIT, T_EOF, T_MISMATCH)

_excepted_last_tk = {
        T_ID: (None, T_SPLIT),
        T_SHARP: (T_ID, ),
        T_START: (T_SHARP, ),
        T_END: (T_SLICE, ),
        T_ROTATE: (T_ATTR, ),
        T_SLICE: (T_START, ),
        T_ATTR: (T_START, T_END),
        T_SPLIT: (T_END, T_START, T_ROTATE),
        T_EOF: (T_SPLIT, T_END, T_START, T_ROTATE),
        T_MISMATCH: ()
        }

def _check_token(type, value, last_type):
    if last_type not in _excepted_last_tk[type]:
        raise Exception(
                'unexcepted character(s) {}. Token: {}, last token {}.'
                .format(value, type, last_type))

def get_selects(s):
    selects_list = []

    last_token = None
    curr_slice = [None, None, None, None]
    for t in re.finditer(_token_re, s):
        type = t.lastgroup
        value = t.group()

        _check_token(type, value, last_token)
        if type == 'ID':
            curr_slice[0] = int(value)-1
        elif type == 'START':
            curr_slice[1] = int(value)
        elif type == 'END':
            curr_slice[2] = int(value)
        elif type == 'ROTATE':
            curr_slice[3] = int(value[1:])
        elif type in ('SPLIT', 'EOF'):
            selects_list.append(PageSelect(*curr_slice))
            curr_slice = [None, None, None, None]

        last_token = type
    return selects_list

if __name__ == '__main__':
    s = '1#2:3=r-90,4#5:6=r45'
    print(get_selects(s))
