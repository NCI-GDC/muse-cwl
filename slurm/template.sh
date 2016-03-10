#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=XX_THREAD_COUNT_XX
#SBATCH --ntasks=1
#SBATCH --workdir="/mnt/SCRATCH/"
#SBATCH --mem=6000

refdir="XX_REFDIR_XX"
block="XX_BLOCKSIZE_XX"
thread_count="XX_THREAD_COUNT_XX"

normal="XX_NORMAL_XX"
tumor="XX_TUMOR_XX"
normal_id="XX_NORMAL_ID_XX"
tumor_id="XX_TUMOR_ID_XX"
case_id="XX_CASE_ID_XX"

s3dir="XX_S3DIR_XX"

repository="git@github.com:NCI-GDC/muse-cwl.git"

wkdir=`sudo mktemp -d -t muse.XXXXXXXXXX -p /mnt/SCRATCH/` \
&& sudo chown ubuntu:ubuntu $wkdir \
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
--basedir $wkdir \
--s3dir $s3dir \
--cwl $wkdir/muse-cwl/workflows/muse-wxs-workflow.cwl.yaml

trap cleanup EXIT
function cleanup (){
    echo "cleanup tmp data";
    rm -rf $wkdir;
}
