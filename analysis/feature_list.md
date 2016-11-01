# feature list

everything I can think of so far, roughly ordered from top to bottom in terms of importance. 

* tip label 
   * used for: designating tip
   * features: 
      * control font face, size, color  
      * show footnote marker
* branch lines
   * used for: drawing tree
   * features: control thickness, color, style
* branch lengths
   * is this too obvious for this list?
* branch labels
   * used for: assigning a name, ID, or footnote marker to a branch
   * features: 
      * variable font
      * placement above or below
* images at the tips
   * used for: fast visual recognition of species 
   * features: 
      * metadata (author, license) and link to full-size image
* text or numeric column aligned with tips
   * used for: common names, character states
   * features:
      * variable font, size, color
* clade designators 
   * used for: designating a clade
   * features 
      * style (bracket, bar or box)
      * label (variable font, size, color)
      * vertical label is frequently desired
      * clade image with vertical-center alignment to clade
      * possibly collapse clade with a triangle notation?
* scale bar 
   * used for: distance or substitutions or other units
   * features: bar, value (length), units
* notes or labels with reference lines
   * used for: pointing out features of tree
   * comment: these can be avoiding by using markers (e.g., a, b, c) and a key
   * features: 
      * bounding box
* time scale 
   * used for: geologic time in scaled trees
   * features
      * tick marks
      * values
      * align 0 end with tips
      * labels on the time scale (mesozoic, cenozoic)
* character matrix 
   * used for: presenting data in phylogenetic context
   * features 
      * variable row shading
      * variable column shading
      * variable cell color (value as color)
      * column descriptors (e.g., position)
      * reference char. state for column
* circular geometry
* bar chart
   * used for: tip data, e.g., abundance in metagenomic sample
   * features: color, style
* ticks along branch
   * used for: designating change events
   * features:
      * multiple styles on same tree (box, tick)
      * tiny labels
* pseudocontinuous coloring 
   * used for: representing BAMM results, continuous char states
   * features: break up segments arbitrarily, assign colors
* a vertical bar representing a time interval through the tree
   * used for: designating an interval of interest across the tree
   * features
      * precise alignment with time scale
      * label on the bar
* extinct branches that terminate prior to the present
* variable thickness of branches 
   * used for: designate an interval
   * used for: emphasis 
* stacked lines 
   * used for: showing aggregated states changing along branches
* link nodes to map via reference lines
   * used for: phylogeography
   * features: variable width, color
* pie labels at nodes
   * used for: ancestral state reconstruction
   * features: multiple colors, various percentages
   * could be represented as a small matrix of states and percentages attached to particular nodes
