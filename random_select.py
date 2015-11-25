#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Discussed in section 8

import numpy as np
import sys
import argparse


def partition(A, pivot):
    '''
    In-place partition in linear time
    as specified by randomSelect algorthm
    '''

    # Put pivot element first
    A[0], A[pivot] = A[pivot], A[0]

    j = 1  # Boundary between halves of partition

    for i in range(1, len(A)):

        if A[i] < A[0]:
            # Put A[i] at end of left half of partition
            A[i], A[j] = A[j], A[i]
            j += 1

    # Put pivot element at boundary
    A[j - 1], A[0] = A[0], A[j - 1]

    return A, j - 1


def randomSelect(A, i):
    '''
    Use randomization of pivot point to find
    ith element by magnitude
    '''

    if len(A) == 1:
        return A

    p = np.random.randint(0, len(A))
    (A, p) = partition(A, p)

    # Hone in without sorting unnecessary array regions
    if p < i:
        A = randomSelect(A[p + 1:], i - (p + 1))
    elif p > i:
        A = randomSelect(A[:p], i)
    elif p == i:
        A = A[p:p + 1]

    return A

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        'randomSelect in-place sorting algorithm in O(n log n)')
    parser.add_argument('-A', type=float, nargs='+',
                        help='Array to sort')
    parser.add_argument('-i', type=float,
                        help='Order of statistic to return')
    args = parser.parse_args()

    A = np.array(args.A)
    s = randomSelect(A, args.i)[0]
    print s
