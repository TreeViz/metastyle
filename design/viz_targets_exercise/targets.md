# targets 

## Notes before starting 

The data inputs consist of 
* a Newick tree in "tree.nwk"
* tip data in "tip\_data.csv"
* internal node data in "inode\_data.csv"
* support values in two additional Newick files, "tree\_boots.nwk" and "tree\_posteriors.nwk"

Each tip or inode has a unique label that is either a species name or a higher taxon name.  In order to accomplish the steps below using the inputs provided, implementations must be able to cross-reference these names with the "Newick label" column in the CSV files.  

Note that using a fully labeled tree by-passes an issue that will come up eventually in real data, which is how to identify nodes in Newick strings that lack internal node labels.  The two obvious solutions are 
1. use phyloreferences that refer to tip labels, e.g., `label clade(otu1, otu7) "carnivores"`
1. begin the process of creating a rich tree by assigning inode labels (e.g., inode1, inode2), then save those and use them. 

## 1. Overall tree style

### Recipe
* display tree with 6-point lines in dark green
* display labels in 16-point Helvetica  

### Rendering options 
* none

### Extra credit

### Comments and notes

## 2. Labeling parts

### Recipe
* show `vernacularName` as label for inodes "Cervidae", "Bovidae" and "Carnivora" 
   * preferred: labeled vertical bars to the right of the tree
* display the annotation "Foregut fermentation evolves" on the branch above node Artiodactyla
   * preferred: floating text box with reference line or arrow to branch

### Rendering options 
* whether to use bars, boxes, braces, or something else to label clades
* whether the labels are fixed or dynamic (e.g., floatover)
* style and font of labels
* whether to use an arrow, speech bubble, etc for the branch annotation

### Extra credit

### Comments and notes


## 3. Images and linkouts

### Recipe
* Display image at `imageURL` for tips
   * preferred: display thumbnail, mouse-down to open or pop-up enlarged view
* Provide link-outs to `infoURL` for tips 
   * preferred: mouse-down on tip label to open `infoURL` in new tab

### Rendering options 
* static thumbnail or mouse-over tip label to show thumbnail
* add "View image" button to each tip, click to open `imageURL` in new tab

### Extra credit
* linkouts and images for internal nodes

### Comments and notes

## 4. Multiple types of support values 

### Recipe
* show bootstrap values in green, posterior probabilities in blue
   * preferred: bootstraps above, posteriors below node

### Rendering options 
* show both values on the same side (above or below) the node

### Extra credit

### Comments and notes

## 5. Categorical and numeric data

### Recipe
* show values of categorical variable `trophic_habit`
   * preferred: color-coded blocks
* show values of numeric variable `mass_in_kg`
   * preferred: bar chart

### Rendering options 
* categorical values in color with key, or as text labels
* numeric values in text format, or as bar chart

### Extra credit

### Comments and notes

