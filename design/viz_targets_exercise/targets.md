# targets 

## Notes before starting 

Read the notes on the README if you haven't already. 

## 1. Overall tree style

### Recipe
* display tree with 4-point lines in dark green
* display labels in 16-point Helvetica  

### Rendering options 
* none

### Extra credit

### Comments and notes

## 2. Labeling parts

### Recipe
* show `vernacularName` as label for inodes "Cervidae", "Bovidae" and "Carnivora" 
   * preferred: labeled vertical bars to the right of the tree
* show `vernacularName` in the label for all of the tips
   * preferred: show in parentheses, after scientific name
* display the annotation "Foregut fermentation evolves" on the branch above node Artiodactyla
   * preferred: floating text box with reference line or arrow to branch

### Rendering options 
* inode labels
   * whether to use bars, boxes, braces, or something else to label clades
* tip labels
   * show `vernacularName` as float-over
   * show one label above the other
* labels in general
   * whether the labels are fixed or dynamic (e.g., floatover)
   * style and font of labels, e.g., common names in green
* whether to use an arrow, speech bubble, etc for the branch annotation

### Extra credit

### Comments and notes


## 3. Images and linkouts

### Recipe
* Display image with URL `imageURL` for tips
   * preferred: display thumbnail, mouse-down to open or pop-up enlarged view
* Provide link-outs to info page with URL `infoURL` for tips 
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
   * preferred: bootstraps above, posteriors below 

### Rendering options 
* show both values on the same side (above or below) the node

### Extra credit
* use float-overs to reveal metadata `label` and `description`, e.g., mouse-over a bootstrap value and see "Bootstrap support: Percent support for this branch from resampled data"

### Comments and notes

## 5. Categorical and numeric data

### Recipe
* show values of categorical variable `trophic_habit`
   * preferred: color-coded blocks
   * preferred: read column label from the `label` column in the metadata file 
* show values of numeric variable `mass_in_kg`
   * preferred: bar chart
   * preferred: read column label from the `label` column in the metadata file 

### Rendering options 
* categorical values as text labels (no colors)
* numeric values in text format (no bar chart)

### Extra credit
* use float-overs to reveal metadata `label` and `description`, as described above. 

### Comments and notes

