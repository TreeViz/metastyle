#!/usr/bin/perl
use strict;
use warnings;
use Text::CSV;
use File::Spec;
use Getopt::Long;
use Bio::Phylo::Factory;
use Bio::Phylo::IO 'parse_tree';
use Bio::Phylo::Util::Logger ':levels';

# will use this as the base URL for namespaces for the metadata CSV files
my $base_url = 'https://github.com/OpenTreeOfLife/phylostylotastic/tree/master/design/viz_targets_exercise';

# process command line arguments
my $verbosity = WARN;
my %arg = ( '-format' => 'newick', '-as_project' => 1 );
my ( @tip_data, @node_data, $tree );
GetOptions(
	'verbose+' => \$verbosity,
	'tips=s'   => sub { @tip_data = split /,/, pop },
	'nodes=s'  => sub { @node_data = split /,/, pop },
	'tree=s'   => sub { $tree = parse_tree( %arg, '-file' => pop ) },
);

# instantiate helper objects
my $fac = Bio::Phylo::Factory->new;
my $log = Bio::Phylo::Util::Logger->new( '-level' => $verbosity, '-class' => 'main' );

# build up the project
$log->info("Going to build up the data project");
my $taxa;
my $proj   = $fac->create_project;
my $forest = $fac->create_forest;
$forest->insert( $tree );
$proj->insert( $forest );
$proj->insert( $taxa = $forest->make_taxa );

# apply the annotations
annotate(@tip_data)  if @tip_data;
annotate(@node_data) if @node_data;

# write output
print $proj->to_xml;

sub annotate {
	my ( $data, $meta ) = @_;

	# the metadata file is second command line argument
	$log->info("Going to read data from $data");
	$proj->set_namespaces( 'node' => $base_url . '/' . $meta );
	my @header;
	my $csv = Text::CSV->new;
	open my $fh, "<:encoding(utf8)", $data or die $!;	
	LINE: while( my @line = @{ $csv->getline($fh) } ) {
	
		# process the data line
		if ( @header ) {
			my $label = $line[0];
			$log->info("Going to lookup node $label");
			if ( my $node = $tree->get_by_name($line[0]) ) {
				$log->info("Going to annotate node ".$line[0]);
				for my $i ( 1 .. $#line ) {
					$node->set_meta_object( "node:".$header[$i] => $line[$i] );
				}
			}
			else {
				$log->warn("Couldn't find node ".$line[0]);
			}
		}
	
		# process the header
		if ( not @header ) {
			$log->info("Reading CSV header: @line");
			@header = @line;
		}
		last LINE if $csv->eof();
	}
}

