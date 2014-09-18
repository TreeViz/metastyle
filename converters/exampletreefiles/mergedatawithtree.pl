#! /usr/bin/env perl

use strict;
use warnings;
use Text::CSV;
use Data::Dumper;
use Bio::Phylo
use Bio::NexmlIO


my $xmlfile='mammal_genomes.nwk.NeXML';
my $datatype='Size (Mb)';

# Getopt::Long magic
my $data_filename = "mammal_genomes.csv";

my $csv = Text::CSV->new({ binary => 1 });

open(my $fh_data, "<:encoding(utf-8)", $data_filename) or die "Could not open '$data_filename': $!";
$csv->column_names($csv->getline($fh_data));

my %genomehash=();
while(my $row = $csv->getline_hr($fh_data)) {
#    print $row->{$datatype} . " = " . Dumper($row) . "\n";
    $genomehash{$row ->{'species'}} = $row ->{'Size (Mb)'};
}

print "$genomehash{'Ursus maritimus'}\n";

close($fh_data);


my $in_nexml = Bio::NexmlIO->new(-file => 'nexml_doc.xml', -format => 'Nexml');



open FH, "<$xmlfile";
$xmlfile = s/.NeXML//g;
my $outfile = ">$xmlfile.annotated.NeXML";
open OUT ">$outfile";
while (<FH>) {
    if (/<otu\s+label="(.*?)"/) {
	my $species =$1;
	print OUT
	$species =~ s/_/ /g;
	print "$species\t$genomehash{$species}\n";
    }
}


#   <node id="node19" label="inodeABCDEF" root="true" about="uniquely_this_node19">
#        <meta property="cdao:has_Datum">
#          <meta typeof="cdao:CharacterStateDatum" rel="cdao:has_State" resource="#s1"/>
#        </meta>
