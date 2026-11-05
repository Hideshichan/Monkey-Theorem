# roll a 6 sided dice 20 times. find every time 2 consecutive rolls are the same (so a double roll)
# file made with assistance from Claude Sonnet 5, it was used as a tutor rather than a developer

import numpy as np
rng = np.random.default_rng()

# generate 20 random numbers between [1,7)
random_ints = rng.integers(low=1, high=7, size=1000000000)

# use a sliding window to check the array for a pattern, in this case 3 consecutive identical numbers
window = np.lib.stride_tricks.sliding_window_view(random_ints, 3)
# break the 2d array into n 1d arrays of 1st rolls and 2nd rolls and... n rolls
first_rolls = window[:, 0]
second_rolls = window[:, 1]
third_rolls = window[:, 2]

# compare rolls for identity
comparison = (first_rolls == second_rolls) & (second_rolls == third_rolls)

# count how many true and what index they are at
number_matches = np.sum(comparison)
where_matches_tuple = np.where(comparison == True)
where_matches = where_matches_tuple[0]


#print(random_ints)
#print(comparison)
#print(number_matches)
#print(where_matches)


print(f"Rolled {random_ints.size:,} times. Found {number_matches:,} contiguous pairs at positions {where_matches}")