n1 = int(input("enter first number: "))
n2 = int(input("enter second number: "))
op_ = ['+','-','*','/','%']
print("choose from the given list of operator")
print(op_)
op = input("enter the operator: ")

while True:
    if op in op_:
        break
    print("enter valid operator!!")
    op = input("enter the operator: ")

if op == '+':
    output = n1+n2
elif op == '-':
    output = n1-n2
elif op == '*':
    output = n1*n2
elif op == '/':
    output = n1/n2
elif op == '%':
    output = n1%n2


print(n1,op,n2,'=',output)    