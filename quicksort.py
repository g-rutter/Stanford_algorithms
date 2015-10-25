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

def quickSort(A, pick='random'):
    '''
    The famous QuickSort algorithm. This implementation takes an array A and
    returns it sorted.

    It also counts the number of comparisons made to achieve the final result,
    and allows multiple pivot selection criteria, beyond the usual 'random'.
    This is for the Stanford course assignment.
    '''

    if len (A) < 2:
        return A, 0

    if pick == 'random':
        p = np.random.randint(0, len(A))
    elif pick == 'first':
        p = 0
    elif pick == 'last':
        p = A.shape[0] - 1
    elif pick == 'median':
        start, mid, end = A[0], A[(A.shape[0]-1)/2], A[A.shape[0]-1]
        if start < mid < end or end < mid < start:
            p = (A.shape[0]-1)/2
        elif mid < start < end or end < start < mid:
            p = 0
        else:
            p = A.shape[0] - 1

    (A, p) = partition(A, p)

    C = A.shape[0] - 1

    (A[:p], C1)   = quickSort(A[:p], pick=pick)
    (A[p+1:], C2) = quickSort(A[p+1:], pick=pick)

    C += C1 + C2

    return A, C

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        'quickSort in-place sorting algorithm in O(n log n)')
    parser.add_argument('-A', type=float, nargs='+',
            help='Array to sort')
    parser.add_argument('-f', type=str,
            help='Name of file containing an array.')
    parser.add_argument('-p', type=str, default='random',
            help='Pivot picking scheme. One of: \'random\', \'first\', \'last\'')
    args = parser.parse_args()

    if args.f != None:
        A = np.fromfile(args.f, sep=" ", dtype=int)
    elif args.A != None:
        A = np.array(args.A, dtype=int)
    else:
        print "Please pass an array in the command line after -A, or the name"\
              " of a file containing an array after -f."
        exit()

    A, C = quickSort(A, pick=args.p)
    print A
    print C
