#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Discussed in section 5

import numpy as np
import sys
import argparse

def partition(A, pivot):
    '''
    In-place partition in linear time
    as specified by quickSort algorthm
    '''

    #Put pivot element first
    A[0], A[pivot] = A[pivot], A[0]

    j = 1 #Boundary between halves of partition

    for i in range(1, len(A)):

        if A[i] < A[0]:
            # Put A[i] at end of left half of partition
            A[i], A[j] = A[j], A[i]
            j += 1

    #Put pivot element at boundary
    A[j-1], A[0] = A[0], A[j-1]

    return A, j-1

def quickSort(A):

    if len (A) < 2:
        return A

    p = np.random.randint(0, len(A))
    (A, p) = partition(A, p)
    #calling QS on left side
    A[:p] = quickSort(A[:p])
    A[p+1:] = quickSort(A[p+1:])

    return A

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        'quickSort in-place sorting algorithm in O(n log n)')
    parser.add_argument('-A', type=float, nargs='+',
            help='Array to sort')
    args = parser.parse_args()

    sys.setrecursionlimit(40)

    A = np.array(args.A)
    A = quickSort(A)
    print A
