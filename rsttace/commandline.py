# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 14:40:01 2018

@author: tinokuba
"""

import click

from rsttace.controller.interactors import AnalyseInteractor, CompareInteractor
from rsttace.input import RstTreeParser
from rsttace.output import RelTableLogger, RelTableCliOutput
from rsttace.output import CompTableLogger, CompTableCliOutput


@click.group()
def cli():
    """ This tool analyses, compares, and evaluates RST-trees. """
    pass


@cli.command('analyse', short_help="Parse a single RST tree, analyse and list\
                                    its annotated relations.")
@click.argument("RSTFILE")
@click.option("--outputfile", "-o",
              default="",
              metavar="FILEPATH",
              help="Write the result list of annotations to FILEPATH (as CSV)")
@click.option('--verbose', '-v', is_flag=True,
              help="Print results on command line")
def analyse(rstfile: str,
            outputfile: str,
            verbose: bool):
    """ Parse the RST-tree from RSTFILE, and create a list of the rethorical \
relations annotated inside it. """
    rstParser = RstTreeParser(rstfile)

    tableOutputs = []
    if outputfile != "":
        tableOutputs.append(RelTableLogger(outputfile))
    if(verbose or outputfile == ""):
        tableOutputs.append(RelTableCliOutput())

    print("\nAnalyse and list relations of RST tree in: " + rstfile)
    interactor = AnalyseInteractor(rstParser, tableOutputs)
    interactor.run()


@cli.command('compare', short_help="Parse an RST tree pair and compare\
                                    both trees with each other.")
@click.argument("RSTFILE1")
@click.argument("RSTFILE2")
@click.option("--outputfile", "-o",
              default="",
              metavar="FILEPATH",
              help="Write the resulting comparison table to FILEPATH (as CSV)")
@click.option('--verbose', '-v', is_flag=True,
              help="Print results on command line")
def compare(rstfile1: str,
            rstfile2: str,
            outputfile: str,
            verbose: bool):
    """ Parse two RST-trees, from RSTFILE1 and RSTFILE2 respectively, \
compare their annotated relations, and create a comparison table. """
    rstParser1 = RstTreeParser(rstfile1)
    rstParser2 = RstTreeParser(rstfile2)

    tableOutputs = []
    if outputfile != "":
        tableOutputs.append(CompTableLogger(outputfile))
    if(verbose or outputfile == ""):
        tableOutputs.append(CompTableCliOutput())

    print("\nComparing the following two RST trees:")
    print("RST tree A: " + rstfile1)
    print("RST tree B: " + rstfile2)
    interactor = CompareInteractor(rstParser1, rstParser2, tableOutputs)
    interactor.run()


@cli.command('evaluate', short_help="Perform a statistical evaluation\
                                     of a set of RST tree pairs.")
@click.argument("DIRECTORY1")
@click.argument("DIRECTORY2")
@click.option("--outputfile", "-o",
              default="",
              metavar="FILEPATH",
              help="Write the result table to FILEPATH (as CSV)")
@click.option('--verbose', '-v', is_flag=True,
              help="Print results on command line")
def evaluate(directory1: str,
             directory2: str,
             outputfile: str,
             verbose: bool):
    """ Parse and compare two sets of RST-trees (in DIRECTORY1 and DIRECTORY2 \
respectively) with each other and calculate statistical metrics. \
In order to associate RST-trees of both sets with each other, the files \
belonging to each other must have the same name (i.e., for each *.rs3 file in \
DIRECTORY1, the file with the equivalent name is read from DIRECTORY2 and used\
 for comparison with the first one). """

    print("Sorry, this functionality is not implemented yet.")
    pass


if __name__ == "__main__":
    cli()
