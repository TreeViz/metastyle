#
# Displays all the metadata contained in a file that PhyloStyloTastic can
# see or render.
# 

import ete2
from pprint import pprint
import argparse
import sys
import os

argparser = argparse.ArgumentParser(
    description='Display all the metadata contained in a file that PhyloStyloTastic can see or render'
)
argparser.add_argument(
    'source',
    nargs=1,
    help='Input NeXML file to process'
)
args = argparser.parse_args()

# Load NeXML files.
nexml = ete2.Nexml()
nexml.build_from_file(args.source[0])

# Go through the entire DOM, looking for Meta objects, and display them.
def displayMeta(parent, meta):
    print("parent = " + str(parent) + ", meta = " + str(meta));

def recurse(node):
    try:
        for meta in node.get_meta():
            displayMeta(node, meta)
    except AttributeError:
        pass

    try:
        for child in node:
            recurse(child)
    except TypeError:
        pass

recurse(nexml)
for trees in nexml.get_trees():
    for tree in trees.get_tree():
        recurse(tree)
