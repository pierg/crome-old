#!/usr/bin/env python3

# This file is part of the Simple LTL model-checker project
# see https://github.com/fredher/simple-ltl-model-checker

import sys

import pygraphviz as pgv
import spot
from buddy import bdd_ithvar, bddtrue

"""
The input file should follow the graphviz DOT file format. Nodes may have
attributes:
- 'initial' (with any non-empty value) if the node is initial. The model should
  specify exactly one initial node
- 'labels' (non-empty comma-separated list of strings) defines the list of
  atomic propositions that label the node
"""


def extract_node_str_labels(n):
    """Extract the set of string labels from node n (attribute labels)"""
    labels = set()
    for label in n.attr["label"].split(","):
        if label != "":
            labels.add(label)
    return labels


def extract_nodes_str_labels(G):
    """Extract the set of string labels from all nodes in graph G (attribute
    labels on nodes in G)"""
    labels = set()
    for n in G.nodes():
        labels = labels.union(extract_node_str_labels(n))
    return labels


def extract_initial_node(G):
    """Extract initial node from graph G (attribute initial on nodes in G)"""
    initial_node_name = ""
    for n in G.nodes():
        if n.attr["initial"] != "":
            if initial_node_name != "":
                raise "Multiple initial states are not allowed"
            initial_node_name = n
    if initial_node_name == "":
        raise "One initial state must be defined"
    return initial_node_name


def node_AP_formula_bdd(n, AP):
    """Build formula of atomic formula for node n over set of atomic
    propositions AP."""
    n_labels = extract_node_str_labels(n)
    f = bddtrue
    for l in AP:
        if l in n_labels:
            f = f & AP[l]
        else:
            f = f & -AP[l]
    return f


def dot_model_to_kripke(file, bdddict):
    """Create a Kripke structure from a DOT file.

    Nodes may have attributes: 'initial' (with any non-empty value) if
    the node is initial, and 'labels' (comma-separated list of strings)
    to define atomic propositions labeling the node
    """
    k = spot.make_kripke_graph(bdddict)
    G = pgv.AGraph(string=file)
    # Extract node labels in G
    G_labels = extract_nodes_str_labels(G)
    # Declare atomic propositions
    AP = {}
    for l in G_labels:
        AP[l] = bdd_ithvar(k.register_ap(l))
    # Declare nodes
    k_nodes = {}
    node_names = []
    for n in G.nodes():
        f = node_AP_formula_bdd(n, AP)
        k_nodes[n] = k.new_state(f)
        node_names = node_names + [n]
    k.set_state_names(node_names)
    # Declare initial node
    initial_node = G.nodes()[0]
    k.set_init_state(k_nodes[initial_node])
    # Declare transitions
    for (src, tgt) in G.edges():
        k.new_edge(k_nodes[src], k_nodes[tgt])
    return k


def build_automaton(formula, bdddict):
    """Build a Büchi automaton that accepts all words satisfying formula, using
    dictionary bdddict."""
    af = spot.translate(formula, dict=bdddict)
    return af


def model_check(k, formula, bdddict):
    """model-check Kripke structure k w.r.t.

    LTL formula using BDD dictionary bdddict
    """
    # Create the automaton for the negation of the formula
    neg_formula = "!(" + formula + ")"
    a_neg_formula = build_automaton(neg_formula, d)
    # Compute the product
    product = spot.otf_product(k, a_neg_formula)
    # Check emptiness of the product
    run = product.accepting_run()
    return (a_neg_formula, product, run)


def write_to_file(filename, str):
    """Write string str to file filename."""
    try:
        f = open(filename, "w")
        f.write(str)
        f.close()
    except:
        print("ERROR, writing to file", filename, "failed")
        sys.exit()


if __name__ == "__main__":
    dot = 'graph EXPR { rankdir=BT; n105553119578400 [label="~z",shape=box]; n105553119578080 [label="adde6",shape=box]; n105553119577312 [label="adaed",shape=box]; n105553119578656 [label="a90d3",shape=box]; n105553119578112 [label="af97d",shape=box]; n105553119578848 [label=or,shape=circle]; n105553119577888 [label="a9e5e",shape=box]; n105553119577216 [label="a11bc",shape=box]; n105553119578016 [label=and,shape=circle]; n105553119578752 [label="a9e3e",shape=box]; n105553119578784 [label="ac643",shape=box]; n105553119578176 [label=and,shape=circle]; n105553119578464 [label=or,shape=circle]; n105553119578688 [label=and,shape=circle]; n105553119578656 -- n105553119578848; n105553119578112 -- n105553119578848; n105553119577888 -- n105553119578016; n105553119577216 -- n105553119578016; n105553119578752 -- n105553119578176; n105553119578784 -- n105553119578176; n105553119578016 -- n105553119578464; n105553119578176 -- n105553119578464; n105553119578400 -- n105553119578688; n105553119578080 -- n105553119578688; n105553119577312 -- n105553119578688; n105553119578848 -- n105553119578688; n105553119578464 -- n105553119578688; }'

    bdd = spot.make_bdd_dict()
    k = dot_model_to_kripke(dot, bdd)
    print(k)

    print("Ciao")
