def combine(parameter):
    if 'main' not in parameter.keys():
        return '{{ main }}'
    command = parameter['main']
    parameter.pop('main')
    repeat = {}
    i = 0
    while i < len(command):
        line = ''
        count = 0
        space_start = i
        while i < len(command):
            if command[i] == '{':
                count += 1
            else:
                if command[i] == ' ' or command[i] == '\t':
                    if(count != 0):
                        space_start = i
                    else:
                        line += command[i]
                else:
                    line = ''
                    space_start = i + 1
                
                count = 0
            i += 1      
            if count == 2:
                start = i
                break
        count = 0
        while i < len(command):
            if command[i] == '}':
                count += 1
            else:
                count = 0
            i += 1                
            if count == 2:
                current = command[start:i-2].strip()
                if not current in repeat.keys():
                    repeat[current] = 0
                else:
                    repeat[current] += 1 if repeat[current]+1 < len(parameter[current]) else 0
                if current in parameter.keys():
                    value = parameter[current][repeat[current]] if isinstance(parameter[current], list) and repeat.get(current) else parameter[current]
                    if(isinstance(value, list)):
                        value = value[0]
                    if len(value) > 0:
                        endn = value[-1] == '\n'
                        value = value.split('\n')
                        if value[-1] == '':
                            value = value[:-1]
                        if len(value) > 1:
                            tv = ''
                            for v in value:
                                tv += line + v + '\n'
                            if not endn:
                                tv = tv[:-1]
                        else:
                            tv = line + value[0] + ('\n' if endn else '')
                    else:
                        tv = ''
                    command = command[:space_start] + tv + command[i:]
                    i = space_start
                else:
                    command = command[:start] + ' ' + current + ' }}' + command[i:]
                break
    return command

from code_tokenizer import color_by_char_type

def show(object):
    print(color_by_char_type(combine(object)))