#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Quick and dirty implementation of a graph class,
# for interfacing with graph algorithms. My own work.

from prettytable import PrettyTable
import random
from copy import deepcopy

class adjListGraph(object):
    """
    Adjacency list-based graph with methods for construction, destruction
    and inspection of vertices and edges.
    """

    def __init__(self, directed = False, n = 0, m = 0):
        ''' Construct adjListGraph object with n vertices and m edges. If m is
            nonzero, edges are assigned randomly. Use addEdge after creation to
            build a specific graph.
        '''

        self.__vertices__ = []
        self.__edges__ = []
        self.__directed__ = directed

        if n != 0:
            self.randomPopulate(n, m)

    def __str__(self):
        allVerts = self.getVertices()

        table = PrettyTable(['Vertex', 'has edges which link to'])

        for thisVert in allVerts:
            directVerts = thisVert.getDirectVertices()
            table.add_row([thisVert.getValue(),
                           " ".join([str(vert.getValue()) for vert in directVerts]) ])

        return str(table)

    def reorderVertices(self, new_indices):
        ''' Returns copy of self with vertices reordered and internal values
            updated according to new_indices where:

            new_indices[old_index] = new_value

        '''

        h = adjListGraph(directed=self.getDirected())
        old_vertices = self.getVertices()
        N = len(old_vertices)
        new_vertices = [h.addVertex(i + 1) for i in range(N)]

        for edge in self.getEdges():
            old_verts = edge.getVertices()
            new_vert_idx = [new_indices[old_vert.getValue() - 1] - 1
                                                for old_vert in old_verts]

            h.addEdge(new_vertices[new_vert_idx[0]],
                      new_vertices[new_vert_idx[1]])

        return h

    def reverseDirectedGraph(self):
        ''' Returns copy of self with edges reversed. Works but acheives
            nothing if graph is undirected.
        '''

        h = adjListGraph(directed=self.getDirected())
        replacement = {}
        for vert in self.getVertices():
            value = vert.getValue()
            new_vert = h.addVertex(value)
            replacement[value] = new_vert

        for edge in self.getEdges():
            old_vertices = edge.getVertices()
            new_vert1 = replacement[old_vertices[0].getValue()]
            new_vert2 = replacement[old_vertices[1].getValue()]
            h.addEdge(new_vert2, new_vert1)

        return h

    def getDirected(self):
        ''' Turns directed on by default, turns off if passed directed=False
        '''

        return self.__directed__

    def setDirected(self, directed = True):
        ''' Turns directed on by default, turns off if passed directed=False
        '''

        self.__directed__ = directed

    def addVertex(self, value):
        new_vertex = Vertex(self, value) 
        self.__vertices__.append(new_vertex)
        return new_vertex

    def addEdge(self, u, v):
        if u == v:
            print "WARNING not adding loop edge between same u and v."
            print "u.getValue() =", u.getValue()
            return None
        else:
            new_edge = Edge(self, u, v)
            self.__edges__.append(new_edge)
            u.addEdge(new_edge)
            v.addEdge(new_edge)
            return new_edge

    def rmVertex(self, v):
        # Requires removal of all edges associated with v
        vEdges = v.getEdges()
        for edge in vEdges:
            self.rmEdge(edge)

        self.__vertices__.remove(v)

    def rmEdge(self, e):
        # Remove from both of its vertices and from the graph's list of edges
        self.__edges__.remove(e)
        eVertices = e.getVertices()
        eVertices[0].rmEdge(e)
        eVertices[1].rmEdge(e)

    def mergeEdge(self, e):
        # Merge v into u: u takes on v's edges and v is removed from graph.
        (u, v) = e.getVertices()
        self.mergeVertices(u, v)

    def mergeVertices(self, u, v):
        # Merge v into u: u takes on v's edges and v is removed from graph.
        vEdges = v.getEdges()

        for edge in vEdges:
            vEdgeVerts = edge.getVertices()
            if vEdgeVerts[0] != u and vEdgeVerts[1] != u:
                # Then this edge needs to be replicated in u
                if vEdgeVerts[0] == v:
                    self.addEdge(u, vEdgeVerts[1])
                else:
                    self.addEdge(vEdgeVerts[0], u)

        self.rmVertex(v)

    def getVertices(self):
        return tuple(self.__vertices__)

    def getEdges(self):
        return tuple(self.__edges__)

    def randomPopulate(self, n = 10, m = 20):
        "Populate the graph with n nodes and m random connections."

        current_vertices = self.getVertices()
        current_n = len(current_vertices)

        if n+current_n == 1 and m < 0:
            print "ERROR: since self-links are not possible, cannot populate "\
                    "graph of one vertex with edges."
            exit()

        if (current_n != 0):
            print "WARNING: graph is not empty. Edges will not be uniformly "\
                    "distributed and multiple instances of the same vertex "\
                    "value can occur if vertices have been deleted."

        for i in range( current_n, current_n + n):
            self.addVertex(i)

        current_vertices = self.getVertices()

        for j in range(m):
            u = random.choice(current_vertices)
            v = random.choice(current_vertices)

            while u == v:
                v = random.choice(current_vertices)

            self.addEdge(u,v)

