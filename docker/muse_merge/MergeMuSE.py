#!/usr/bin/env python

"""
Merge MuSE call output
"""

import argparse

def get_args():
    '''
    Loads the parser
    '''
    # Main parser
    parser = argparse.ArgumentParser(description="Merge MuSE call output.")
    # Args
    required = parser.add_argument_group("Required input parameters")
    required.add_argument("--muse_call_out", action='append', required=True)
    required.add_argument("--merge_outname", required=True)
    return parser.parse_args()

if __name__ == '__main__':
    ARGS = get_args()
    FIRST = True
    with open(ARGS.merge_outname, "w") as ohandle:
        for mco in ARGS.muse_call_out:
            with open(mco) as handle:
                for line in handle:
                    if FIRST or not line.startswith('#'):
                        ohandle.write(line)
            FIRST = False
