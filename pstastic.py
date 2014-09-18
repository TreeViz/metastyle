from ete2 import Nexml, TreeStyle, NodeStyle, TextFace
from ete2 import add_face_to_node
from pprint import pprint
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
        ts, tss_cascade = apply_stylesheet(
            stylesheet=s, 
            tree_style=ts,
            node_rules=node_rules)

    # Use a layout function to test each node against TSS selectors?
    def apply_tss(node):
        node_style = NodeStyle()

        # gather label text and styles separately; we'll need to add this 
        # using a TextFace after all styles have been considered
        label_specs = {}
        label_specs['text'] = get_proper_node_label(node)

        for rule in node_rules:
            # Test this node against each selector
            if test_node_against_selector(node, rule.selector):
                node_style, node = apply_node_rule(rule, node_style, node, label_specs)
        node.set_style(node_style);

        # assign the final label with appropriate style
        if node.is_leaf():
            label_face = TextFace(**label_specs)
            node.add_face(label_face, 0)
        
        return node

    # apply this layout function to each node as it's rendered
    ts.layout_fn = apply_tss
    # suppress default node-labeling behavior (so we can style labels!)
    ts.show_leaf_name = False
    return ts

def get_proper_node_label(node):
    # TODO: Always resolve from OTUs? or use "natural" labels or IDs?
    return node.name

def test_node_against_selector(node, selector):
    # Interpret a selector in the context of a live tree (vs. a DOM)
    # and return True if this node matches (or False). 
    #
    # We'll optimistically hope that this node is a match, but walk 
    # the series of tokens looking for a reason to fail it.
    ##pprint("TESTING SELECTOR %s" % selector.as_css())

    # keep track of the most recently specified context element(s), since we
    # will often test their properties
    context_elements = [ node.get_tree_root() ]

    # wait for descendant name after a whitespace token
    waiting_for_descendant_element_name = True

    # wait for a class (attribute) name after a '.' token
    waiting_for_class_name = False

    for token in selector:
        if token.type == u'S':  # string
            # ASSUME this is whitespace?
            waiting_for_descendant_element_name = True
            waiting_for_class_name = False

        elif token.type == u'IDENT': # element or classname
            if waiting_for_descendant_element_name:
                if token.value == 'node':
                    # gather all descendant nodes
                    new_context_elements = []
                    for e in context_elements:
                        new_context_elements.extend(e.get_descendants())
                    context_elements = new_context_elements
                elif token.value in TREE_ONLY_SELECTOR_TOKENS:
                    # respect these and apply font styles, etc
                    pass
                else:
                    # fail on other element names for now
                    report_unsupported_element_selector(token.value)
                    context_elements = []
            elif waiting_for_class_name:
                # test for matching classname
                new_context_elements = []
                for e in context_elements:
                    if e.nexml_node.anyAttributes_.has_key( 'class'):
                        if e.nexml_node.anyAttributes_['class'] == token.value:
                            new_context_elements.append(e)
                context_elements = new_context_elements
            else:
                print("Unexpected IDENT in selector: %s" % token.value)

        elif token.type == u'[': # property test
            # compare this property or metadata
            context_elements = [e for e in context_elements 
                if compare_property(e,token)]
            
            pass

        elif token.type == u'DELIM':
            if token.value == '.':
                waiting_for_class_name = True
                waiting_for_descendant_element_name = False
            else:
                print("Unsupported DELIM in selector: %s" % token.value)

        else:
            print("Unexpected token type (%s) in selector: %s" % 
                (token.type, token.value))

        if len(context_elements) == 0:
            ##pprint("No more context_elements after token: %s" % token)
            return False
        else: 
            ##pprint("%i context_elements, after token: %s" % (len(context_elements), token,))
            pass
    
    # check to see if this node is (or is descended from) the final context_elements
    if node in context_elements:
        return True
    for test_ancestor in node.get_ancestors():
        if test_ancestor in context_elements:
            return True
    return False


