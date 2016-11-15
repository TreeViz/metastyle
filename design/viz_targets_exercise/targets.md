# targets 

## Notes before starting 

* there is a single table of data for tips, and another for internal nodes (inodes)
* the Newick string and the data tables are cross-referenced by the tip and inode labels in the Newick string.  For readability, I am using higher taxon names (a kind of human-readable label) as node identifiers.  However, it many circumstances these will be arbitrary identifiers. That is, you might have a tree with "inode1" through "inode7" instead of taxon names.  
* The same thing goes for tips.  In the real world, these are often codes like "D_melanogaster_NM288433".
* In order to accomplish the steps below using the inputs provided, implementations must be able to match Newick ids with labels that are stored in separate data file.  

## Overall tree style

### Recipe
* display tree with 6-point lines in dark green
* display labels in 16-point Helvetica  

### Rendering options 
* 
### Extra credit

### Comments and notes

## Labeling parts

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


## Images and linkouts

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


## Categorical and numeric data

### Recipe
* align tips with data table 
   * show viz_sample7.nwk with categorical data in trophic habit column of viz_sample7_data.csv 
   * show viz_sample7.nwk with numeric data in body mass column of viz_sample7_data.csv 

### Rendering options 

### Extra credit

### Comments and notes

