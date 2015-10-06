#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Discussed in section 3.

import sys
import argparse
import numpy as np

def sortAndCountInv(A):
    """Count inversions in an n-length array in O(n log n) time using mergesort

    :A: array to count inversions in
    :returns: count of inversions in array

    """

    lenA = len(A)

    if lenA == 1:
        return A, 0

    else:
        B,x = sortAndCountInv( A[:lenA/2] )
        C,y = sortAndCountInv( A[lenA/2:] )

        #Merge sorted arrays B and C
        #indexes of lists to iterate over:
        i = 0
        j = 0
        #inversion counter:
        z = 0

        sortedA = np.array([], dtype=int)

        while True:
            if B[i] <= C[j]:
                sortedA = np.append(sortedA, B[i])
                i += 1
            else:
                sortedA = np.append(sortedA, C[j])
                z += ( len(B)-i )
                j += 1

            #If an array reaches its end, add on all the elements from other
            if i == len(B):
                return np.append(sortedA, C[j:]), x+y+z
            elif j == len(C):
                return np.append(sortedA, B[i:]), x+y+z

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        'Use mergeSort logic to count inversions in an array of ints. O(n log n)')
    parser.add_argument('-A', type=int, nargs='+',
            help='Array to sort as command-line input')
    parser.add_argument('-f', type=str,
            help='Order of statistic to return')
    args = parser.parse_args()

    if args.f != None:
        A = np.fromfile(args.f, sep=" ", dtype=int)
    elif args.A != None:
        A = np.array(args.A, dtype=int)
    else:
        print "Please pass an array in the command line after -A, or the name"\
              " of a file containing an array after -f."
        exit()
    print sortAndCountInv(A)[1]
