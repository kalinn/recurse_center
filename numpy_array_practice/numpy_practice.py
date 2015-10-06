# numpy_array_practice
# Simple game to practice numpy array slicing in python.
# I wrote this on day 3 of my Recurse Center batch to become more familiar with writing functions and manipulating arrays in python.
# Run from the terminal with 'python numpy_practice.py' or in IPython with '%run numpy_practice.py'

import numpy as np
import random

def main():
    person = raw_input('Enter your name: ')
    print('Hello ' + person + "!")

    dims = [random.randint(1, 10) for dim in range(2)]
    fills = reduce(lambda x, y: x*y, dims)
    # Original matrix
    z = np.arange(fills).reshape(tuple(dims))
    # Make reduced matrix
    d1_start = 0
    d1_end = 0
    while(d1_start==d1_end):
        d1_start = random.randint(0, z.shape[0])
        d1_end = random.randint(d1_start, z.shape[0])
    d2_start = 0
    d2_end = 0
    while(d2_start==d2_end):
        d2_start = random.randint(0, z.shape[1])
        d2_end = random.randint(d2_start, z.shape[1])
    # Several cases
    case = random.randint(0, 4)
    if case==0:
        sliced_matrix = z[d1_start:d1_end, d2_start:d2_end]
    elif case==1:
        sliced_matrix = z[:, d2_start:d2_end]
    elif case==2:
        sliced_matrix = z[d1_start:d1_end, :]
    elif case==3:
        sliced_matrix = z[:, d2_start]
    else:
        sliced_matrix = z[d1_start, :]
    print 'Reduce'
    print z
    print 'to'
    print sliced_matrix
    incorrect = True
    while(incorrect):
        answer = input('Enter your solution in the form z[<answer>]: ')
        print answer
        if np.array_equal(sliced_matrix, answer):
            print 'Contratulations! You answered correctly, ' + person
            incorrect = False
        else:
            print 'Try again, ' + person
    again = raw_input('Play again? y/n ')
    if again=='y':
        main()


if __name__ == "__main__":
    main()

