use warnings;
use strict;

my $csv = $ARGV[0];
my $xml = $ARGV[1];

open(CSV,$csv);
my @meta=<CSV>;
open(NeXML,$xml);
my @nexml=<NeXML>;
chomp($meta[0]);
my @type=split("\t",$meta[0]);

my $type1 = $type[1];
my $type2 = $type[2];
die "No type defined!" unless defined $type1;

shift(@meta);

my %meta_value;
my %meta_value2;

foreach(@meta){
    chomp;
    my @data=split(/\t{1}/);

    my $scname = $data[0];
    my $value=$data[1];
    $meta_value{lc $scname}=$data[1];
    $meta_value2{lc $scname}=$data[2];	

    print "($data[1])($data[2])\n";
}

my %otu_db;

foreach(@nexml){
	if(/<otu id="(.*?)" label="(.*?)"/i){
            $otu_db{$1} = $2;
        } 

        my $flag_printed = 0;
        if(/<node id="(.*?)" otu="(.*?)"\s*\/?>/i) {
            my $otu_id = $2;
            my $scname = $otu_db{$otu_id};
            my $value1 = $meta_value{lc $scname};
            my $value2 = $meta_value2{lc $scname};

            if(defined $value1) {
                s/\/>/>/g;
                print;
                print "\t\t<meta xsi:type=\"nex:LiteralMeta\" property=\"$type1\" content=\"$value1\" />\n";
                print "\t\t</node>\n";
                $flag_printed = 1;
            }

            if(defined $value2) {
                s/\/>/>/g;
                print;
                print "\t\t<meta xsi:type=\"nex:LiteralMeta\" property=\"$type2\" content=\"$value2\" />\n";
                print "\t\t</node>\n";
                $flag_printed = 1;
            }
 
        }

        print unless $flag_printed;
}

