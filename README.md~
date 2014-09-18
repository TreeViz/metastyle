phylostylotastic
================

Styled publication of NeXML/NeXSON trees

This is a proof-of-concept implementation, applying TSS styles to the
existing tree-visualization features of [ETE](https://pypi.python.org/pypi/ete2/).

#### Prerequisites
- Python 2.5+
- pip
- [ete2](https://pypi.python.org/pypi/ete2/) 
- [tinycss](http://pythonhosted.org/tinycss/)

#### Quick start
```bash
easy_install pip
pip install tinycss

python pstastic.py examples/met1.xml default.nexss
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
