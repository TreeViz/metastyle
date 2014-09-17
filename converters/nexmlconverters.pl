use strict;
use warnings;
use Bio::Phylo::IO 'parse';


#### Newick to Nexml
sub newicktonexml {
    my $file = shift;
    my $outfile = $file.".NeXML";
    open(OUT,">$outfile");
    print OUT parse( '-format' => 'newick', '-file' => $file, '-as_project' => 1 )->to_xml;
    close OUT;
    return $outfile;
}

##### Nexus to Nexml
sub nexustonexml{
    my $file = shift;
    my $outfile = $file.".NeXML";
    open(OUT,">$outfile");
    print OUT parse( '-format' => 'nexus', '-file' => $file, '-as_project' => 1 )->to_xml;
    close OUT;
    return $outfile;
}

return 1;


