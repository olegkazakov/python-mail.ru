import sys
digit_string = sys.argv[1]

print(sum(int(symb) for symb in digit_string if symb.isdigit()))
