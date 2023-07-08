"""Python Lottery Number Generator
This is a simple program to help us choose lottery number
"""
import secrets

# Declare needed constants
START = 1
END = 55
AMOUNT = 6

numbers = [secrets.randbelow(END - START + 1) + START for _ in range(AMOUNT)]
numbers.sort()

print(f"Your lucky number today: {numbers}")
