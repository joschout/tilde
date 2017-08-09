#!/usr/bin/python
import sys
import re
empty_line_pattern = re.compile(r'\s*$')
begin_model_pattern = re.compile(r'begin\(model\((\w+)\)\)')
end_model_pattern = re.compile(r'end\(model\((\w+)\)\)')

start_models_predicate_pattern = re.compile(r'(\w+)\(')


def is_empty_line(line:str)->bool:
    return empty_line_pattern.match(line)


# remember: sys.argv[0] is the name of the script
with open(sys.argv[1]) as f:
    for line in f:
        # remove last char of line
        line = line[:-1]
        if not is_empty_line(line):
            m = begin_model_pattern.match(line)
            if m:
                key = m.group(1)
        elif end_model_pattern.match(line):
            print("\n")
        else:
            m = start_models_predicate_pattern.match(line)
            if m:
                keys_line = re.sub(m.group(1) + '\(', m.group(1) + '\(' + key + ',', line)
                print(keys_line)
            else:
                #TODO: vul aan
                pass
                