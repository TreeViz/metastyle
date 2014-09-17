#! /usr/bin/env perl

use strict;
use warnings;
use Text::CSV;
use Data::Dumper;

#my $xmlfile=shift;
my $datatype='Species';

# Getopt::Long magic
my $data_filename = "mammal_genomes.csv";

my $csv = Text::CSV->new({ binary => 1 });

open(my $fh_data, "<:encoding(utf-8)", $data_filename) or die "Could not open '$data_filename': $!";
$csv->column_names($csv->getline($fh_data));

while(my $row = $csv->getline_hr($fh_data)) {
    print $row->{$datatype} . " = " . Dumper($row) . "\n";
}

close($fh_data);
