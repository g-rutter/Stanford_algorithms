#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Discussed in section 9.
# Implements the random contraction algorithm

from adjacencyListGraph import adjListGraph
import random
import Queue

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

def minCutRandomContract(g):
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

if __name__ == "__main__":

    g = adjListGraph(n = 20, m = 40)
    # minCutRandomContract(g)

    print g
    print "From", g.getVertices()[0].getValue(), "to", g.getVertices()[1].getValue()
    length = shortestPath(g.getVertices()[0], g.getVertices()[1])
    print "Shortest path is", length, "steps."

