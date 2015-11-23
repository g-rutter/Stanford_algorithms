#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Discussed in section 9.
# Implements the random contraction algorithm

from adjacencyListGraph import *
import random
import sys
import Queue
import numpy as np
from copy import deepcopy
import heapq

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
                dist[vert] = dist[v] + 1

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
            e = random.choice(allEdges)
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

def DFS_loop(g):
    '''
    Driver for depth-first search finder of strongly connected components
    (Kosaraju's Two-Pass Algorithm). Needs some work doing in global scope,
    e.g.  the following will print the top 5 most populated SSCs:

    t = 0
    s = 0

    h = g.reverseDirectedGraph()
    _, finish_time = DFS_loop(h)
    del h

    g = g.reorderVertices(finish_time)
    leader, _ = DFS_loop(g)

    N = len(g.getVertices())
    counts = []
    for i in range(N):
        counts.append(leader.count(i))
    counts.sort(reverse=True)
    print counts[:5]

    '''

    global s

    N = len(g.getVertices())

    explored = np.zeros(N, dtype=bool) # List of explored nodes by IDX (value-1)
    leader = [-1 for i in range(N)]
    finish_time = np.zeros(N, dtype=int)

    for i in range(N-1, -1, -1):
        if not explored[i]:
            s = i
            DFS_it(g, i, explored, leader, finish_time)

    return leader, finish_time

def DFS(g, i, explored, leader, finish_time):
    ''' Recursive implementation of DFS for finding SSCs
    '''

    global t
    global s
    explored[i] = True
    leader[i] = s

    tail_vert = g.getVertices()[i]
    head_verts = tail_vert.getDirectVertices()

    for head_vert in head_verts:
        j = head_vert.getValue() - 1

        if not explored[j]:
            DFS(g, j, explored, leader, finish_time)

    t += 1
    finish_time[i] = t

def DFS_it(g, start_idx, explored, leader, finish_time):
    ''' Iterative implementation of DFS for finding SSCs
    '''

    global t
    global s

    vertices = g.getVertices()
    stack = [vertices[start_idx]]

    while len(stack) > 0:
        j_vert = stack.pop()
        j = j_vert.getValue() - 1
        j_direct_verts = j_vert.getDirectVertices()

        if finish_time[j] == 0:

            if not explored[j]:
                explored[j] = True
                leader[j] = s

            toappend = []
            for j_direct_vert in j_direct_verts:
                if not explored[(j_direct_vert.getValue() - 1)]:
                    toappend.append(j_direct_vert)

            if len(toappend) == 0:
                t += 1
                finish_time[j] = t
            else:
                stack.append(j_vert)
                stack += toappend

def Dijkstra_Shortest_Path(g, start_idx):
    ''' Heap implementation of Dijkstra's shortest path algorithm for exploring
        graphs with weighted paths.
    '''

    vertices = g.getVertices()
    N = len(vertices)
    start = vertices[start_idx]

    shortest = np.zeros([N], dtype=int)

    #Initialise heap
    h = []
    # map vertex idx to entry on heap
    vertex_finder = {}
    for vert_idx in range(N):
        vert_partners, lengths = vertices[vert_idx].getDirectVertices()
        try:
            dist = lengths[vert_partners.index(start)]
        except ValueError:
            dist = sys.maxint

        entry = [dist, vert_idx]
        heapq.heappush(h, entry)
        vertex_finder[vert_idx] = entry

    while h:

        #Extract-min and add to shortest
        nearest_dist, nearest_vert_idx = heapq.heappop(h)
        if nearest_vert_idx != -1:
            shortest[nearest_vert_idx] = nearest_dist

            #Update heap
            for neigh_vert, neigh_length in zip(*vertices[nearest_vert_idx].getDirectVertices()):
                neigh_idx = neigh_vert.getValue() - 1

                if shortest[neigh_idx] != 0:
                    continue

                neigh_new_length = nearest_dist + neigh_length

                entry = vertex_finder[neigh_idx]
                neigh_old_length = entry[0]
                entry[1] = -1
                entry[0] = -1

                if neigh_new_length < neigh_old_length:
                    new_entry = [neigh_new_length, neigh_idx]
                else:
                    new_entry = [neigh_old_length, neigh_idx]

                heapq.heappush(h, new_entry)
                vertex_finder[neigh_idx] = new_entry

    return shortest

if __name__ == "__main__":

    try:
        filename = sys.argv[1]
    except IndexError:
        print "Please pass the name of the file containing an adjacency list "\
              "for a graph as the first argument."
        raise

    ############################
    #  For depth-first search  #
    ############################

    # g = fromFileType2(filename)
    # print "Read-in complete."

    # t = 0
    # s = 0

    # h = g.reverseDirectedGraph()
    # _, finish_time = DFS_loop(h)
    # del h

    # print "finish_time obtained."
    # g = g.reorderVertices(finish_time)
    # print "Calculating leader"
    # leader, _ = DFS_loop(g)
    # print leader

    # N = len(g.getVertices())
    # counts = []
    # for i in range(N):
        # counts.append(leader.count(i))
    # counts.sort(reverse=True)
    # print counts[:5]

    ###################################
    #  For shortest-path computation  #
    ###################################

    g = fromFileType3(filename)
    print g
    shortest = Dijkstra_Shortest_Path(g, 0)
