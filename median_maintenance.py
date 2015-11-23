#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Discussed in section 12

import sys
import numpy as np
import heapq

def getMedians(integers):
    ''' Use two heaps to record the median for each of integers[:1],
        integers[:2], integers[:3], ... integers

        Since we use a heap with smallest on top, the low heap shall store
        negatives of the relevant values
    '''

    lowheap = [-integers[0]]
    highheap = []
    medians = np.empty(len(integers), dtype=int)
    medians[0] = integers[0]

    for i, newint in enumerate(integers[1:]):

        # Add new value to the heap
        if newint > -lowheap[0]:
            heapq.heappush(highheap, newint)
            # If this made highheap bigger than lowheap, rebalance
            if len(highheap) > len(lowheap):
                val = heapq.heappop(highheap)
                heapq.heappush(lowheap, -val)

        else:
            heapq.heappush(lowheap, -newint)
            # If this made lowheap more than 1 bigger than highheap, rebalance
            if len(lowheap) - 1 > len(highheap):
                val = -heapq.heappop(lowheap)
                heapq.heappush(highheap, val)

        medians[i+1] = -lowheap[0]


    return medians

if __name__ == "__main__":

    filename = sys.argv[1]
    integers = np.fromfile(filename, sep=" ", dtype=np.int64)
    medians = getMedians(integers)

    print sum(medians)
