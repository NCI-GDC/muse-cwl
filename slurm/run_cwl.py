import argparse
import pipelineUtil
import uuid
import os
import postgres
import status_postgres
import setupLog
import logging
import tempfile
import time
import datetime
from elapsed_time import Time as Time

def update_postgres(exit, cwl_failure, vcf_upload_location, muse_location, logger):
    """ update the status of job on postgres """

    loc = 'UNKNOWN'
    status = 'UNKNOWN'


    if sum(exit) == 0:

        loc = vcf_upload_location

        if not(cwl_failure):

            status = 'COMPLETED'
            logger.info("uploaded all files to object store. The path is: %s" %muse_location)

        else:

            status = 'POSTGRES_FAILED'
            logger.info("CWL failed but outputs were generated. The path is: %s" %muse_location)

    else:

        loc = 'Not Applicable'

        if not(cwl_failure):

            status = 'UPLOAD_FAILURE'
            logger.info("Upload of files failed")

        else:
            status = 'FAILED'
            logger.info("CWL and upload both failed")

def upload_all_output(localdir, remotedir, logger):
    """ upload output files to object store """

    all_exit_code = list()

    for filename in os.listdir(localdir):
        localfilepath = os.path.join(localdir, filename)
        remotefilepath = os.path.join(remotedir, filename)
        exit_code = pipelineUtil.upload_to_cleversafe(logger, remotefilepath, localfilepath)
        all_exit_code.append(exit_code)

    return all_exit_code

