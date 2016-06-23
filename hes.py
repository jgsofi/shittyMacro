#!/usr/bin/env python
import javalang
import sys
import re

# Parse java file
try:
    filename = sys.argv[1]
except:
    print('Please pass file to alter as parameter')
file = open(filename).read()
parsed = javalang.parse.parse(file)

# Grab class name
classname = parsed.types[0].name

# Grab all getter names
methods = [m.name for m in parsed.types[0].methods if m.name[:3] == "get"]

# Ask use to select getters
print('Possible getters:')
for i, method in enumerate(methods):
    print('({}) {}'.format(i, method))
print('Enter whitespace separated selections (default: all)')
selected_raw = raw_input()
if selected_raw:
    selected_indexes = map(int, selected_raw.split())
    # Grab desired fields in selected order
    methodset = dict(enumerate(methods))
    selected = [methodset[i] for i in selected_indexes]
else:
    selected = methods

# Build from templates
comparators = "\n            && ".join(
    "Objects.equals({0}(), other.{0}())".format(m) for m in selected)
hashparams = ", ".join("{0}()".format(m) for m in selected)
if len(selected) >= 2:
    hasher = "Objects.hash({})".format(hashparams)
else:
    hasher = "Objects.hashCode({})".format(hashparams)
result = u"""
    @Override
    public boolean equals(Object obj) {{
        if ((this == obj))
            return true;
        if (!(obj instanceof {classname}))
            return false;
        final {classname} other = ({classname})obj;
        return {comparators};
    }}

    @Override
    public int hashCode() {{
        return {hasher};
    }}""".format(comparators=comparators, hasher=hasher, classname=classname)

# Output
print()
print("Placing at end of file:")
line = '=' * 100
print(line + result)
print(line)

# Append to class and write to file
newfile = re.sub(r'\n}', result + u'\n}', file)
open(filename, 'w').write(newfile)