class Vertex(object):

    """ Vertex/node object for adjListGraph class."""

    def __init__(self, graph, value):
        self.__edges__ = []
        self.__parent__ = graph
        self.__value__ = value

    def addEdge(self, edge):
        try:
            self.__edges__.index(edge)
            print "Edge" , edge, "already exists on vertex", self
            exit()
        except ValueError:
            self.__edges__.append(edge)

    def rmEdge(self, edge):
        try:
            self.__edges__.remove(edge)
        except ValueError:
            print "rmEdge called on vertex", self,
            print "but edge argument", edge,
            print "does not exist."
            raise

    def getEdges(self):
        return tuple(self.__edges__)

    def getParent(self):
        return self.__parent__

    def getValue(self):
        return self.__value__

    def setValue(self, value):
        self.__value__ = value

    def getDirectVertices(self, reverse=False):
        ''' Vertices this vertex is connected to directly, via a single edge.
            If parent graph is directed, only finds connected verices connected
            by a tail from self to a head at the foreign vertex.
        '''

        edges = self.getEdges()
        dvertices = []
        for edge in edges:
            vert_pair = edge.getVertices()

            if vert_pair[0] != self:
                # On directed graph, this means foreign vertex is at the tail
                # of the edge and can't be reached from here.
                if self.__parent__.__directed__ == False or reverse == True:
                    dvertices.append( vert_pair[0] )
            else:
                if reverse == False:
                    dvertices.append( vert_pair[1] )

        return tuple(dvertices)

class Edge(object):

    """ Edge object for adjListGraph class."""

    def __init__(self, graph, u, v):
        ''' u will be considered tail, and v the head, if graph is directed.
        '''

        self.__vertices__ = (u,v)
        self.__parent__ = graph

    def getVertices(self):
        return tuple(self.__vertices__)

    def getParent(self):
        return self.__parent__

def fromFileType2(filename, directed=True):
    """ Makes a directed adjacencyListGraph object from a text file containing
        an adjacency list. Each row should represent an edge, with the first
        column representing tails and the second, heads.

        e.g.

        1 2
        1 3
        2 7
        ...
    """

    with open(filename, 'r') as graph_file:
        g = adjListGraph(directed=directed)

        # Get largest node value
        max_node = 0
        for line in graph_file:
            node_idxs = [int(index)-1 for index in line.split()]
            max_node = max(node_idxs+[max_node])

    print "Creating", max_node+1, "nodes."
    # Create nodes
    for node_idx in range(max_node+1):
        g.addVertex(node_idx+1)

    verts = g.getVertices()

    print "Creating edges."

    with open(filename, 'r') as graph_file:

        # Create edges
        for line in graph_file:
            node_idxs = [int(index)-1 for index in line.split()]

            tail = verts[node_idxs[0]]
            head = verts[node_idxs[1]]

            g.addEdge(tail, head)

    return g

def fromFileType1(filename):
    """ Makes an adjacencyListGraph object from a text file containing an
        adjaceny list. File should be organised as:

        1 [space-separated list of connections to 1]
        2 [space-separated list of connections to 2]
        3 [space-separated list of connections to 3]
        4 ...

        e.g.

        1 2 3 4 7
        2 1 3 4
        3 1 2 4
        4 1 2 3 5
        5 ...
    """

    with open(filename, 'r') as graph_file:
        g = adjListGraph()

        for line in graph_file:
            values = line.split()

            new_vertex_val = int(values[0])
            adj_vertices_vals = [int(value) for value in values[1:]]

            new_vertex = g.addVertex(new_vertex_val)

            for adj_vertex_val in adj_vertices_vals:
                # Only add vertices with lower value, i.e. already exist.
                if adj_vertex_val <= new_vertex_val:
                    # Assume index of vertex on getVertices() tuple is
                    # adj_vertex_val-1. Safer approach would be to use two-way
                    # dict to map between values and vertices.
                    adj_vertex = g.getVertices()[adj_vertex_val-1]
                    g.addEdge(new_vertex, adj_vertex)

    return g
