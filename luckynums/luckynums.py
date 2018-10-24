import numpy as np 


def get_lucky_nums(max_num, max_pb, num_of_nums=5):
    """ Print a random set of numbers and a powerball """

    # Calculate random numbers in given range after scrambling a random amount of iterations
    iterations = np.random.randint(1,11)
    for i in range(iterations):
        nums =  np.random.randint(1, max_num + 1, size=num_of_nums)
        powerball = np.random.randint(1, max_pb + 1, size=1)

    # Replace any duplicates
    final = []
    for num in nums:
        if num not in final:
            final.append(num)
        else:
            replacement = np.random.randint(1,70, size=1)
            final.append(replacement[0])
            # If replacement is another duplicate, it is removed from final and recalculated
            while num == replacement:
                final.pop()
                replacement = np.random.randint(1,70, size=1)
                final.append(replacement[0])

    # Convert final from list to numpy array
    final = np.asarray(final)

    # Print result
    print(f"Your numbers are: {final}")
    print(f"Powerball: {powerball[0]}")


get_lucky_nums(70, 25)

# "May the odds be ever in your favor"
