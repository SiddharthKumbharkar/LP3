# Assignment 1: Fibonacci numbers - recursive and non-recursive
#
# Recursive:
#   Time Complexity  -> O(2^n)
#   Space Complexity -> O(n)  (recursion call stack)
#
# Iterative:
#   Time Complexity  -> O(n)
#   Space Complexity -> O(1)

def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_iterative(n):
    if n <= 1:
        return n
    a = 0
    b = 1
    for i in range(2, n + 1):
        c = a + b
        a = b
        b = c
    return b


def main():
    while True:
        print("\n1. Fibonacci using Recursion")
        print("2. Fibonacci using Iteration (Non-Recursion)")
        print("3. Compare both")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            n = int(input("Enter n: "))
            print("Fibonacci number is:", fib_recursive(n))

        elif choice == "2":
            n = int(input("Enter n: "))
            print("Fibonacci number is:", fib_iterative(n))

        elif choice == "3":
            n = int(input("Enter n: "))

            print("Recursive result :", fib_recursive(n))
            print("Iterative result :", fib_iterative(n))

        elif choice == "4":
            print("Exiting.")
            break

        else:
            print("Invalid choice")


main()
