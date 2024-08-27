import argparse
from re import match, search
from os.path import exists
from os import rename, remove

parser = argparse.ArgumentParser(description="C/C++ header file auto create tool")
parser.add_argument("codefile", type=str, help="Abs/rel path to source code file")
file = parser.parse_args().codefile

assert exists(file), "Non-existing file"
assert (file.endswith(".c") or file.endswith(".cpp")), "File must be C/C++ source code file"

prototype_template = r"\w+ \*?\w+\([ ?\*?\w+ |,]*\)"
include_template = r'#include [<|"]..\w+\.h[>|"]'
prototypes = []
includes = []

with open(file, 'r') as code:
    for line in code:
        if(match(prototype_template, line) != None and not "main" in line):
            prototypes.append(search(prototype_template, line).group(0))
        if(match(include_template, line) != None):
            includes.append(line)

with open(file[:file.find('.c')] + ".h", 'w') as Hfile:
    print(f"{''.join(includes)}\n{";\n".join(prototypes)};", file=Hfile)

rename(file, file + ".old")
with open(file + ".old", 'r') as old, open(file, 'w') as new:
    new.write(f'#include ".{file[file.rfind('/'):file.find('.c')]}.h"\n')
    for line in old:
        new.write(line if (match(include_template, line) == None) else "")

remove(file + ".old")
        