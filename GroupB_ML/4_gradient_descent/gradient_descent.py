"""
Assignment 4: Gradient Descent to find the local minima of a function.

Example function: y = (x + 3)^2, starting at x = 2.
Derivative      : dy/dx = 2 * (x + 3)
Update rule     : x_new = x_old - learning_rate * dy/dx
"""

import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return (x + 3) ** 2


def df(x):
    return 2 * (x + 3)


def gradient_descent(start_x, learning_rate=0.1, iterations=100, tolerance=1e-6):
    x = start_x
    history = [x]

    for i in range(iterations):
        grad = df(x)
        new_x = x - learning_rate * grad
        history.append(new_x)
        if abs(new_x - x) < tolerance:
            x = new_x
            break
        x = new_x

    return x, history


if __name__ == "__main__":
    start_x = 2
    learning_rate = 0.1
    minima_x, history = gradient_descent(start_x, learning_rate)

    print(f"Function   : y = (x + 3)^2")
    print(f"Start      : x = {start_x}")
    print(f"Learning rate = {learning_rate}\n")

    print(f"{'iter':>5} | {'x':>12} | {'y=f(x)':>12}")
    print("-" * 35)
    for i, x in enumerate(history[:15]):
        print(f"{i:>5} | {x:>12.6f} | {f(x):>12.6f}")
    if len(history) > 15:
        print("...")

    print(f"\nConverged after {len(history) - 1} iterations")
    print(f"Local minima at x = {minima_x:.6f}, y = {f(minima_x):.6f}")
    print("Expected minima: x = -3, y = 0")

    xs = np.linspace(-8, 4, 200)
    plt.plot(xs, f(xs), label="y = (x+3)^2")
    plt.plot(history, [f(x) for x in history], "o-", color="red", label="gradient descent path")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.title("Gradient Descent Convergence")
    plt.show()
