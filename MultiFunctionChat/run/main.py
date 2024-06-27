import random

# Generate 10 random numbers
random_numbers = [random.randint(1, 100) for _ in range(10)]

# Write the random numbers to a file
with open('numbers.txt', 'w') as file:
    for number in random_numbers:
        file.write(f"{number}\n")

print("10 random numbers have been written to numbers.txt")