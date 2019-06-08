def print_tree(node):
    stack = []
    decision = set()

    def tree_traverse(node, stack, decision):
        if 'label' in node:
            stack.append(' THEN ' + node['label'])
            decision.add(''.join(stack))
            stack.pop()
        elif 'attribute' in node:
            ifstatement = 'IF ' if not stack else ' AND '
            stack.append(ifstatement + node['attribute'] + ' EQUALS ')
            for subnode in node['nodes']:
                stack.append(subnode)
                tree_traverse(node['nodes'][subnode], stack, decision)
                stack.pop()
            stack.pop()

    tree_traverse(node, stack, decision)
    print(decision)