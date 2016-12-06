phylostylotastic reborn
=======================

We have taken over this repo for a broader project than the original phylostylotastic.  The general thrust of it is to move things forward with regard to supporting portable renderings of richly annotated trees with data.  

## Our plan

Our plan has not fully materialized, but it is something like this
* part 1: talk a lot, build up team (done)
* part 2: 
   * Complete an exercise in serialization and rendering 
   * Write something up about that 
* part 3: organize a movement for broader adoption, including a hackathon 

### Serialization and rendering exercise 

* Stage 1: Create implementation targets -- DONE (Dec 6, 2016)
   * (Arlin) Create small (7 otu) data set to support mashups
   * (Arlin, Rutger, Jaime) Serialize that in NeXML, NEXUS and Newick + csv
   * (Arlin) Write natural language instructions for 5 increasingly complex views including some or all of the data and key viz features. 
   * Meet to review implementation targets (so everyone understands)
* Stage 2: Proof-of-concept implementations (due 13 December)
   * (Jaime) ETE using internal command language
   * (Jim and Rick) TreeIllustrator using Vega 
   * (Daisie) Mesquite using stylesheets
* Stage 3: Analysis (20 December)
   * Take a week to review implementations
   * Meet to discuss and evaluate
      * consider
         * Serialization of data
         * Representation of graphical commands
         * graphical conventions 
      * relative to criteria of 
         * Compelling design logic
         * Extensibility
         * Ease of use


phylostylotastic
================

Styled publication of NeXML/NeXSON trees. [See the project wiki for more information.](https://github.com/OpenTreeOfLife/phylostylotastic/wiki)

This is a proof-of-concept implementation, applying TSS styles to the
existing tree-visualization features of [ETE](https://pypi.python.org/pypi/ete2/).

#### Prerequisites
- Python 2.5+
- pip
- [ete2](https://pypi.python.org/pypi/ete2/) 
- [tinycss](http://pythonhosted.org/tinycss/)

Installation instructions for ETE are [here (for linux and Mac OS X)](https://pypi.python.org/pypi/ete2/#download-and-install). 
For Mac users who prefer [Homebrew](https://github.com/Homebrew/homebrew), @gaurav suggests these steps instead:
```bash
brew install qt sip pyqt
```

#### Quick start
```bash
easy_install pip
pip install tinycss

# Open a demo file in an interactive view, using a local stylesheet
python pstastic.py examples/met1.xml default.nexss

# Render the styled tree file to an output file (png, pdf, svg)
python pstastic.py -o met1.png examples/met1.xml default.nexss
```

#### ETE gotchas and limitations

Not surprisingly, ETE doesn't support all of the styles and manipulations we would like.

```css
tree {tip-orientation: left;}
tree.upward {tip-orientation: top;}
```
We apparently can't rotate trees cleanly in ETE. That is, the entire diagram is rotated, so labels appear sideways or upside-down. There's no provision for legibility or spacing, so this is effectively useless.

```css
figure {
    background-color: white;
    width: 500px;
    height: 500px;
}
```
Sadly, None of these seem to be available through ETE's `TreeStyle`. It seems to reckon width and height based on the tree and scale.

Font names can't be "chained" for ETE. If you ask for this:
```css
figure {
    background-color: white;
    font: 12pt "Helvetica",serif;
}
```
... all text will appear as the generic serif font, ignoring "Helvetica". The interpreter will instead be optimistic and apply the first (preferred) font name found.

Dimensions can't be expressed as percentages. If you ask for this, it will be ignored:
```css
node[nexss:bootstrap>=0.91][nexss:bootstrap<=1.0] {
    font-size: 200%;
}
```
Use simple numbers instead, or `px` (but the units will be ignored):
```css
node[nexss:bootstrap>=0.91][nexss:bootstrap<=1.0] {
    font-size: 30px;
}
```
