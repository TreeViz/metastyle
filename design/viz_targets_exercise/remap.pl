#!/usr/bin/perl
use strict;
use warnings;
use Bio::Phylo::Factory;
use Bio::Phylo::IO 'parse';
use Bio::Phylo::Util::CONSTANT qw':objecttypes :namespaces';

my $fac = Bio::Phylo::Factory->new;
my $file = shift;
my $project = parse(
	'-format'     => 'nexml',
	'-file'       => $file,
	'-as_project' => 1,
);

# add these namespaces and their prefixes to the project
$project->set_namespaces(
	'dwc'     => _NS_DWC_,
	'dcterms' => _NS_DCTERMS_,
	'cdao'    => _NS_CDAO_,
	'px'      => _NS_PHYLOXML_,
	'rdfs'    => _NS_RDFS_,
);

# convert these predicates
my %predicates = (
	'tip:vernacularName'  => 'dwc:vernacularName',
	'tip:rank'            => 'dwc:taxonRank',
	'tip:imageURL'        => 'dwc:associatedMedia',
	'tip:ncbi_taxid'      => 'dwc:taxonID',
	'tip:infoURL'         => 'cdao:has_External_Reference',
	'tip:imageLicense'    => 'dcterms:license',
	'tip:imageAuthor'     => 'dcterms:rightsHolder',
	'node:vernacularName' => 'dwc:vernacularName',
	'node:rank'           => 'dwc:taxonRank',
	'node:imageURL'       => 'dwc:associatedMedia',
	'node:ncbi_taxid'     => 'dwc:taxonID',
	'node:infoURL'        => 'cdao:has_External_Reference',
	'node:imageLicense'   => 'dcterms:license',
	'node:imageAuthor'    => 'dcterms:rightsHolder',
);
for my $node ( @{ $project->get_items(_NODE_) } ) {
	
	# simple remapping
	for my $meta ( @{ $node->get_meta(keys %predicates) } ) {
		my ( $p, $o ) = ( $meta->get_predicate, $meta->get_object );
		$meta->set_triple( $predicates{$p} => $o );
	}
	
	# attach under confidence node
	my $c = $fac->create_meta( '-triple' => { 'px:confidence' => 1 } );
	$node->add_meta($c);
	for my $m ( @{ $node->get_meta(qw(node:bootstrap node:posterior)) } ) {
		my ( $p, $o ) = ( $m->get_predicate, $m->get_object );
		$p =~ s/node:/px:/;
		$m->set_triple( $p => $o );	
		$c->add_meta($m);
		$node->remove_meta($m);	
	}
}

# attach license and rightsHolder to image
for my $node ( @{ $project->get_items(_NODE_) } ) {
	my @p = qw(dwc:associatedMedia dcterms:license dcterms:rightsHolder);
	my ( $i, $l, $h ) = @{ $node->get_meta(@p) };
	if ( $i and $l and $h ) {
		$i->add_meta($l);
		$i->add_meta($h);
		$node->remove_meta($l);
		$node->remove_meta($h);
	}
}

# create a continuous character matrix
my ($taxa) = @{ $project->get_taxa };
{
	my $matrix = $fac->create_matrix( 
		'-type' => 'continuous',
		'-taxa' => $taxa,
		'-name' => 'mass_in_kg',
	);
	$project->insert($matrix);
	for my $tip ( grep { $_->is_terminal } @{ $project->get_items(_NODE_) } ) {
		my ($meta) = @{ $tip->get_meta('tip:mass_in_kg') };
		$matrix->insert( $fac->create_datum(
			'-type_object' => $matrix->get_type_object,
			'-taxon'       => $tip->get_taxon,
			'-char'        => [ $meta->get_object ],
		) );
		$tip->remove_meta($meta);
	}
}

# create a categorical character matrix
{
 
 	my $matrix = $fac->create_matrix(
 		'-type' => 'standard',
 		'-taxa' => $taxa,
 		'-name' => 'trophic_habit',
 	);
 	$project->insert($matrix);
	my ( %state, %lookup, $counter );
	for my $tip ( grep { $_->is_terminal } @{ $project->get_items(_NODE_) } ) {
		my ($meta) = @{ $tip->get_meta('tip:trophic_habit') };
		my $o = $meta->get_object;
		my $state = $state{$o} || ( $state{$o} = $counter++ );
		$matrix->insert( $fac->create_datum(
			'-type_object' => $matrix->get_type_object,
			'-taxon'       => $tip->get_taxon,
			'-char'        => [ $state ],
		) );
		$tip->remove_meta($meta);
		$lookup{$state} = [ $state ];
	}
	$matrix->get_type_object->set_lookup(\%lookup);
	for my $label ( keys %state ) {
		$matrix->get_type_object->add_meta_for_state(
			$fac->create_meta( '-triple' => { 'rdfs:label' => $label } ), $state{$label}
		);
	}			
}

# done
print $project->to_xml;