## viz targets exercise (README)

This contains all of the files relevant to the initial exercise. 

Note that we are working on at least 4 things at once 
* conventions for integration of trees with other data
* serializations of integrations
* high-level language for describing renderings of integrations
* detailed implementations of rendering

## files 

* `targets.md` - description of targets
* `tree.nwk` - a Newick tree 
* `tree_boots.nwk` - Newick tree with bootstrap support values 
* `tree_posteriors.nwk` - Newick tree with Bayesian posteriors
* `tip_data.csv` - tip data in comma-separated-value format
* `tip_data_meta.csv` - metadata describing columns and their meaning in `tip_data.csv`
* `inode_data.csv` - internal node data in comma-separated-value format
* `inode_data_meta.csv` - metadata describing columns and their meaning in `inode_data.csv`

Each tip or inode has a unique label that is either a species name or a higher taxon name.  

In order to accomplish the steps described in `targets.md`, implementations must be able to cross-reference these names with the "Newick label" column in the CSV files.  

Note that using a fully labeled tree by-passes an issue that will come up eventually in real data, which is how to identify nodes in Newick strings that lack internal node labels.  The two obvious solutions are 

1. use phyloreferences that refer to tip labels, e.g., `label clade(otu1, otu7) "carnivores"`
1. begin the process of integration by assigning inode labels (e.g., inode1, inode2), then save those and use them. 