TREE_ONLY_SELECTOR_TOKENS = ("figure","tree","scale",)
TREE_STYLE_PROPERTIES = ("layout","border","scaled","visible",)
# See the full list at 
# http://pythonhosted.org/ete2/reference/reference_treeview.html#treestyle

NODE_STYLE_PROPERTIES = ("color","background-color","size","shape","border","font",)
# See the full list at 
# http://pythonhosted.org/ete2/reference/reference_treeview.html#ete2.NodeStyle


# Report unsupported style properties, etc. *just once*

unsupported_tree_styles = []
def report_unsupported_tree_style(name):
    if name not in unsupported_tree_styles:
        print("ETE TreeStyle does not provide '%s'" % name)
        unsupported_tree_styles.append(name)

unsupported_node_styles = []
def report_unsupported_node_style(name):
    if name not in unsupported_node_styles:
        print("ETE NodeStyle does not provide '%s'" % name)
        unsupported_node_styles.append(name)

unsupported_element_selectors = []
def report_unsupported_element_selector(name):
    if name not in unsupported_element_selectors:
        print("ETE does not support element selector '%s'" % name)
        unsupported_element_selectors.append(name)

def apply_node_rule(rule, node_style, node, label_specs):
    for style in rule.declarations:
        # N.B. name is always normalized lower-case
        # Translate TSS/CSS property names into ETE properties
        if style.name not in NODE_STYLE_PROPERTIES:
            report_unsupported_node_style(style.name)
            continue

        # TODO: handle dynamic (data-driven) values in all cases!
        if style.name == "color":
            node_style["fgcolor"] = style.value.as_css()
            # apply this with label text! but how to retrieve it?
            label_specs['fgcolor'] = style.value.as_css()
        elif style.name == "background-color":
            node_style["bgcolor"] = style.value.as_css()
        elif style.name == "border":
            # for now, apply these styles to vertical edges only
            # TODO: revisit our expectations, and possibly more tree-wise property names

            # examine value, apply any/all styles found
            for a_value in style.value:
                if a_value.type == u'DIMENSION':
                    # disregard units for now (TODO)
                    node_style["hz_line_width"] = a_value.value
                elif a_value.type == u'S':
                    # assume this is whitespace, ignore it
                    pass
                elif a_value.type == u'IDENT':
                    # ETE offers just a few line types: 0 solid, 1 dashed, 2 dotted
                    if a_value.value == 'solid':
                        node_style["hz_line_type"] = 0
                    elif a_value.value == 'dashed':
                        node_style["hz_line_type"] = 1
                    elif a_value.value == 'dotted':
                        node_style["hz_line_type"] = 2
                    else:
                        # apply as a color, and hope for the best
                        node_style["hz_line_color"] = a_value.value
                        node_style["vt_line_color"] = a_value.value
        elif style.name == "font":
            # examine value, apply any/all styles found
            for a_value in style.value:
                if a_value.type == u'DIMENSION':
                    # disregard units for now (TODO)
                    label_specs['fsize'] = a_value.value
                elif a_value.type == u'S':
                    # assume this is whitespace, ignore it
                    pass
                elif a_value.type == u'IDENT':
                    # apply as a font name and hope for the best
                    label_specs['ftype'] = a_value.value
                    # TODO: expect color names here as well?
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
            if r.selector.as_css() in TREE_ONLY_SELECTOR_TOKENS:
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
                    elif style.name == "border":
                        # crappy support for this
                        its_value = style.value.as_css()
                        if its_value == "none":
                            tree_style.show_border = False
                        else:
                            tree_style.show_border = True
                    elif style.name == "scaled":
                        # determines whether we show branch lengths or not
                        its_value = style.value.as_css()
                        if its_value == "true":
                            tree_style.force_topology = False
                        else:
                            # show all branches as equal length
                            tree_style.force_topology = True
                    elif r.selector.as_css() == 'scale' and style.name == "visible":
                        its_value = style.value.as_css()
                        if its_value == "false":
                            tree_style.show_scale = False
                        else:
                            tree_style.show_scale = True
                    else:
                        setattr(tree_style, style.name, style.value.as_css())

            #tree_style.mode = 'c'  # circular
            #tree_style.show_leaf_name = False
            #tree_style.show_branch_length = True
                
    return tree_style, node_rules
        
