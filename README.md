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

python pstastic.py nexml/testtree.xml nexml/default.nexss
```
