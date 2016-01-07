"""The gateway between the CLI and tt's core functionality.
"""

import sys
import logging as log

from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentError

from tt.eqtools import (BooleanEquationWrapper, GrammarError,
                        TooManySymbolsError)
from tt.fmttools import TruthTablePrinter

__all__ = ['main']
__version__ = 0.1

logging_format = '%(levelname)s: %(message)s'


# function wrappers; may be moved/refactored when this becomes too cluttered
def table_cmd(bool_eq_wrapper):
    TruthTablePrinter(bool_eq_wrapper.eval_result).print_tt()
    print()


def table_intermediates_cmd(bool_eq_wrapper):
    pass


def kmap_cmd(bool_eq_wrapper):
    pass


def sop_cmd(bool_eq_wrapper):
    pass


def pos_cmd(bool_eq_wrapper):
    pass


def minimal_cmd(bool_eq_wrapper):
    pass


def main(args=None):
    """The main entry point to the command line application.

    Set up the arg parser and choose which control flow to follow according to
    user's command line options.

    Args:
        args (List[str]): The command line arguments. Allows for complete
            testing of the program with ``main`` as the entry point.

    Returns:
        Error level (int):
            0: Program ran fine.
            1: Recognized error occurred.
            2: Unrecognized error occurred.

    """

    if args is None:
        args = sys.argv[1:]

    try:
        # Setup argument parser
        parser = ArgumentParser(
            prog='tt',
            description='tt is a command line utility written in Python for '
                        'truth table and Karnaugh Map generation.\n'
                        'tt also provides Boolean algebra syntax checking.\n'
                        'Use tt --help for more information.',
            formatter_class=RawTextHelpFormatter)
        parser.add_argument(
            '--version',
            action='version',
            version='v'+str(__version__),
            help='Program version and latest build date')
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Specify verbose output, useful for debugging.')
        parser.add_argument(
            '--kmap',
            action='store_true',
            help='Generate kmap of specified boolean equation.\n'
                 'Currently unsupported.')
        parser.add_argument(
            '--intermediates',
            action='store_true',
            help='Indicates that intermediate Boolean expressions should be\n'
                 'displayed with their own column in the truth table.\n'
                 'Not valid with the --kmap option.\n'
                 'NOTE: Not yet implemented.')
        parser.add_argument(
            '--table',
            action='store_true',
            help='') # TODO
        parser.add_argument(
            '--minimal',
            action='store_true',
            help='Use this option to modify the --pos and --sop commands to\n'
                 'get the minimal product of sums or sum of products form.')
        parser.add_argument(
            '--sop',
            action='store_true',
            help='') # TODO
        parser.add_argument(
            '--pos',
            action='store_true',
            help='') # TODO
        parser.add_argument(
            dest='equation',
            help='Boolean equation to be analyzed, enclosed with quotes.\n'
                 'Boolean operations can be specified using plain English or '
                 'their common symbolic equivalents.\n'
                 'For example, the two equations:\n'
                 '\t(1) "out = operand_1 and operand_2 or operand_3"\n'
                 '\t(2) "out = operand_1 && operand_2 || operand_3"\n'
                 'Would evaluate identically.\n'
                 '\n'
                 'Supported Boolean operations are:\n'
                 '\tnot\n'
                 '\txor\n'
                 '\txnor\n'
                 '\tand\n'
                 '\tnand\n'
                 '\tor\n'
                 '\tnor\n')

        # Process arguments
        args = parser.parse_args(args)

        verbose = args.verbose
        kmap = args.kmap
        intermediates = args.intermediates
        table = args.table
        minimal = args.minimal
        sop = args.sop
        pos = args.pos
        equation = args.equation

        if verbose:
            log.basicConfig(format=logging_format, level=log.DEBUG)
            log.info('Starting verbose output.')
        else:
            log.basicConfig(format=logging_format)

        # temporary, until these features are implemented
        if kmap:
            raise NotImplementedError('--kmap')
        if intermediates:
            raise NotImplementedError('--intermediates')
        if minimal:
            raise NotImplementedError('--minimal')
        if sop:
            raise NotImplementedError('--sop')
        if pos:
            raise NotImplementedError('--pos')

        if intermediates and not table:
            raise ArgumentError('The --intermediates option must be used in\n'
                                'conjunction with the --table option.')

        bool_eq_wrapper = BooleanEquationWrapper(equation)

        if table:
            if intermediates:
                table_intermediates_cmd(bool_eq_wrapper)
            else:
                table_cmd(bool_eq_wrapper)
        if kmap:
            kmap_cmd(bool_eq_wrapper)
        if pos:
            pos_cmd(bool_eq_wrapper)
        if sop:
            sop_cmd(bool_eq_wrapper)

    except KeyboardInterrupt:
        return 0
    except GrammarError as e:
        e.log()
        return 1
    except TooManySymbolsError as e:
        log.error(str(e))
        return 1
    except ArgumentError as e:
        log.error(str(e))
        return 1
    except NotImplementedError as e:
        log.error('Tried to use a feature that is not yet implemented: ' +
                  str(e))
        return 1
    except Exception as e:
        log.critical('An unknown error occurred. '
                     'Cannot continue program execution.\n' +
                     str(e))
        return 2
