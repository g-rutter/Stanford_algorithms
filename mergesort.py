#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Discussed in section 2.

import sys
import pdb

def mergeSort(A):
    '''Return sorted copy of A'''

    print "Entering mergeSort with", A
    lenA = len(A)

    if lenA <= 1:
        return A

    else:
        halflenA = lenA/2
        B = mergeSort(A[halflenA:])
        C = mergeSort(A[:halflenA])

        #Merge sorted arrays A and B
        i = 0
        j = 0
        sortedA = []
        while (i+j) < lenA:
            if B[i] < C[j]:
                sortedA.append(B[i])
                i += 1
            else:
                sortedA.append(C[j])
                j += 1

            #If an array reaches its end, add on all the elements from other
            if i == len(B):
                [sortedA.append(C[k]) for k in range(j, len(C))]
                return sortedA
            elif j == len(C):
                [sortedA.append(B[k]) for k in range(i, len(B))]
                return sortedA

        return sortedA


if __name__ == "__main__":
    unsorted = [ float(element) for element in sys.argv[1:] ]

    # pdb.run( 'mergeSort(unsorted)' )
    print mergeSort(unsorted)


