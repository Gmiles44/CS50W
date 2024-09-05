import sys

try:
    x = int(input("x: "))
    y = int(input("y: "))
except ValueError:
    print("Input an actual number")

try:
    result = x / y
    print(f"{x} / {y} = {result}")
except ZeroDivisionError:
    print("Let's do something else, shall we? We will add these two numbers instead")
    result2 = x + y
    print(f"{x} + {y} = {result2}")
