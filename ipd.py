
# line types
CATEGORY = 'c'
ATTRIBUTES = 'a'


class Line:
    '''
    a line in ipd file
    '''
    def __init__(self, type, contents):
        self.type = type
        self.contents = contents
        self.children = []
    
    def pretty_print(self, indent):
        lines = ['\t' * indent + '|'.join(self.contents)]
        for child in self.children: lines.append(child.pretty_print(indent + 1))
        return '\n'.join(lines)

    def __cmp__(self, other):
        if not self.type == other.type == ATTRIBUTES: raise Exception('only attributes lines can be compared')
        for i in range(min(len(self.contents), len(other.contents))):
            if self.contents[i] < other.contents[i]: return -1
            elif self.contents[i] > other.contents[i]: return 1
        return sign(len(self.contents) - len(other.contents))

    def __repr__(self): 
        return self.pretty_print(0)
    
    def is_category(self):
        return self.type == CATEGORY
        

def parse_data(file_name):
    '''
    parses data from supplied file_name and returns a list of top-level lines
    '''
    f = open(file_name)
    node_stack = [Line("root", None)]
    prev_indent_level = 0
    prev_node = None
    for line in f.readlines():
        indent_level = 0
        line = line.rstrip()
        while line[0] == '\t':
            line = line[1:]
            indent_level += 1
        parent = None
        if indent_level == prev_indent_level:
            parent = node_stack.pop()
        elif indent_level < prev_indent_level:
            while prev_indent_level > indent_level:
                parent = node_stack.pop()
                prev_indent_level -= 1
            parent = node_stack.pop()
        else:
            parent = prev_node
            prev_indent_level = indent_level
        current_node = Line(CATEGORY if _is_category_level(indent_level) else ATTRIBUTES, line.split('|'))
        parent.children.append(current_node)
        node_stack.append(parent)
        prev_node = current_node
    f.close()
    parent = None
    while len(node_stack) > 0: parent = node_stack.pop()
    return parent.children

    
def _is_category_level(level): return level % 2 == 1


def sign(num):
    if num < 0: return -1
    elif num == 0: return 0
    else: return 1
    
