#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Discussed in section 3.

import argparse
import numpy as np


def Strassen(X, Y):
    """Use Strassen's algorithm to compute X*Y in sub O(n^3) time

    :X: Square matrix of size N*N
    :Y: Square matrix of size N*N
    :returns: Product X*Y

    """

    sideLen = X.shape[0]
    halfLen = sideLen / 2

    if sideLen == 1:
        Z = X * Y
    else:
        A = X[:halfLen, :halfLen]
        B = X[:halfLen, halfLen:]
        C = X[halfLen:, :halfLen]
        D = X[halfLen:, halfLen:]

        E = Y[:halfLen, :halfLen]
        F = Y[:halfLen, halfLen:]
        G = Y[halfLen:, :halfLen]
        H = Y[halfLen:, halfLen:]

        P1 = Strassen(A, F - H)
        P2 = Strassen(A + B, H)
        P3 = Strassen(C + D, E)
        P4 = Strassen(D, G - E)
        P5 = Strassen(A + D, E + H)
        P6 = Strassen(B - D, G + H)
        P7 = Strassen(A - C, E + F)

        Ztop = np.hstack((P5 + P4 - P2 + P6, P1 + P2))
        Zbottom = np.hstack((P3 + P4, P1 + P5 - P3 - P7))
        Z = np.vstack((Ztop, Zbottom))

    return Z


def validInput():
    """Checks input and returns two square matrices if possible.

    :returns: Two square matrices as numpy objects.

    """

    parser = argparse.ArgumentParser(
        'Multiply two matrices of identical size using Strassen\'s algorithm')
    parser.add_argument('-X', type=float, nargs='+',
                        help='List the elements for a square matrix in row-major order.')
    parser.add_argument('-Y', type=float, nargs='+')

    args = parser.parse_args()

    lenX = len(args.X)
    lenY = len(args.Y)

    try:
        assert (lenX == lenY)
    except (AssertionError):
        print ('Arguments -X and -Y must receive the same square number of inputs.')
        raise

    sqrtA = np.sqrt(lenX)

    try:
        X = np.reshape(args.X, (sqrtA, sqrtA))
        Y = np.reshape(args.Y, (sqrtA, sqrtA))
    except ValueError:
        print ('Arguments -X and -Y must receive the same square number of inputs.')
        raise

    return X, Y

if __name__ == "__main__":
    X, Y = validInput()

    C = Strassen(X, Y)
    C_check = np.dot(X, Y)

    try:
        assert (np.array_equal(C, C_check))
    except AssertionError:
        print ('C=X*Y was calculated incorrectly by my Strassen function.')
        raise
    else:
        print ('Correct!')
