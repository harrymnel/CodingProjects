def bin_to_dec(binary):
    decimal = 0
    power = len(binary) - 1
    for digit in binary:
        if digit == '1':
            decimal += 2 ** power
        elif digit != '0':
            return "Invalid input. Please enter only binary digits (0's and 1's)."
        power -= 1
    return decimal

def main():
    binary_input = input("Enter up to 8 binary digits: ")
    if len(binary_input) > 8:
        print("Please enter up to 8 binary digits.")
    else:
        result = bin_to_dec(binary_input)
        print("Decimal equivalent:", result)

if __name__ == "__main__":
    main()
