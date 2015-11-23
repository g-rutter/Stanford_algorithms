#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Discussed in section 14

import sys
import numpy as np

def twoSum(integers, targets):
    ''' The 2-sum problem is determining whether a pair of ints from an array A
        sum to a given target value. Hashing makes this possible in O(n).

        Here, the assignment is to determine the number of targets in a given
        range which can be reached from the input array, with the added
        condition that the two numbers summing to the target must be different.

        The dict type provides a very easy hash table implementation in Py.
    '''

    hashtable = dict([(integer, True) for integer in integers])
    hits = 0

    for integer1 in hashtable.keys():

        for target in targets:

            integer2 = target - integer1

            if integer1 != integer2 and integer2 in hashtable:
                # print integer1, integer2, target
                hits += 1
                targets.remove(target)

    return hits

if __name__ == "__main__":
    filename = sys.argv[1]
    integers = np.fromfile(filename, sep=" ", dtype=np.int64)
    hits = twoSum(integers, range(-10000,10001))
    print hits
