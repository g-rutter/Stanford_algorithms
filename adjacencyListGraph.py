#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Quick and dirty implementation of a graph class,
# for interfacing with graph algorithms. My own work.

from prettytable import PrettyTable
import random

class adjListGraph(object):

    """
    Adjacency list-based graph with methods for construction, destruction
    and inspection of vertices and edges.
    """

    def __init__(self, n = 0, m = 0):
        self.__vertices__ = []
        self.__edges__ = []

        if n != 0:
            self.randomPopulate(n,m)

    def __str__(self):
        allVerts = self.getVertices()

        table = PrettyTable(['Vertex', 'has edges which link to'])

        for thisVert in allVerts:
            directVerts = thisVert.getDirectVertices()
            table.add_row([thisVert.getValue(),
                           " ".join([str(vert.getValue()) for vert in directVerts]) ])

        return str(table)

    def addVertex(self, value):
        self.__vertices__.append( Vertex(self, value) )

    def addEdge(self, u, v):
        newEdge = Edge(self, u, v)
        self.__edges__.append( newEdge )
        u.addEdge(newEdge)
        v.addEdge(newEdge)

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
        (u,v) = e.getVertices()
        self.mergeVertices(u,v)

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
            print "WARNING: graph is not empty. Edges will not uniformly "\
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

    def getDirectVertices(self):
        '''Vertices this vertex is connected to directly, via a single edge.'''
        edges = self.getEdges()
        dvertices = []
        for edge in edges:
            vert_pair = edge.getVertices()

            if vert_pair[0] != self:
                dvertices.append( vert_pair[0] )
            else:
                dvertices.append( vert_pair[1] )

        return tuple(dvertices)

class Edge(object):

    """ Edge object for adjListGraph class."""

    def __init__(self, graph, u, v):
        self.__vertices__ = (u,v)
        self.__parent__ = graph

    def getVertices(self):
        return tuple(self.__vertices__)

    def getParent(self):
        return self.__parent__
