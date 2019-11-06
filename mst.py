#!/usr/bin/env python3

import sys


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

if len(sys.argv) < 2:
    print("Usage: %s <file> [-e]" % sys.argv[0])
    exit(1)

print_edges = len(sys.argv) > 2 and sys.argv[2] == "-e"

edges = list()
with open(sys.argv[1]) as infile:
    # The first line tells how many nodes are in the graph.
    num_nodes = int(infile.readline())
    nodes = [list()] * num_nodes

    # Now read lines until the line is empty.
    line = infile.readline().strip()
    while line:
        node1, node2, cost = (int(x) for x in line.split(" "))
        nodes[node1].append((node2, cost))
        nodes[node2].append((node1, cost))
        edges.append((node1, node2, cost))
        line = infile.readline().strip()

t = kruskal_mst(num_nodes, edges)
print(sum(e[2] for e in t))
if print_edges:
    for e in t:
        print("%i %i %i" % e)
t = prim_mst(num_nodes, edges)
print(sum(e[2] for e in t))
if print_edges:
    for e in t:
        print("%i %i %i" % e)
