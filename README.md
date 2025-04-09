# RST-Tace
### A tool for automatic comparison and evaluation of RST trees

*RST-Tace allows RST trees annotated by different annotators to be compared and evaluated automatically, aiming to measure the agreement between two annotators. It can be used regardless of the language or the size of rhetorical trees. Based on Iruskieta's method (Iruskieta et.al.,2015), constituents do not need to coincide in their entirety to be compared, only the central subconstituent (CS) which indicates the most important unit of the satellite span, has to be identical. With this restriction, RST Trees are compared using four independent factors: Constituent(C), Attachment point (A), Nuclearity (N) and Relation (R).
The result is reflected by F-measure and inter-annotator agreement. 
For more information, please refer to Wan et.al. (2019).*

## Getting Started

### Prerequisites
RST-Tace is a tool based on Python. It has been developed with [Python 3.6](https://www.python.org/downloads/release/python-360/) and tested with [Python 3.13.2](https://www.python.org/downloads/release/python-3132/). A guide on how to install Python can be found [here](https://realpython.com/installing-python/).

### Installing
RST-Tace can be installed by the following command (once Python 3 has been installed):

```pip3 install git+https://github.com/tkutschbach/RST-Tace.git```

## Usage
After successful installation, RST-Tace can be used on the terminal via: `rsttace`

RST-Tace currently offers the following functionality:

1. Parse a single RST tree, *analyse* and list its annotated relations:
   * ```rsttace analyse <rst-tree>.rs3 -o <output-directory>/```
     > * Reads single file: *\<rst-tree\>.rs3*
     > * Generates result: *\<output-directory\>/Analysis_\<rst-tree>.csv*

2. Parses RST tree pairs and *compares* them with each other:
   * Compare two single trees:\
     ```rsttace compare <rst-tree-1>.rs3 <rst-tree-2>.rs3 -o <output-directory>/```
     > * Reads and compares two files: *\<rst-tree-1\>.rs3* and *\<rst-tree-2\>.rs3*
     > * Generates comparison table: *\<output-directory\>/Comparison_\<rst-tree-1>+\<rst-tree-2\>_Table.csv*
     > * Generates comparison metrics: *\<output-directory\>/Comparison_\<rst-tree-1>+\<rst-tree-2\>_Metrics.csv*
   * Compare two sets of trees (organized in separate directories):\
     ```rsttace compare <directory-1>/ <directory-2>/ -o <output-directory>/```
     > * Reads each file *\<rst-tree\>.rs3* available in both input directories (i.e., *\<directory-1\>/\<rst-tree\>.rs3* and *\<directory-2\>/\<rst-tree\>.rs3*) and compares both different versions with each other
     > * Generates comparison table for each file pair: *\<output-directory\>/Comparison_\<rst-tree\>_Table.csv*
     > * Generates overall comparison metrics for set of pairs: *\<output-directory\>/Comparison_OverallMetrics.csv*

Stating an output directory (via `-o <output-directory>/`) is optional. If ommited, the results will be printed on the command line.

## Versioning
We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/tkutschbach/RST-Tace/tags).

## Authors
* **Shujun Wan** - *Theoretical methodology* - [ShujunW](https://github.com/ShujunW)
* **Tino Kutschbach** - *Implementation* - [tkutschbach](https://github.com/tkutschbach)

## References
* Wan, Shujun; Kutschbach, Tino; Lüdeling, Anke & Stede, Manfred (2019): **RST-Tace. A tool for automatic comparison and evaluation of RST trees.** In: *Proceedings of Discourse Relation Parsing and Treebanking* ([DISRPT](https://sites.google.com/view/disrpt2019/)). NAACL Workshop, Minneapolis.
* Mikel Iruskieta, Iria da Cunha, and Maite Taboada (2015): **A qualitative comparison method for rhetorical structures: identifying different discourse structures in multilingual corpora**. In: *Language Resources and Evaluation*, 49(2):263–309.
