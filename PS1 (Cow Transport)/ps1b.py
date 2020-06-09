###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================
import random
# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # TODO: Your code here
    #sort eggs by biggest to smallest
    egg_weights = sorted(egg_weights,reverse=True)
    #base case
    try:
        return memo[str(target_weight)+str(egg_weights[0])]
    except KeyError:
        if target_weight == 0 or egg_weights == []:
            num_eggs = 0
    
    
        #start by taking the biggest egg, if you cant go right (move on)
        elif target_weight - egg_weights[0] < 0:
            num_eggs = dp_make_weight(egg_weights[1:],target_weight)
            memo[str(target_weight)+str(egg_weights[0])] = num_eggs
        #if u can take the egg, take it
        else:
            num_eggs = 1 + dp_make_weight(egg_weights,target_weight-egg_weights[0])
            memo[str(target_weight)+str(egg_weights[0])] = num_eggs
        return num_eggs






# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = 2
    n = 12399
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
