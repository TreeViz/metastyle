from ete2 import Nexml, TreeStyle
import sys

if len(sys.argv) < 2:
    print("Command line argument required: NeXML file")
    exit(-1)

custom_stylesheet = None
if len(sys.argv) > 2:
    if sys.argv[2]:
        custom_stylesheet = sys.argv[2]
    
nexml = Nexml()
nexml.build_from_file(sys.argv[1])

def build_tree_style(tree):
    # use our simple TSS cascade to prepare an ETE TreeStyle object
    ##import pdb; pdb.set_trace()
    sheets = gather_tss_stylesheets(tree)
    if len(sheets) == 0:
        return None
    ts = TreeStyle()
    for s in sheets:
        ts = apply_stylesheet(stylesheet=s, tree_style=ts)
    return ts

def gather_tss_stylesheets(tree):
    sheets = []
    # if a stylesheet was provided, this is all we should use
    if custom_stylesheet:
        sheets.append(custom_stylesheet)
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

# Apply styles to an existing TreeStyle object and return it
def apply_stylesheet(stylesheet, tree_style):
    if (not stylesheet):
        print("Missing stylesheet!")
        return tree_style
    if (not tree_style):
        print("Missing tree_style!")
        return None
    # TODO: load the stylesheet using path+filename
    # TODO: parse the TSS from its CSS-style syntax
    tss = """node {color: red;}"""

    # walk the TSS rules and translate them into TreeStyle properties
    tree_style.mode = 'c'  # circular
    tree_style.show_leaf_name = False
    tree_style.show_branch_length = True
    return tree_style

# render a series of SVG files (one for each tree)
for trees in nexml.get_trees():
    tree_index = 0
    for tree in trees.get_tree():
        tree_index += 1
        ts = build_tree_style(tree)
        tree.render("output%d.svg" % tree_index, tree_style=ts)
        # let's try the interactive QT viewer
        tree.show(tree_style=ts)



