import argparse
import pipelineUtil
import uuid
import os
import postgres
import setupLog
import logging
import shutil

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
    required.add_argument("--ref", default="/mnt/SRCATCH/index/GRCh38.d1.vd1.fa", help="path to reference genome")
    required.add_argument("--refindex", default="/mnt/SCRATCH/index/GRCh38.d1.vd1.fa.fai", help="Path to ref index on object store")
    required.add_argument("--refdict", default="/mnt/SCRATCH/index/GRCh38.d1.vd1.dict", help="Path to ref dict on object store")
    required.add_argument("--snp", default="/mnt/SRCATCH/index/dbsnp_144.grch38.vcf.bgz", help="path to known dbsnp sites")
    required.add_argument("--snpindex", default="/mnt/SCRATCH/index/dbsnp_144.grch38.vcf.bgz.tbi", help="Path to dbsnp index on object store")
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
    optional.add_argument("--s3dir", default="s3://bioinformatics_scratch/", help="path to output files")
    optional.add_argument("--basedir", default="/mnt/SCRATCH/", help="Base directory for computations")

    args = parser.parse_args()

    if not os.path.isdir(args.basedir):
        raise Exception("Could not find path to base directory: %s" %args.basedir)

    #create directory structure
    index = os.path.join(args.basedir, "index")
    workdir = os.path.join(args.basedir, "workdir")
    inp = os.path.join(args.basedir, "input")

    if not os.path.isdir(index):
        os.mkdir(index)

    if not os.path.isdir(workdir):
        os.mkdir(workdir)

    if not os.path.isdir(inp):
        os.mkdir(inp)

    #generate a random uuid
    vcf_uuid = uuid.uuid4()
    vcf_file = "%s.vcf" %(str(vcf_uuid))

    #setup logger
    log_file = os.path.join(workdir, "%s.muse.cwl.log" %str(vcf_uuid))
    logger = setupLog.setup_logging(logging.INFO, str(vcf_uuid), log_file)

    #download bam files
    reference = os.path.join(index, "GRCh38.d1.vd1.fa")
    if not os.path.isfile(reference):
        logger.info("getting reference")
        pipelineUtil.download_from_cleversafe(logger, args.ref, index)
        reference = os.path.join(index, os.path.basename(args.ref))

    reference_index = os.path.join(index, "GRCh38.d1.vd1.fa.fai")
    if not os.path.isfile(reference_index):
        logger.info("getting reference index")
        pipelineUtil.download_from_cleversafe(logger, args.refindex, index)
        reference_index = os.path.join(index, os.path.basename(args.refindex))

    reference_dict = os.path.join(index, "GRCh38.d1.vd1.dict")
    if not os.path.isfile(reference_dict):
        logger.info("getting reference dict")
        pipelineUtil.download_from_cleversafe(logger, args.refdict, index)
        reference_dict = os.path.join(index, os.path.basename(args.refdict))

    dbsnp = os.path.join(index, "dbsnp_144.grch38.vcf.bgz")
    if not os.path.isfile(dbsnp):
        logger.info("getting known dbsnp sites")
        pipelineUtil.download_from_cleversafe(logger, args.snp, index)
        dbsnp = os.path.join(index, os.path.basename(args.snp))

    dbsnp_index = os.path.join(index, "dbsnp_144.grch38.vcf.bgz.tbi")
    if not os.path.isfile(dbsnp_index):
        logger.info("getting known dbsnp index")
        pipelineUtil.download_from_cleversafe(logger, args.snpindex, index)
        dbsnp_index = os.path.join(index, os.path.basename(args.snpindex))

    logger.info("getting normal bam")
    pipelineUtil.download_from_cleversafe(logger, args.normal, inp)
    bam_norm = os.path.join(inp, os.path.basename(args.normal))

    logger.info("geeting tumor bam")
    pipelineUtil.download_from_cleversafe(logger, args.tumor,  inp)
    bam_tumor = os.path.join(inp, os.path.basename(args.tumor))

    os.chdir(workdir)
    #run cwl command
    cmd = ['/home/ubuntu/.virtualenvs/p2/bin/cwl-runner', "--debug", args.cwl,
            "--reference_fasta_name", reference,
            "--reference_fasta_fai", reference_index,
            "--normal_bam_path", bam_norm,
            "--tumor_bam_path", bam_tumor,
            "--normal_id", args.normal_id,
            "--tumor_id", args.tumor_id,
            "--dbsnp_known_snp_sites", dbsnp,
            "--Parallel_Block_Size", args.block,
            "--thread_count", args.thread_count,
            "--case_id", args.case_id,
            "--username", args.username,
            "--password", args.password,
            "--output", vcf_file
            ]

    cwl_exit = pipelineUtil.run_command(cmd, logger)

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


    if cwl_exit:

        postgres.add_status(engine, args.case_id, str(vcf_uuid), [args.normal_id, args.tumor_id], "FAILED", "unknown")

    #upload results to s3

    key_location = os.path.join(args.s3dir, 'muse_results', str(vcf_uuid))
    vcf_upload_location = os.path.join(key_location, vcf_file)

    ec_1 = pipelineUtil.upload_to_cleversafe(logger, vcf_upload_location, os.path.join(workdir, vcf_file))

    ec_2 = pipelineUtil.upload_to_cleversafe(logger, os.path.join(key_location, "%s.muse.cwl.log" %(str(vcf_uuid))), log_file)

    ec_3 = pipelineUtil.upload_to_cleversafe(logger, os.path.join(key_location, "%s.muse_call.log" %(str(vcf_uuid))),
                                             os.path.join(workdir, "%s.muse_call.log" %args.case_id))
    ec_4 = pipelineUtil.upload_to_cleversafe(logger, os.path.join(key_location, "%s.muse_sump_wxs.log" %(str(vcf_uuid))),
                                             os.path.join(workdir, "%s.muse_sump_wxs.log" %args.case_id))

    if not(ec_1 and ec_2 and ec_3 and ec_4):

        postgres.add_status(engine, args.case_id, str(vcf_uuid), [args.normal_id, args.tumor_id], "COMPLETED", vcf_upload_location)

    else:

        postgres.add_status(engine, args.case_id, str(vcf_uuid), [args.normal_id, args.tumor_id], "FAILED", key_location)

    #remove work and input directories
    shutil.rmtree(inp)
    shutil.rmtree(workdir)
