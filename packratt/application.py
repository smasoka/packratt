# -*- coding: utf-8 -*-
import argparse
import sys

from packratt.directories import user_data_dir
from packratt.cache import Cache

def create_parser():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(help='command', dest='command')
    clean = sp.add_parser('clean')
    verify = sp.add_parser('verify')
    return p


def clean(args):
    pass


def _run(args):
    args = create_parser().parse_args(args)
    cache = Cache(user_data_dir)

    return 0

def run():
    return _run(sys.argv[1:])

if __name__ == "__main__":
    sys.exit(run())