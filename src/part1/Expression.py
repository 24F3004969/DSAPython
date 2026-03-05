def EvaluateExpression(exp):
    li = exp.split()
    stack = []
    for x in li:
        if x.isdigit():
            stack.append(float(x))
        else:
            a = stack.pop()
            b = stack.pop()
            match x:
                case '*':
                    stack.append(b * a)
                case '+':
                    stack.append(b + a)
                case '-':
                    stack.append(b - a)
                case '/':
                    stack.append(b / a)
                case '**':
                    stack.append(b ** a)
    return stack.pop()
print(EvaluateExpression('3 7 + 12 2 - *'))