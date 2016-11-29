#!/bin/bash
# driver script to explain the command line arguments
# This requires:
# from CPAN, XML::Twig, and github.com/rvosa/bio-phylo
perl convert.pl \
	-verbose \
	-tips tip_data.csv,tip_data_meta.csv \
	-nodes inode_data.csv,inode_data_meta.csv \
	-tree tree.nwk | xml_pp > annotated.xml
