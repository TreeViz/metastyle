from ete2 import Nexml
import sys

if len(sys.argv) < 2:
    print("Command line argument required: NeXML file")
    exit(-1)

nexml = Nexml()
nexml.build_from_file(sys.argv[1])

# render a series of SVG files (one for each tree)
for trees in nexml.get_trees():
    tree_index = 0
    for tree in trees.get_tree():
        tree_index += 1
        tree.render("output%d.svg" % tree_index)
	# let's try the interactive QT viewer
        tree.show()
