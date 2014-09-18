use warnings;
use strict;

my $csv = $ARGV[0];
my $xml = $ARGV[1];
my $outfile = $xml.".meta.NeXML";
open(CSV,$csv);
my @meta=<CSV>;
open(NeXML,$xml);
my @nexml=<NeXML>;
chomp($meta[0]);
my @type=split(",",$meta[0]);
shift(@meta);
my %meta_size;
foreach(@meta){
	my @data=split(",",$_);
	my $size=$data[4];
	my $label=$data[0];
	$meta_size{$label}=$size;	
}

open(metaNeXML,">$outfile");
foreach(@nexml){
	if($_=~/<otu id\=.*?label="(.*?)"/g){
		my $otu=$1;
		print metaNeXML $_;
		print metaNeXML "\t\t<meta xsi:type=\"$type[4]\" property=\"external:data\" content=\"$meta_size{$otu}\"/>\n";
	}else{
		print metaNeXML $_;
	}
}

