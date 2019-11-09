#!/usr/bin/env python3

import sys
import time


def kruskal_mst(num_nodes, edges):
    # Sort the edges.
    edges = sorted(edges, key=lambda e: e[2])

    # Create an empty set.
    t = set()

    # Put each node in its own component.
    num_components = num_nodes
    components = [{i} for i in range(num_nodes)]

    while num_components >= 2:
        edge = edges.pop(0)
        node1, node2, _ = edge
        if components[node1] != components[node2]:
            t.add(edge)
            set2 = components[node2]
            for node in set2:
                components[node] = components[node1]
            components[node1].update(set2)
            num_components -= 1

    return t

def prim_mst(num_nodes, edges):
    visited = [False] * num_nodes
    visited[0] = True
    num_unvisited = num_nodes - 1

    t = set()

    while num_unvisited > 0:
        lowest = min((e for e in edges if visited[e[0]] ==
                (not visited[e[1]])), key=lambda e: e[2])
        t.add(lowest)
        if not visited[lowest[0]]:
            visited[lowest[0]] = True
            num_unvisited -= 1
        elif not visited[lowest[1]]:
            visited[lowest[1]] = True
            num_unvisited -= 1
        else:
            raise RuntimeError("This shouldn't happen")

    return t

def do_mst(proc, num_nodes, edges, print_edges):
    start_time = time.time()
    t = proc(num_nodes, edges)
    end_time = time.time()

    cost = sum(e[2] for e in t)

    print("  Execution time: %fs" % (end_time - start_time))
    print("  MST cost: %i" % cost)

    if print_edges:
        print("  Edges:")
        for e in sorted(t):
            print("    %i %i (cost %i)" % e)

if len(sys.argv) < 2:
    print("Usage: %s <file> [-e]" % sys.argv[0])
    exit(1)

print_edges = len(sys.argv) > 2 and sys.argv[2] == "-e"

edges = list()
with open(sys.argv[1]) as infile:
    # The first line tells how many nodes are in the graph.
    num_nodes = int(infile.readline())

    # Now read lines until the line is empty.
    line = infile.readline().strip()
    while line:
        node1, node2, cost = (int(x) for x in line.split(" "))
        edges.append((node1, node2, cost))
        line = infile.readline().strip()

print("Kruskal's algorithm:")
do_mst(kruskal_mst, num_nodes, edges, print_edges)

print("Prim's algorithm:")
do_mst(prim_mst, num_nodes, edges, print_edges)
