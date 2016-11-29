#!/bin/bash
# driver script to explain the command line arguments
# This requires:
# from CPAN, XML::Twig, and github.com/rvosa/bio-phylo
# note also the pipe through xml_pp, one of the optional
# scripts from XML::Twig that you should opt to install
perl convert.pl \
	-verbose \
	-tips tip_data.csv,tip_data_meta.csv \
	-nodes inode_data.csv,inode_data_meta.csv \
	-tree tree.nwk | xml_pp > annotated.xml
