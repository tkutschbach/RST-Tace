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
@click.option("--output", "-o",
              default="",
              metavar="OUTPUTDIR",
              help="Write the result files to the directory OUTPUTDIR.")
@click.option('--verbose', '-v', is_flag=True,
              help="Print results on command line")
def analyse(rstfile: str,
            output: str,
            verbose: bool):
    """ Parse the RST-tree from RSTFILE, and create a list of the rethorical \
relations annotated inside it. """
    rstParser = RstTreeParser(rstfile)

    tableOutputs = []
    if output != "":
        checkAndMakeDir(output)
        filename = extractFileName(rstfile)
        outputfile = "Analysis_" + filename + ".csv"
        outputpath = joinPaths(output, outputfile)
        tableOutputs.append(RelTableLogger(outputpath))
    if(verbose or outputfile == ""):
        tableOutputs.append(RelTableCliOutput())

    print("\nAnalyse and list relations of RST tree in: " + rstfile)
    interactor = AnalyseInteractor(rstParser, tableOutputs)
    interactor.run()


@cli.command('compare', short_help="Compare RST tree pairs and calculate \
                                    statistical equivalence metrics.")
@click.argument("INPUTPATH1")
@click.argument("INPUTPATH2")
@click.option("--output", "-o",
              default="",
              metavar="OUTPUTDIR",
              help="Write the result files to the directory OUTPUTDIR.")
@click.option('--verbose', '-v', is_flag=True,
              help="Print results on command line")
def compare(inputpath1: str,
            inputpath2: str,
            output: str,
            verbose: bool):
    """ Parse two RST-trees (or two sets of RST-tree pairs), \
from INPUTPATH1 and INPUTPATH2 respectively, compare their annotated \
relations, and create comparison tables. If INPUTPATH1 and INPUTPATH2 \
both point to files then both single files will be compared with \
each other. If INPUTPATH1 and INPUTPATH2 both point to directories \
then all '.rs3' files in both directories will be compared with each other. \
If '-o' is set, then the results will be written to OUTPUTPATH. Otherwise,
the results will be printed back on the command line. """
    checkAndMakeDir(output)

    if isFile(inputpath1) and isFile(inputpath2):
        compareTwoFiles(inputpath1, inputpath2, output, verbose)
    elif isDirectory(inputpath1) and isDirectory(inputpath2):
        compareTwoFolders(inputpath1, inputpath2, output, verbose)
    else:
        print("Error: INPUTPATH1 and INPUTPATH2 must either both point to files or \
both to directories. -> Abort")
        pass


def compareTwoFiles(rstfile1, rstfile2, outputdir, verbose):
    rstParser1 = RstTreeParser(rstfile1)
    rstParser2 = RstTreeParser(rstfile2)

    tableOutputs = []
    if outputdir != "":
        filename1 = extractFileName(rstfile1)
        filename2 = extractFileName(rstfile2)
        outputfile = "Comparison_" + filename1 + "+" + filename2 + ".csv"
        outputpath = joinPaths(outputdir, outputfile)
        tableOutputs.append(CompTableLogger(outputpath))
    if(verbose or outputdir == ""):
        tableOutputs.append(CompTableCliOutput())

    print("\nComparing the following two RST trees:")
    print("RST tree A: " + rstfile1)
    print("RST tree B: " + rstfile2)
    interactor = CompareInteractor(rstParser1, rstParser2, tableOutputs)
    interactor.run()
    return


def compareTwoFolders(inputdir1, inputdir2, outputdir, verbose):
    print("\nComparing the following two RST-Tree sets:")
    print("RST tree set A: " + inputdir1)
    print("RST tree set B: " + inputdir2)

    # prepare input and output classes
    pairTripleList = buildPairTripleList(inputdir1, inputdir2, outputdir)
    tableOutputs = buildEvalTableOutputs(outputdir, verbose)

    print("\nFollowing RST tree pairs have been found and will be compared:")
    for touple in pairTripleList:
        print(touple[-1])

    interactor = EvaluateInteractor(pairTripleList, tableOutputs)
    interactor.run()

    return


def buildPairTripleList(inputdir1: str, inputdir2: str, outputdir: str):
    pairTripleList = []
    for file in listDirectory(inputdir1):
        if file.endswith(".rs3") and file in listDirectory(inputdir2):
            filename = extractFileName(file)
            rstParser1 = RstTreeParser(joinPaths(inputdir1, file))
            rstParser2 = RstTreeParser(joinPaths(inputdir2, file))
            if outputdir != "":
                outputfile = "Comparison_" + filename + ".csv"
                outputpath = joinPaths(outputdir, outputfile)
                compTableOutput = CompTableLogger(outputpath)
            else:
                compTableOutput = CompTableCliOutput()
            pairTuple = (rstParser1, rstParser2, compTableOutput, filename)
            pairTripleList.append(pairTuple)
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


def extractFileName(path: str):
    """ Extracts the file name of a file path """
    from os.path import basename, splitext
    return splitext(basename(path))[0]


def checkAndMakeDir(path: str):
    from os.path import exists
    from os import makedirs
    if not exists(path):
        print("Output directory does not exist. Create: " + path)
        makedirs(path)


if __name__ == "__main__":
    cli()
