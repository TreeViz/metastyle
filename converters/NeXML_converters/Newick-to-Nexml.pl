use strict;
use warnings;
use Bio::Phylo::IO 'parse';
my $file = $ARGV[0];
my $outfile = $file.".NeXML";
open(OUT,">$outfile");
print OUT parse( '-format' => 'newick', '-file' => $file, '-as_project' => 1 )->to_xml;