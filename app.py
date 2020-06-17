import argparse
import command

def app():
    argparser = argparse.ArgumentParser(description='daily-report-cli')
    argparser.set_defaults(func=command.main)
    subparsers = argparser.add_subparsers(dest='subparser_name')
    subparsers.required = False
    current_parser = subparsers.add_parser('current', help='')
    current_parser.set_defaults(func=command.current)
    argparser.add_argument('-m', '--message', type=str, 
    nargs='+', action='append', default=[], required=False, help='')
    argparser.add_argument('-n', '--next', type=str,
    nargs='+', action='append', default=[], required=False, help='')
    argparser.add_argument('-d', '--did', type=str,
    nargs='+', action='append', default=[], required=False, help='')
    argparser.add_argument('-t', '--times', required=False, action='store_true', help='')
    args = argparser.parse_args()
    args.func(args)

