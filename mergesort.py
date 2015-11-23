#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Discussed in section 2.

import sys
import pdb
import numpy as np

def mergeSort(A):
    '''Return sorted copy of A'''

    lenA = len(A)

    if lenA <= 1:
        return A

    else:
        halflenA = lenA/2
        B = mergeSort(A[:halflenA])
        C = mergeSort(A[halflenA:])

        # Merge sorted arrays B and C
        i = 0
        j = 0
        sortedA = np.array([])
        while True:
            if B[i] < C[j]:
                sortedA = np.append(sortedA, B[i])
                i += 1
            else:
                sortedA = np.append(sortedA, C[j])
                j += 1

            # If an array reaches its end, add on all the elements from other
            if i == len(B):
                return np.append(sortedA, C[j:])
            elif j == len(C):
                return np.append(sortedA, B[i:])

if __name__ == "__main__":

    try:
        unsorted = [float(element) for element in sys.argv[1:]]
        unsorted = np.array(unsorted)
    except ValueError:
        print "Please pass an unsorted list of floats as the arguments of the program."
        exit()

    print mergeSort(unsorted)
