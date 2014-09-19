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
argparser.add_argument(
    '--all', '-a',
    action='store_true',
    dest='flag_all',
    help='Display every annotation'
)
argparser.add_argument(
    '--fullnames', '-fn',
    action='store_true',
    dest='flag_fullnames',
    help='Display full(y resolved) names for properties'
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
    node_id = str(node.__class__.__name__) + " " + node.oid

    # print " - annotations: %d" % len(node.annotations)

    for annotation in node.annotations:
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

        for node in tree.nodes():
            search_for_meta_nodes(node)

# Display everything.
property_values = dict()
property_types = dict()

def record_property(name, value, proptype):
    if name not in property_values:
        property_values[name] = dict()
    if value not in property_values[name]:
        property_values[name][value] = 0
    property_values[name][value] += 1

    if name not in property_types:
        property_types[name] = dict()
    if proptype is not None:
        if proptype not in property_types[name]:
            property_types[name][proptype] = 0
        property_types[name][proptype] += 1

# Process every record.
for node_id in metadata_order:
    if args.flag_all:
        print(" - " + node_id)

    for meta in metadata[node_id]:
        name = meta.prefixed_name
        if args.flag_fullnames:
            name = meta.namespace + meta.name

        record_property(name, meta.value, meta.datatype_hint)
        if args.flag_all:
            print("    - %s: %s (%s)" % (name, meta.value, meta.datatype_hint))
    if args.flag_all:
        print("")

# Display summary.
print("Metadata summary:")
for pname in property_values.keys():
    types = property_types[pname].keys()
    if len(types) == 0:
        types = ['no type information']

    values = sorted(property_values[pname].keys(), key=lambda k: property_values[pname][k], reverse = True)

    print(" - " + pname + " (" + ', '.join(sorted(types)) + "): ")

    count = 0
    count_unique = 0
    count_entries = 0
    for value in values:

        display_value = value
        if display_value is None or display_value.strip() == "":
            display_value = "(blank)"

        count += 1
        if count <= 10:
            print("    - " + display_value + " [%d]" % (property_values[pname][value]))
        elif count == len(values):
            print("    ... (%d entries with %d unique values)" % (count_entries, count_unique))
            print("    - " + display_value + " [%d]" % (property_values[pname][value]))
        else:
            count_unique += 1
            count_entries += property_values[pname][value]

    print("")

