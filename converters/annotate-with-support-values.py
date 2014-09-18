#! /usr/bin/env python

###############################################################################
##
##  Copyright 2014 Jeet Sukumaran.
##
##  This program is free software; you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation; either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License along
##  with this program. If not, see <http://www.gnu.org/licenses/>.
##
###############################################################################

"""
This program does something.
"""

import sys
import os
import argparse
import dendropy

__prog__ = os.path.basename(__file__)
__version__ = "1.0.0"
__description__ = __doc__
__author__ = 'Jeet Sukumaran'
__copyright__ = 'Copyright (C) 2014 Jeet Sukumaran.'

def main():
    """
    Main CLI handler.
    """

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("input_file", metavar="FILEPATH", type=str)

    source_options = parser.add_argument_group("source options")
    source_options.add_argument("-f", "--from-format",
            type=str,
            metavar="SCHEMA",
            default="newick",
            choices=["nexus", "newick"],
            help="input data format: 'newick' or 'nexus' (default: '%(default)s')")
    source_options.add_argument("-s", "--support-values",
            type=str,
            default="labels",
            choices=["labels", "comment", "beast-posterior", "mrbayes-prob"],
            help="Source of support values in input tree(s) (default: '%(default)s')")
    source_options.add_argument("--preserve-undescores",
            action="store_true",
            default=False,
            help="By default, unprotected underscores get converted to spaces under standard NEWICK/NEXUS conventions. Set this flag to preserve unquoted underscores.")

    output_options = parser.add_argument_group("output options")

    output_options.add_argument("-o", "--output-filepath",
            action="store",
            type=str,
            default="-",
            metavar="FILEPATH",
            help="Name of output file (defaults to standard output)")

    args = parser.parse_args()

    if args.support_values == "beast-posterior" or args.support_values == "mrbayes-prob":
        extract_comment_metadata = True
    else:
        extract_comment_metadata = False
    tree = dendropy.Tree.get_from_path(
            args.input_file,
            args.from_format,
            extract_comment_metadata=extract_comment_metadata,
            suppress_internal_node_taxa=True)

    for node in tree:
        if args.support_values == "labels":
            if node.label is not None:
                try:
                    support_value = float(node.label)
                except ValueError:
                    support_value = None
            else:
                support_value = None
        elif args.support_values == "comment":
            try:
                support_value = float("".join(node.comments))
            except ValueError:
                support_value = None
        elif args.support_values == "beast-posterior":
            source_annote = node.annotations.find(name="posterior")
            if source_annote is not None:
                try:
                    support_value = float(source_annote.value)
                except ValueError:
                    support_value = None
            else:
                support_value = None
        elif args.support_values == "mrbayes-prob":
            source_annote = node.annotations.find(name="prob")
            if source_annote is not None:
                try:
                    support_value = float(source_annote.value)
                except ValueError:
                    support_value = None
            else:
                support_value = None
        else:
            raise ValueError(args.support_values)
        if support_value is not None:
            node.annotations.add_new("support", support_value)
    if args.output_filepath == "-":
        out = sys.stdout
    else:
        out = open(args.output_filepath, "w")
    with out:
        tree.write_to_stream(out, "nexml")


if __name__ == '__main__':
    main()