def is_nat(x):
    '''
    Checks that a value is a natural number.
    '''
    if int(x) > 0:
        return int(x)
    raise argparse.ArgumentTypeError('%s must be positive, non-zero' % x)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run MuSE variant calling CWL")
    required = parser.add_argument_group("Required input parameters")
    required.add_argument("--refdir", help="path to reference dir on object store")
    required.add_argument("--block", type=is_nat, default=50000000, help="parallel block size")
    required.add_argument('--thread_count', type=is_nat, default=8, help='thread count')

    required.add_argument("--normal", default=None, help="path to normal bam file")
    required.add_argument("--tumor", default=None, help="path to tumor bam file")
    required.add_argument("--normal_id", default=None, help="UUID for normal BAM")
    required.add_argument("--tumor_id", default=None, help="UUID for tumor BAM")
    required.add_argument("--case_id", default=None, help="UUID for case")

    required.add_argument("--username", default=None, help="Username for postgres")
    required.add_argument("--password", default=None, help="Password for postgres")
    required.add_argument("--cwl", default=None, help="Path to CWL code")

    optional = parser.add_argument_group("Optional input parameters")
    optional.add_argument("--s3dir", default="s3://muse_variant/", help="path to output files")
    optional.add_argument("--basedir", default="/mnt/SCRATCH/", help="Base directory for computations")

    args = parser.parse_args()

    if not os.path.isdir(args.basedir):
        raise Exception("Could not find path to base directory: %s" %args.basedir)

    #create directory structure
    casedir = tempfile.mkdtemp(prefix="muse_%s_" %args.case_id, dir=args.basedir)
    workdir = tempfile.mkdtemp(prefix="workdir_", dir=casedir)
    inp = tempfile.mkdtemp(prefix="input_", dir=casedir)
    index = tempfile.mkdtemp(prefix="index_", dir=casedir)

    #establish connection with database

    DATABASE = {
        'drivername': 'postgres',
        'host' : 'pgreadwrite.osdc.io',
        'port' : '5432',
        'username': args.username,
        'password' : args.password,
        'database' : 'prod_bioinfo'
    }

    engine = postgres.db_connect(DATABASE)

    #generate a random uuid
    vcf_uuid = uuid.uuid4()
    vcf_file = "%s.vcf" %(str(vcf_uuid))

    #setup logger
    log_file = os.path.join(workdir, "%s.muse.cwl.log" %str(vcf_uuid))
    logger = setupLog.setup_logging(logging.INFO, str(vcf_uuid), log_file)

    #logging inputs
    logger.info("normal_bam_path: %s" %(args.normal))
    logger.info("normal_bam_id: %s" %(args.normal_id))
    logger.info("tumor_bam_path: %s" %(args.tumor))
    logger.info("tumor_bam_id: %s" %(args.tumor_id))
    logger.info("case_id: %s" %(args.case_id))
    logger.info("vcf_id: %s" %(str(vcf_uuid)))

    #Get datetime
    datetime_now = str(datetime.datetime.now())
    #Get CWL start time
    cwl_start = time.time()

    #download
    logger.info("getting refs")
    pipelineUtil.download_from_cleversafe(logger, args.refdir, index)
    reference_fasta_name = os.path.join(index,"GRCh38.d1.vd1.fa")
    reference_fasta_fai = os.path.join(index,"GRCh38.d1.vd1.fa.fai")
    dbsnp_known_snp_sites = os.path.join(index,"dbsnp_144.grch38.vcf.bgz")

    logger.info("getting normal bam")
    pipelineUtil.download_from_cleversafe(logger, os.path.dirname(args.normal)+'/', inp)
    bam_norm = os.path.join(inp, os.path.basename(args.normal))

    logger.info("getting tumor bam")
    pipelineUtil.download_from_cleversafe(logger, os.path.dirname(args.tumor)+'/',  inp)
    bam_tumor = os.path.join(inp, os.path.basename(args.tumor))

    os.chdir(workdir)
    #run cwl command
    cmd = ['/home/ubuntu/.virtualenvs/p2/bin/cwl-runner', "--debug", args.cwl,
            "--reference_fasta_name", reference_fasta_name,
            "--reference_fasta_fai", reference_fasta_fai,
            "--normal_bam_path", bam_norm,
            "--tumor_bam_path", bam_tumor,
            "--normal_id", args.normal_id,
            "--tumor_id", args.tumor_id,
            "--dbsnp_known_snp_sites", dbsnp_known_snp_sites,
            "--Parallel_Block_Size", str(args.block),
            "--thread_count", str(args.thread_count),
            "--case_id", args.case_id,
            "--username", args.username,
            "--password", args.password,
            "--output", vcf_file
            ]

    cwl_exit = pipelineUtil.run_command(cmd, logger)

    cwl_failure = False
    if cwl_exit:
        cwl_failure = True

    #rename outputs
    orglog2 = os.path.join(workdir, "%s_muse_call.log" % args.case_id)
    os.rename(orglog2, os.path.join(workdir, "%s_muse_call.log" % str(vcf_uuid)))
    orglog3 = os.path.join(workdir, "%s_muse_sump_wxs.log" % args.case_id)
    os.rename(orglog3, os.path.join(workdir, "%s_muse_sump_wxs.log" % str(vcf_uuid)))

    #upload results to s3

    muse_location = os.path.join(args.s3dir, str(vcf_uuid))

    vcf_upload_location = os.path.join(muse_location, vcf_file)

    exit = upload_all_output(workdir, muse_location, logger)

    cwl_end = time.time()
    cwl_elapsed = cwl_end - cwl_start
    met = Time(case_id = args.case_id,
               datetime_now = datetime_now,
               vcf_id = str(vcf_uuid),
               files = [args.normal_id, args.tumor_id],
               elapsed = cwl_elapsed,
               thread_count = str(args.thread_count))

    postgres.create_table(engine, met)
    postgres.add_metrics(engine, met)

    status, loc = update_postgres(exit, cwl_failure, vcf_upload_location, muse_location, logger)

    status_postgres.add_status(engine, args.case_id, args.normal_id, str(vcf_uuid), [args.normal_id, args.tumor_id], status, loc)

    #remove work and input directories
    pipelineUtil.remove_dir(casedir)
