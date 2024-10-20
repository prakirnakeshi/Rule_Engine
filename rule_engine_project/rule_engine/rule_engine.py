class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type  # "operator" or "operand"
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        if self.node_type == "operator":
            return f"Node(type='operator', value='{self.value}', left={repr(self.left)}, right={repr(self.right)})"
        else:
            return f"Node(type='operand', value='{self.value}')"


def parse_rule(rule_string):
    tokens = rule_string.replace("(", "").replace(")", "").split()
    stack = []

    for token in tokens:
        if token in ("AND", "OR"):
            right = stack.pop()
            left = stack.pop()
            stack.append(Node(node_type="operator", left=left, right=right, value=token))
        else:
            stack.append(Node(node_type="operand", value=token))

    return stack[0] if stack else None

def evaluate(ast, data):
    if ast.node_type == "operand":
        # For simplicity, assume value is in the format "attribute > value"
        attribute, operator, value = ast.value.split()
        user_value = data.get(attribute)

        if operator == '>':
            return user_value > int(value)
        elif operator == '<':
            return user_value < int(value)
        elif operator == '=':
            return user_value == value
        return False
    elif ast.node_type == "operator":
        left_result = evaluate(ast.left, data)
        right_result = evaluate(ast.right, data)

        if ast.value == "AND":
            return left_result and right_result
        elif ast.value == "OR":
            return left_result or right_result
    return False
