#!usr/bin/env perl

use strict;
use warnings;
require "/Users/julieallen/code/phylostylotastic/converters/nexmlconverters.pl";

my $file=shift;
my $file2=shift;

newicktonexml($file);

#nexustonexml($file2);