def compare_property(element, test_container):
    # Split this token to get property name, operator, and value;
    # compare to this element's properties (including typical
    # metadata) and return the result
    
    # find the operator (DELIM) and concat the rest
    test_property = ''
    test_operator = None
    test_value = None
    test_value_type = "string"
    for token in test_container.content:
        if token.type == u'DELIM':
            if test_operator is None:
                test_operator = token.value
            else:
                # keep adding to the operator (concatenate things like '>=')
                test_operator = "%s%s" % (test_operator, token.value,)
        elif test_operator is None:
            # keep adding to the property name
            test_property = "%s%s" % (test_property, token.value,)
        else:
            if test_value is None:
                test_value = token.value
                test_value_type = token.type
            else:
                # keep adding to the test value (ASSUMES a string)
                test_value = "%s%s" % (test_value, token.value,)
                test_value_type = u"CONCAT_STRING"
        
    el_value = get_property_or_meta(element, test_property)

    if el_value is None:
        return False
    else:
        if test_operator is None:
            # match on the mere existence of this property
            return True
        else:

            ##pprint("%s - %s" % (test_value_type, test_value,))
            # convert strings as needed for comparison
            if test_value_type == u'INTEGER':
                try:
                    recast_value = int(el_value)
                    el_value = recast_value
                except ValueError:
                    try:
                        recast_value = float(el_value)
                        el_value = recast_value
                    except ValueError:
                        print("Expected an integer, but found %s" % el_value);
            elif test_value_type == u'NUMBER':  # a fractional number like 0.45
                try:
                    recast_value = float(el_value)
                    el_value = recast_value
                except ValueError:
                    print("Expected a float, but found %s" % el_value);
            else:  # u'INDENT', u'CONCAT_STRING' should remain as strings
                # TODO: special handling for boolean IDENT (true)?
                pass

            # use the operator and value to work it out
            if test_operator == '=':
                # test for equality
                return el_value == test_value
            elif test_operator == '!=':
                # test for inequality
                return el_value != test_value
            # value comparisons (alpha, numeric?)
            elif test_operator == '>':
                return el_value > test_value
            elif test_operator == '<':
                return el_value < test_value
            elif test_operator == '>=':
                return el_value >= test_value
            elif test_operator == '<=':
                return el_value <= test_value
            # string comparisons (startswith, endswith, anywhere)
            elif test_operator == '^=':
                return el_value.startswith(test_value)
            elif test_operator == '$=':
                return el_value.endswith(test_value)
            elif test_operator == '*=':
                return el_value.find(test_value) != -1

def get_property_or_meta(element, property_name):
    # check first for an attribute by this name
    if getattr(element, property_name, None):
        return getattr(element, property_name, None)
    # ...then for a child META element
    for metatag in element.nexml_node.meta:
        # ASSUMES there's just one matching metatag!
        if metatag.property == property_name:
            # TODO: normalize to lower-case?
            return metatag.content
    # TODO: ...finally, check for a distant META tag that 
    # points to this element?
    return None

# Figure out the file basename in case we have multiple trees.
(output_basename, output_extension) = os.path.splitext(args.output)

# render a series of output files (one for each tree)
tree_index = 0
for trees in nexml.get_trees():
    for tree in trees.get_tree():
        tree_index += 1
        ts = build_tree_style(tree)

        # let's try the interactive QT viewer
        tree.show(tree_style=ts)
        
        # BEWARE! Each time we call .render() or .show(), new labels will be created :-/
        ##tree.show(tree_style=ts)

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

