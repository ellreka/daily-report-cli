import argparse
# import numpy as np
# import matplotlib.pyplot as plt
# import japanize_matplotlib
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
    default=[], required=False, help='')
    argparser.add_argument('-t', '--times',required=False, action='store_true', help='')
    args = argparser.parse_args()
    print(args)
    args.func(args)
    # command.main()

    

# def create_graph(data):
#     label = list(map(lambda n: n['project_name'], data))
#     colors = list(map(lambda n: n['color'], data))
#     x = np.array(list(map(lambda n: n['time'], data)))
#     plt.pie(x, labels=label, colors=colors, counterclock=False, startangle=90)
#     plt.savefig('figure.png')
