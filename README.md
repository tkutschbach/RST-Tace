# RST-Tace

This repository is still under construction.
Updates and more information will follow.

## Getting Started

### Prerequisites
RST-Tace is a tool based on Python. It has been developed and tested with [Python 3.6](https://www.python.org/downloads/release/python-360/). A guide on how to install Python can be found [here](https://realpython.com/installing-python/).

### Installing
RST-Tace can be installed by the following command (once Python 3 has been installed):

```pip3 install git+https://github.com/tkutschbach/RST-Tace.git```

## Usage
After successful installation, RST-Tace can be used on the terminal via: `rsttace`

RST-Tace currently offers the following functionality:

1. Parse a single RST tree, *analyse* and list its annotated relations:

```rsttace analyse <rst-tree>.rs3 -o <output-file>.csv```

2. Parse an RST tree pair and *compare* the trees with each other:

```rsttace compare <rst-tree-1>.rs3 <rst-tree-2>.rs3 -o <output-file>.csv```

Stating an output file (via `-o <output-file>.csv`) is optional. If ommited, the results will be printed on the command line.

## Versioning
We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/tkutschbach/RST-Tace/tags).

## Authors
* **Shujun Wan** - *Theoretical methodology* 
* **Tino Kutschbach** - *Implementation* - [tkutschbach](https://github.com/tkutschbach)

## References
* Wan, Shujun; Kutschbach, Tino; Lüdeling, Anke & Stede, Manfred (2019) **RST-Tace. A tool for automatic comparison and evaluation of RST trees.** In: *Proceedings of Discourse Relation Parsing and Treebanking* ([DISRPT](https://sites.google.com/view/disrpt2019/)). NAACL Workshop, Minneapolis.