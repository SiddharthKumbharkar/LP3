# Assignment 3: 0/1 Knapsack Problem
# Dynamic Programming approach and Branch and Bound approach
#
# Dynamic Programming:
#   Time Complexity  -> O(n * W)  (n = items, W = capacity)
#   Space Complexity -> O(n * W)  (dp table)
#
# Branch and Bound:
#   Time Complexity  -> O(2^n) worst case, prunes many branches in practice
#   Space Complexity -> O(n)  (recursion call stack)

def knapsack_dp(weights, values, capacity, n):
    dp = []
    for i in range(n + 1):
        row = [0] * (capacity + 1)
        dp.append(row)

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]


best_value = 0


def knapsack_branch_bound(weights, values, capacity, n, index, current_weight, current_value):
    global best_value

    if current_weight <= capacity and current_value > best_value:
        best_value = current_value

    if index == n or current_weight > capacity:
        return

    # upper bound: assume all remaining items can be added (loose bound used for pruning)
    remaining_value = current_value
    for i in range(index, n):
        remaining_value = remaining_value + values[i]
    if remaining_value <= best_value:
        return

    # include current item
    knapsack_branch_bound(weights, values, capacity, n, index + 1,
                           current_weight + weights[index], current_value + values[index])

    # exclude current item
    knapsack_branch_bound(weights, values, capacity, n, index + 1,
                           current_weight, current_value)


def main():
    global best_value

    while True:
        print("\n1. Solve using Dynamic Programming")
        print("2. Solve using Branch and Bound")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1" or choice == "2":
            n = int(input("Enter number of items: "))
            weights = []
            values = []
            for i in range(n):
                w = int(input("Enter weight of item " + str(i + 1) + ": "))
                v = int(input("Enter value of item " + str(i + 1) + ": "))
                weights.append(w)
                values.append(v)
            capacity = int(input("Enter capacity of knapsack: "))

            if choice == "1":
                result = knapsack_dp(weights, values, capacity, n)
                print("Maximum value (Dynamic Programming):", result)
            else:
                best_value = 0
                knapsack_branch_bound(weights, values, capacity, n, 0, 0, 0)
                print("Maximum value (Branch and Bound):", best_value)

        elif choice == "3":
            print("Exiting.")
            break

        else:
            print("Invalid choice")


main()
