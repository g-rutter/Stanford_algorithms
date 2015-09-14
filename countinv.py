#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Discussed in section 3.

import sys

def sortAndCountInv(A):
    """Count inversions in an n-length array in O(n log n) time using mergesort

    :A: array to count inversions in
    :returns: count of inversions in array

    """

    lenA = len(A)

    if len(A) == 1:
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

        sortedA = []

        while True:
            if B[i] <= C[j]:
                sortedA.append(B[i])
                i += 1
            else:
                sortedA.append(C[j])
                z += ( len(B)-i )
                j += 1

            #If an array reaches its end, add on all the elements from other
            if i == len(B):
                return sortedA + C[j:], x+y+z
            elif j == len(C):
                return sortedA + B[i:], x+y+z

if __name__ == "__main__":

    try:
        array = [ float(element) for element in sys.argv[1:] ]
    except ValueError:
        print "Please pass an unsorted list of floats as the arguments of the program."
        exit()

    print sortAndCountInv(array)
