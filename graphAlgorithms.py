#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Discussed in section 9.
# Implements the random contraction algorithm

from adjacencyListGraph import adjListGraph, fromFile
import random
import sys
import Queue
from copy import deepcopy

def shortestPath(start, goal):
    '''
    Use breadth-first search and keep track of minimum distance of each 
    explored node from starting node. Terminate when goal node is reached.

    Return: number of edges between node start and node goal.
            If these nodes are unconnected, returns float('inf').
    '''

    vertexqueue = Queue.Queue()
    vertexqueue.put(start)
    exploredVerts = [start]
    dist          = {start:0}

    if start == goal:
        return dist[start]

    while vertexqueue.empty() != True:

        v = vertexqueue.get()
        vDVertices = v.getDirectVertices()

        for vert in vDVertices:

            if vert not in exploredVerts:

                exploredVerts.append(vert)
                vertexqueue.put(vert)
                dist[vert] = dist[v]+1

                if vert == goal:
                    return dist[vert]

    return float("inf")

def RandomContract(g):
    '''
    Takes a graph g and executes uniformly selected random cuts on it
    iteratively, yielding the minimum cut with 1/n^2 probability.
    '''

    while len( g.getVertices() ) > 2:

        allEdges = g.getEdges()
        try:
            e = random.choice( allEdges )
        except IndexError:
            print "ERROR: All edges removed before vertex counted reached 2. "\
                    "This implies the graph was disconnected."
            raise
        g.mergeEdge(e)

def nRandomContracts(g, n=1000):
    '''
    Runs RandomContract on a copy of g, n times.
    Returns the minimum cut found (lowest number of edges in the final graph.)
    over all n runs.
    '''

    mincut = len(g.getEdges())

    for i in range(n):
        h = deepcopy(g)
        RandomContract(h)
        mincut = min([mincut, len(h.getEdges())])

    return mincut

if __name__ == "__main__":


    try:
        filename = sys.argv[1]
    except IndexError:
        print "Please pass the name of the file containing an adjacency list "\
              "for a graph as the first argument."
        raise

    # g = adjListGraph(n = 20, m = 40)
    g = fromFile(filename)
    sys.setrecursionlimit(2500)

    print nRandomContracts(g, n=1000)
