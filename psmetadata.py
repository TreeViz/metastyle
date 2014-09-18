#
# Displays all the metadata contained in a NeXML file.
# 

import dendropy
from pprint import pprint
from StringIO import StringIO
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
ds = dendropy.DataSet.get_from_path(args.source[0], 'nexml', attach_taxon_set=True)

#
# SECTION 1: Look for Meta nodes (http://www.nexml.org/nexml/html/doc/schema-1/meta/annotations/#Meta)
# and display them.
#
metadata_order = []
metadata = dict()

def search_for_meta_nodes(node):
    # Check for meta elements and display them.
    for annotation in node.annotations:
        node_id = str(node.__class__.__name__) + " " + node.oid

        if node_id in metadata:
            metadata[node_id].append(annotation)
        else:
            metadata_order.append(node_id)
            metadata[node_id] = [annotation]

# Search for meta nodes on:
# - The top-level Nexml node.
search_for_meta_nodes(ds)

# - Each OTU.
for taxonsets in ds.taxon_sets:
    for taxon in taxonsets:
        search_for_meta_nodes(taxon)

# - Each trees and tree node.
for tree_list in ds.tree_lists:
    for tree in tree_list:
        search_for_meta_nodes(tree)

# Display everything.
property_names = []
property_values = dict()
property_types = dict()

def record_property(name, value, proptype):
    property_names.append(name)

    if name not in property_values:
        property_values[name] = dict()
    if value not in property_values[name]:
        property_values[name][value] = 0
    property_values[name][value] += 1

    if name not in property_types:
        property_types[name] = dict()
    if value not in property_types[name]:
        property_types[name][value] = 0
    property_types[name][value] += 1

for node_id in metadata_order:
    print(" - " + node_id)
    for meta in metadata[node_id]:
        record_property(meta.name, meta.value, meta.datatype_hint)
        print("    - %s: %s (%s)" % (meta.name, meta.value, meta.datatype_hint))

pprint(property_values)
