from ete2 import Nexml, TreeStyle
import sys

if len(sys.argv) < 2:
    print("Command line argument required: NeXML file")
    exit(-1)

nexml = Nexml()
nexml.build_from_file(sys.argv[1])

def build_tree_style(tree):
    # use our simple TSS cascade to prepare an ETE TreeStyle object
    sheets = gather_tss_stylesheets(tree)
    if len(sheets) == 0:
        return None
    for s in sheets:
        ts = TreeStyle()
        return ts

def gather_tss_stylesheets(tree):
    return []

# render a series of SVG files (one for each tree)
for trees in nexml.get_trees():
    tree_index = 0
    for tree in trees.get_tree():
        tree_index += 1
        tree_style = build_tree_style(tree)
        tree.render("output%d.svg" % tree_index)
        # let's try the interactive QT viewer
        tree.show()



