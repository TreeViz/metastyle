from ete2 import Nexml, TreeStyle, NodeStyle

import argparse
import tinycss
import sys
import os

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
    nargs='?',
    default='output.svg',
    help='The name of the output file. Must have a .svg, .png or .pdf extension.'
)
args = argparser.parse_args()

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
        ts, tss_cascade = apply_stylesheet(
            stylesheet=s, 
            tree_style=ts,
            node_rules=node_rules)

    # Use a layout function to test each node against TSS selectors?
    def apply_tss(node):
        node_style = NodeStyle()
        for rule in node_rules:
            # Test this node against each selector
            if test_node_against_selector(node, rule.selector):
                node_style, node = apply_node_rule(rule, node_style, node)
        node.set_style(node_style);
        return node

    # apply this layout function to each node as it's rendered
    ts.layout_fn = apply_tss
    return ts

def test_node_against_selector(node, selector):
    # TODO: Here we can interpret our selectors 
    # in the context of a live tree (vs. a DOM)
    return True

TREE_STYLE_PROPERTIES = ("layout",)
# See the full list at 
# http://pythonhosted.org/ete2/reference/reference_treeview.html#treestyle

NODE_STYLE_PROPERTIES = ("color", "background-color", "size", "shape",)
# See the full list at 
# http://pythonhosted.org/ete2/reference/reference_treeview.html#ete2.NodeStyle


# Report unsupported style properties *just once*
unsupported_tree_styles = []
def report_unsupported_tree_style(name):
    if name not in unsupported_tree_styles:
        print("ETE does not support '%s' in TreeStyle" % name)
        unsupported_tree_styles.append(name)

unsupported_node_styles = []
def report_unsupported_node_style(name):
    if name not in unsupported_node_styles:
        print("ETE does not support '%s' in NodeStyle" % name)
        unsupported_node_styles.append(name)


def apply_node_rule(rule, node_style, node):
    for style in rule.declarations:
        # N.B. name is always normalized lower-case
        # Translate TSS/CSS property names into ETE properties
        if style.name not in NODE_STYLE_PROPERTIES:
            report_unsupported_node_style(style.name)
            continue

        # TODO: handle dynamic (data-driven) values in all cases!
        if style.name == "color":
            node_style["fgcolor"] = style.value.as_css()
        elif style.name == "background-color":
            node_style["bgcolor"] = style.value.as_css()
        else:
            # by default, use the same name as in TSS
            try:
                setattr(node_style, style.name, style.value.as_css())
            except:
                print("Invalid property for node: %s" % style.name);
                pass

        # TODO: consider style.priority? ('important')

    # node_style["shape"] = "sphere"
    # node_style["hz_line_type"] = 2
    # node_style["hz_line_color"] = "#cc99cc"
    # node_style["size"] = 10

    return node_style, node

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

# Apply styles to an existing TreeStyle object and return it
def apply_stylesheet(stylesheet, tree_style, node_rules):
    if (not stylesheet):
        print("Missing stylesheet!")
        return tree_style, node_rules
    if (not tree_style):
        print("Missing tree_style!")
        return None, None

    # parse the TSS from its CSS-style syntax
    parser = tinycss.make_parser('page3')
    # load the stylesheet using its path+filename
    stylesheet = os.path.abspath(stylesheet)
    style = parser.parse_stylesheet_file(css_file=stylesheet)
    print("Found %i rules, %i errors" % 
       (len(style.rules),len(style.errors)))
    if len(style.errors) > 0:
        for e in style.errors:
            print(e)

    # walk the TSS rules and translate them into TreeStyle properties
    # or add them to the node_rules collection
    for r in style.rules:
        if r.at_keyword:
            # this is an ImportRule, MediaRule, or the like
            # TODO: support @import, etc?
            print("Unsupported at-rule:")
            print(r)
        else:
            # it's a normal CSS RuleSet
            #print("TSS RuleSet:")
            #print("  selector: %s" % r.selector.as_css())
            #print("  as list:  %s" % repr(r.selector))
            #print("  declarations: %s" % r.declarations)

            # add every rule to node tests 
            node_rules.append(r)

            # TODO: interpret its selector to find targets
            # see https://pythonhosted.org/tinycss/parsing.html

            # Some rules should modify the current TreeStyle
            if r.selector.as_css() in ("canvas", "tree", "scale"):
                for style in r.declarations:
                    if style.name not in TREE_STYLE_PROPERTIES:
                        report_unsupported_tree_style(style.name)
                        continue
                    if style.name == "layout":
                        its_value = style.value.as_css()
                        if its_value == "rectangular":
                            tree_style.mode = "r"
                        elif its_value == "circular":
                            tree_style.mode = "c"
                    else:
                        setattr(tree_style, style.name, style.value.as_css())

            #tree_style.mode = 'c'  # circular
            #tree_style.show_leaf_name = False
            #tree_style.show_branch_length = True
                
    return tree_style, node_rules
        
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
        
        tree.render(output_filename, tree_style=ts)

        # let's try the interactive QT viewer
        tree.show(tree_style=ts)

