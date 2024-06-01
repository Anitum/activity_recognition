import numpy as np
import matplotlib.pyplot as plt

def generate_function(p, length=100):
    """Generate a random function based on given probabilities."""
    function = [0]  # Initial value
    for _ in range(length - 1):
        if np.random.rand() < p:
            function.append(function[-1] + 1)  # Go up
        else:
            function.append(function[-1] - 1)  # Go down
    return function

def plot_functions(functions, probabilities):
    """Plot the generated functions."""
    for func, prob in zip(functions, probabilities):
        plt.plot(func, label=f"p = {prob}")
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Graph of the Given Functions')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    # Choose whether to enter probabilities or generate random probabilities
    choice = input("Do you want to enter probabilities for each function? (yes/no): ").lower()
    
    if choice == 'yes':
        # Input parameters
        num_functions = int(input("Enter the number of functions to generate: "))
        probabilities = []
        for i in range(num_functions):
            prob = float(input(f"Enter the probability of going up for function {i+1} (between 0 and 1): "))
            probabilities.append(prob)
    elif choice == 'no':
        # Input parameters
        num_functions = int(input("Enter the number of functions to generate: "))
        probabilities = np.random.rand(num_functions)  # Generate random probabilities
    else:
        print("Invalid choice.")
        return
    
    length = int(input("Enter the length of the function: "))

    # Generate the functions
    functions = [generate_function(p, length) for p in probabilities]

    # Plot the functions
    plot_functions(functions, probabilities)

if __name__ == "__main__":
    main()
