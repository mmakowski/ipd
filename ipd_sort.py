import ipd, sys


def merge(lines1, lines2):
    if lines1 == None: return lines2
    if lines2 == None: return lines1
    result = []
    while len(lines1) > 0 and len(lines2) > 0:
        line1 = lines1.pop(0)
        line2 = lines2.pop(0)
        if line1 > line2: 
            result.append(line2)
            result.append(line1)
        else:
            result.append(line1)
            result.append(line2)
    result = result + lines1
    result = result + lines2
    return result


def sort(lines):
    if lines == None or len(lines) == 0: return lines
    l = len(lines)
    if l > 1: return merge(sort(lines[:l/2]), sort(lines[l/2:]))
    line = lines[0]
    if line.is_category(): line.children = sort(line.children)
    elif line.children != None:
        for cat in line.children: cat.children = sort(cat.children)
    return lines


sorted_lines = sort(ipd.parse_data(sys.argv[1]))
result = open(sys.argv[1] + ".sorted", "w")
for line in sorted_lines: result.write(repr(line) + "\n")
result.close()


