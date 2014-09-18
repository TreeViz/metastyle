from ete2 import Nexml, TreeStyle, NodeStyle
import argparse
import sys
import os

import phylostylotastic.parser

argparser = argparse.ArgumentParser(
    description='Produce publication-quality phylogenetic trees using NexSS stylesheets'
)
argparser.add_argument(
    'source',
    nargs=1,
    help='Input NeXML file to process'
)
argparser.add_argument(
    'stylesheet',
    nargs='*',
    help='NexSS stylesheet to format the NeXML file with'
)
argparser.add_argument(
    '-o', '--output',
    nargs=1,
    default='output.svg',
    help='The name of the output file. Must have a .svg, .png or .pdf extension.'
)
argparser.add_argument(
    '-ow', '--width',
    nargs=1,
    default=[None],
    type=int,
    help='The width of the output image'
)
argparser.add_argument(
    '-oh', '--height',
    nargs=1,
    default=[None],
    type=int,
    help='The height of the output image'
)
argparser.add_argument(
    '--dpi',
    nargs=1,
    default=[300],
    type=int,
    help='The dots-per-inch (DPI) in the output file.'
)
args = argparser.parse_args()

# Change single-list items into single items.
args.output = args.output[0]
args.dpi = args.dpi[0]
args.width = args.width[0]
args.height = args.height[0]

nexml = Nexml()
nexml.build_from_file(sys.argv[1])

def build_tree_style(tree):
    # use our simple TSS cascade to prepare an ETE TreeStyle object
    sheets = gather_tss_stylesheets(tree)
    if len(sheets) == 0:
        return None

    # Some styles can be applied to the entire tree
    ts = TreeStyle()
    # For nodes (and other elements?), build an ordered set of TSS rules 
    # to apply to each element in our layout function
    node_rules = []

    for s in sheets:
        ts, tss_cascade = phylostylotastic.parser.apply_stylesheet(
            stylesheet=s, 
            tree_style=ts,
            node_rules=node_rules)

    # apply this layout function to each node as it's rendered
    ts.layout_fn = phylostylotastic.parser.apply_tss
    return ts

def gather_tss_stylesheets(tree):
    sheets = []
    # if a stylesheet was provided, this is all we should use
    if args.stylesheet:
        sheets.extend(args.stylesheet)
        return sheets

    # TODO: add any default stylesheet for this tool?

    # add any linked stylesheets in the NeXML file
    # add any embedded stylesheets in the NeXML file
    nexml_doc = tree.nexml_project
    if nexml_doc:
        # TODO: can we retrieve <?xml-stylesheet ... ?> elements?
        pass

    # TODO: add any linked stylesheets just for this tree

    # TODO: add any embedded stylesheets in this tree

    return sheets 



# Figure out the file basename in case we have multiple trees.
(output_basename, output_extension) = os.path.splitext(args.output)

# render a series of output files (one for each tree)
tree_index = 0
for trees in nexml.get_trees():
    for tree in trees.get_tree():
        tree_index += 1
        ts = build_tree_style(tree)

        # Only use suffixes if there is more than one tree.
        output_filename = "%s%s" % (output_basename, output_extension)
        if tree_index > 1:
            output_filename = "%s%d%s" % (output_basename, tree_index, output_extension)
        
        if args.width and args.height:
            tree.render(output_filename, tree_style=ts, w=args.width, h=args.height, dpi=args.dpi)
        elif args.width:
            tree.render(output_filename, tree_style=ts, w=args.width, dpi=args.dpi)
        elif args.height:
            tree.render(output_filename, tree_style=ts, h=args.height, dpi=args.dpi)
        else:
            tree.render(output_filename, tree_style=ts, dpi=args.dpi)

        # let's try the interactive QT viewer
        tree.show(tree_style=ts)

