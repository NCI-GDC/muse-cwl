#!/usr/bin/env python
'''Internal multithreading MuSE call'''

import os
import argparse
import logging
import subprocess
import string
from functools import partial
from multiprocessing.dummy import Pool, Lock

def is_nat(x):
    '''Checks that a value is a natural number.'''
    if int(x) > 0:
        return int(x)
    raise argparse.ArgumentTypeError('%s must be positive, non-zero' % x)

def setup_logging(level, log_name, log_filename):
    '''Sets up a logger'''
    logger = logging.getLogger(log_name)
    logger.setLevel(level)
    if log_filename is None:
        shell_log = logging.StreamHandler()
    else:
        shell_log = logging.FileHandler(log_filename, mode='w')

    shell_log.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(shell_log)
    return logger

def do_pool_commands(cmd, logger, lock = Lock(), shell_var=True):
    '''run pool commands'''
    logger.info('running: {}'.format(cmd))
    try:
        output = subprocess.Popen(cmd, shell=shell_var, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_stdout, output_stderr = output.communicate()
        with lock:
            logger.info(cmd)
            output_stdout = output_stdout.split("\n")
            for line in output_stdout:
                logger.info(line)
            output_stderr = output_stderr.split("\n")
            for line in output_stderr:
                logger.info(line)
    except Exception:
        logger.exception("command failed {}".format(cmd))
    return output.wait()

def multi_commands(cmds, thread_count, logger, shell_var=True):
    '''run commands on number of threads'''
    pool = Pool(int(thread_count))
    output = pool.map(partial(do_pool_commands, logger=logger, shell_var=shell_var), cmds)
    return output

def get_region(intervals):
    '''get region from intervals'''
    interval_list = []
    with open(intervals, 'r') as fh:
        line = fh.readlines()
        for bed in line:
            blocks = bed.rstrip().rsplit('\t')
            intv = '{}:{}-{}'.format(blocks[0], int(blocks[1])+1, blocks[2])
            interval_list.append(intv)
    return interval_list

def cmd_template(ref=None, region=None, tumor=None, normal=None):
    '''cmd template'''
    template = string.Template("/bin/MuSEv1.0rc_submission_c039ffa call -f ${REF} -r ${REGION} ${TUMOR} ${NORMAL} -O ${NUM}")
    for i, interval in enumerate(region):
        cmd = template.substitute(
            dict(
                REF=ref,
                REGION=interval,
                TUMOR=tumor,
                NORMAL=normal,
                NUM=i
            )
        )
        yield cmd, '{}.MuSE.txt'.format(i)

def main():
    '''main'''
    parser = argparse.ArgumentParser('Internal multithreading MuSE call.')
    # Required flags.
    parser.add_argument('-f', '--reference_path', required=True, help='Reference path.')
    parser.add_argument('-r', '--interval_bed_path', required=True, help='Interval bed file.')
    parser.add_argument('-t', '--tumor_bam', required=True, help='Tumor bam file.')
    parser.add_argument('-n', '--normal_bam', required=True, help='Normal bam file.')
    parser.add_argument('-c', '--thread_count', type=is_nat, required=True, help='Number of thread.')
    args = parser.parse_args()
    ref = args.reference_path
    interval = args.interval_bed_path
    tumor = args.tumor_bam
    normal = args.normal_bam
    threads = args.thread_count
    log_file = "{}.{}.multi_muse.log".format(os.path.basename(tumor), os.path.basename(normal))
    logger = setup_logging(logging.INFO, '{}.{}'.format(os.path.basename(tumor), os.path.basename(normal)), log_file)
    muse_cmds = list(cmd_template(ref=ref, region=get_region(interval), tumor=tumor, normal=normal))
    outputs = multi_commands(muse_cmds, threads, logger)
    first = True
    with open('multi_muse_call_merged.MuSE.txt', 'w') as oh:
        for cmd, out in muse_cmds:
            with open(out) as fh:
                for line in fh:
                    if first or not line.startswith('#'):
                        oh.write(line)
            first = False
    if any(x != 0 for x in outputs):
        logger.info('Failed multi_muse')
    else:
        logger.info('Completed multi_muse')

if __name__ == '__main__':
    main()
