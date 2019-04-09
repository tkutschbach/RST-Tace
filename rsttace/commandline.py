# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 14:40:01 2018

@author: tinokuba
"""

import click

from rsttace.controller import Interactor
from rsttace.controller.interactors import AnalyseInteractor, CompareInteractor
from rsttace.input import RstTreeParser
from rsttace.output import RelTableLogger, RelTableCliOutput
from rsttace.output import CompTableLogger, CompTableCliOutput


@click.group()
def cli():
    """ This tool analyses, compares, and evaluates RST-trees. """
    pass


@cli.command('analyse', short_help="Parse single RST trees, analyse and list\
                                    their annotated relations")
@click.argument("RSTFILE")
@click.option("--outputfile", "-o",
              default="",
              metavar="FILEPATH",
              help="Write the result list to FILEPATH (as CSV)")
@click.option('--verbose', '-v', is_flag=True,
              help="Print results on command line")
def analyse(rstfile: str,
            outputfile: str,
            verbose: bool):
    """ Parse the RST-tree from RSTFILE, and create a list of the rethorical
    relations annotated inside it. """
    rstParser = RstTreeParser(rstfile)

    tableOutputs = []
    if outputfile != "":
        tableOutputs.append(RelTableLogger(outputfile))
    if(verbose or outputfile == ""):
        tableOutputs.append(RelTableCliOutput())

    interactor = AnalyseInteractor(rstParser, tableOutputs)
    interactor.run()


@cli.command('compare', short_help="Parse RST tree pairs and \
                                    compare them with each other")
@click.argument("RSTFILE1")
@click.argument("RSTFILE2")
@click.option("--outputfile", "-o",
              default="",
              metavar="FILEPATH",
              help="Write the result list to FILEPATH (as CSV)")
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

    interactor = CompareInteractor(rstParser1, rstParser2, tableOutputs)
    interactor.run()


@cli.command('evaluate', short_help="Perform a statistical evaluation\
                                     of a set of RST tree pairs.")
@click.argument("RSTFILE1")
@click.argument("RSTFILE2")
@click.option("--outputfile", "-o",
              default="",
              metavar="FILEPATH",
              help="Write the result list to FILEPATH (as CSV)")
def evaluate(rstfile1: str,
             rstfile2: str,
             outputfile: str):
    print("Sorry, this functionality is not implemented yet.")
    pass


if __name__ == "__main__":
    cli()
