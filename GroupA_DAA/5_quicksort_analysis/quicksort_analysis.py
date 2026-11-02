# Assignment 5: Quick Sort - Deterministic vs Randomized pivot
#
# Deterministic (last element as pivot):
#   Time Complexity  -> O(n log n) average, O(n^2) worst case
#                        (worst case triggered by sorted/reverse-sorted input)
#   Space Complexity -> O(log n) average, O(n) worst case (recursion stack)
#
# Randomized (random pivot):
#   Time Complexity  -> O(n log n) average, O(n^2) worst case (rare in practice)
#   Space Complexity -> O(log n) average, O(n) worst case (recursion stack)

import random
import time
import sys

sys.setrecursionlimit(10000)


def partition(arr, low, high, pivot_index):
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def deterministic_sort(arr, low, high):
    if low < high:
        pivot_index = partition(arr, low, high, high)
        deterministic_sort(arr, low, pivot_index - 1)
        deterministic_sort(arr, pivot_index + 1, high)


def randomized_sort(arr, low, high):
    if low < high:
        random_index = random.randint(low, high)
        pivot_index = partition(arr, low, high, random_index)
        randomized_sort(arr, low, pivot_index - 1)
        randomized_sort(arr, pivot_index + 1, high)


def main():
    while True:
        print("\n1. Sort your own array")
        print("2. Compare timing on random, sorted and reverse sorted data")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            data = input("Enter array elements separated by space: ")
            arr1 = []
            for x in data.split():
                arr1.append(int(x))
            arr2 = arr1.copy()

            deterministic_sort(arr1, 0, len(arr1) - 1)
            randomized_sort(arr2, 0, len(arr2) - 1)

            print("Sorted using Deterministic Quick Sort:", arr1)
            print("Sorted using Randomized Quick Sort   :", arr2)

        elif choice == "2":
            n = int(input("Enter number of elements: "))

            random_data = []
            for i in range(n):
                random_data.append(random.randint(0, 100000))

            sorted_data = list(range(n))
            reverse_data = list(range(n, 0, -1))

            datasets = [
                ("Random Data", random_data),
                ("Sorted Data (worst case for deterministic)", sorted_data),
                ("Reverse Sorted Data (worst case for deterministic)", reverse_data),
            ]

            for name, data in datasets:
                arr1 = data.copy()
                arr2 = data.copy()

                start = time.time()
                deterministic_sort(arr1, 0, len(arr1) - 1)
                end = time.time()
                det_time = end - start

                start = time.time()
                randomized_sort(arr2, 0, len(arr2) - 1)
                end = time.time()
                rand_time = end - start

                print("\n" + name)
                print("Deterministic Quick Sort Time:", det_time)
                print("Randomized Quick Sort Time   :", rand_time)

        elif choice == "3":
            print("Exiting.")
            break

        else:
            print("Invalid choice")


main()
