# Assignment 4: N-Queens Problem using Backtracking (first queen already placed)
#
# Time Complexity  -> O(N!) worst case (backtracking search)
# Space Complexity -> O(N)  (board array + recursion call stack)

def is_safe(board, row, col):
    for r in range(row):
        c = board[r]
        if c == col:
            return False
        if abs(c - col) == abs(r - row):
            return False
    return True


def solve(board, row, n, first_row):
    if row == n:
        return True

    if row == first_row:
        return solve(board, row + 1, n, first_row)

    for col in range(n):
        if is_safe(board, row, col):
            board[row] = col
            if solve(board, row + 1, n, first_row):
                return True
            board[row] = -1

    return False


def print_board(board, n):
    for row in range(n):
        line = ""
        for col in range(n):
            if board[row] == col:
                line = line + "Q "
            else:
                line = line + ". "
        print(line)


def main():
    while True:
        print("\n1. Solve N-Queens")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            n = int(input("Enter value of n: "))
            first_row = int(input("Enter row of first queen (0 to " + str(n - 1) + "): "))
            first_col = int(input("Enter column of first queen (0 to " + str(n - 1) + "): "))

            board = [-1] * n
            board[first_row] = first_col

            if not is_safe(board, first_row, first_col):
                print("Invalid placement for first queen")
                continue

            if solve(board, 0, n, first_row):
                print("\nSolution:")
                print_board(board, n)
            else:
                print("No solution exists")

        elif choice == "2":
            print("Exiting.")
            break

        else:
            print("Invalid choice")


main()
