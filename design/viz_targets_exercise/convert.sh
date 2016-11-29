#!/bin/bash
# driver script to explain the command line arguments
perl convert.pl \
	-verbose \
	-tips tip_data.csv,tip_data_meta.csv \
	-nodes inode_data.csv,inode_data_meta.csv \
	-tree tree.nwk | xml_pp > annotated.xml
