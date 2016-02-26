#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=XX_THREAD_COUNT_XX
#SBATCH --ntasks=1
#SBATCH --workdir=XX_BASEDIR_XX

refdir="XX_REFDIR_XX"
block="XX_BLOCKSIZE_XX"
thread_count="XX_THREAD_COUNT_XX"

normal="XX_NORMAL_XX"
tumor="XX_TUMOR_XX"
normal_id="XX_NORMAL_ID_XX"
tumor_id="XX_TUMOR_ID_XX"
case_id="XX_CASE_ID_XX"

basedir="XX_BASEDIR_XX"
s3dir="XX_S3DIR_XX"


username="XX_USERNAME_XX"
password="XX_PASSWORD_XX"

repository="git@github.com:NCI-GDC/muse-cwl.git"

wkdir=`mktemp -d -p /mnt/SCRATCH/` \
&& cd $wkdir \
&& sudo git clone -b feat/slurm $repository \
&& sudo chown ubuntu:ubuntu muse-cwl \
&& /home/ubuntu/.virtualenvs/p2/bin/python muse-cwl/slurm/run_cwl.py \
--refdir $refdir \
--block $block \
--thread_count $thread_count \
--normal $normal \
--normal_id $normal_id \
--tumor $tumor \
--tumor_id $tumor_id \
--case_id $case_id \
--basedir $basedir \
--s3dir $s3dir \
--username $username \
--password $password \
--cwl $wkdir/muse-cwl/workflows/muse-wxs-workflow.cwl.yaml

sudo rm -rf $wkdir
