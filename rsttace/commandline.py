# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 14:40:01 2018

@author: tinokuba
"""

import click

from rsttace.controller.interactors import AnalyseInteractor
from rsttace.controller.interactors import CompareInteractor
from rsttace.controller.interactors import EvaluateInteractor
from rsttace.input import RstTreeParser
from rsttace.output import RelTableLogger, RelTableCliOutput
from rsttace.output import CompTableLogger, CompTableCliOutput
from rsttace.output import EvalTableLogger, EvalTableCliOutput


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
@click.argument("INPUTDIR1")
@click.argument("INPUTDIR2")
@click.option("--outputdir", "-o",
              default="",
              metavar="OUTPUTDIR",
              help="Write the result files to OUTPUTDIR")
@click.option('--verbose', '-v', is_flag=True,
              help="Print results on command line")
def evaluate(inputdir1: str,
             inputdir2: str,
             outputdir: str,
             verbose: bool):
    """ Parse and compare two sets of RST-trees (in INPUTDIR1 and INPUTDIR2 \
respectively) with each other and calculate statistical metrics. \
In order to associate RST-trees of both sets with each other, the files \
belonging to each other must have the same name (i.e., for each *.rs3 file in \
INPUTDIR1, the file with the equivalent name is read from INPUTDIR2 and used\
 for comparison with the first one). """

    print("\nComparing the following two RST-Tree sets:")
    print("RST tree set A: " + inputdir1)
    print("RST tree set B: " + inputdir2)

    # prepare input and output classes
    pairTripleList = buildPairTripleList(inputdir1, inputdir2, outputdir)
    tableOutputs = buildEvalTableOutputs(outputdir, verbose)

    print("\nThe following RST tree pairs have been found and will be compared")
    for touple in pairTripleList:
        print(touple[-1])

    interactor = EvaluateInteractor(pairTripleList, tableOutputs)
    interactor.run()


def buildPairTripleList(inputdir1: str, inputdir2: str, outputdir: str):
    pairTripleList = []
    for file in listDirectory(inputdir1):
        if file.endswith(".rs3") and file in listDirectory(inputdir2):
            rstParser1 = RstTreeParser(joinPaths(inputdir1, file))
            rstParser2 = RstTreeParser(joinPaths(inputdir2, file))
            if outputdir != "":
                compTableOutput = CompTableLogger(joinPaths(outputdir, "CompTable_"+file+".csv"))
            else:
                compTableOutput = CompTableCliOutput()
            pairTripleList.append((rstParser1, rstParser2, compTableOutput, file))
    return sorted(pairTripleList, key=lambda tuple: tuple[-1])


def buildEvalTableOutputs(outputdir: str, verbose: bool):
    tableOutputs = []
    if outputdir != "":
        outputfile = joinPaths(outputdir, "EvaluationResults.csv")
        tableOutputs.append(EvalTableLogger(outputfile))
    if(verbose or outputdir == ""):
        tableOutputs.append(EvalTableCliOutput())
    return tableOutputs


def listDirectory(path: str):
    """ Returns list with file names in directory """
    from os import listdir
    return listdir(path)


def joinPaths(path, *paths):
    """ Join two or more paths, inserting "/" as needed """
    from os.path import join
    return join(path, *paths)


def isFile(path: str):
    """ Check whether path points to a file """
    from os.path import isfile
    return isfile(path)


def isDirectory(path: str):
    """ Check whether patch points to a directory """
    from os.path import isdir
    return isdir(path)


if __name__ == "__main__":
    cli()
