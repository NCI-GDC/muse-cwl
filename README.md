# GDC MuSE (v1.0rc_submission_c039ffa) CWL

MuSE is somatic point mutation caller developed by Dr. Wenyi Wang’s group in MD Anderson Cancer Center (MDACC), and used by the Human Genome Sequencing Center (HGSC) in the Baylor College of Medicine (BCM). Thus it is often referred to as the Baylor pipeline. This pipeline takes a pair of tumor and normal BAM files, and does two-step calling and summarization to generate somatic SNV and INDEL VCFs. The only auxiliary file requirement is a VCF file from Single Nucleotide Polymorphism Database (dbSNP) for annotation.

Original MuSE: http://bioinformatics.mdanderson.org/main/MuSE

## Docker

All the docker images are built from `Dockerfile`s at https://github.com/NCI-GDC/muse-tool.

## CWL

https://www.commonwl.org/

The CWL are tested under multiple `cwltools` environments. The most tested one is:
* cwltool 1.0.20180306163216


## For external users

There is a production-ready GDC CWL workflow at https://github.com/NCI-GDC/gdc-somatic-variant-calling-workflow, which uses this repo as a git submodule.

Please notice that you may want to change the docker image host of `dockerPull:` for each CWL.

To use CWL directly from this repo, we recommend to run `tools/muse_call.cwl` + `tools/muse_sump.cwl` or `tools/multi_muse_call.cwl` + `tools/muse_sump.cwl`.

To run CWL:

```
>>>>>>>>>>MuSE call<<<<<<<<<<
cwltool tools/muse_call.cwl -h
/home/ubuntu/.virtualenvs/p2/bin/cwltool 1.0.20180306163216
Resolved 'tools/muse_call.cwl' to 'file:///mnt/SCRATCH/githubs/submodules/m/muse-cwl/tools/muse_call.cwl'
usage: tools/muse_call.cwl [-h] --normal_bam NORMAL_BAM --ref REF --region
                           REGION --tumor_bam TUMOR_BAM
                           [job_order]

positional arguments:
  job_order             Job input json file

optional arguments:
  -h, --help            show this help message and exit
  --normal_bam NORMAL_BAM
  --ref REF
  --region REGION
  --tumor_bam TUMOR_BAM

>>>>>>>>>>MuSE sump<<<<<<<<<<

cwltool tools/muse_sump.cwl -h
/home/ubuntu/.virtualenvs/p2/bin/cwltool 1.0.20180306163216
Resolved 'tools/muse_sump.cwl' to 'file:///mnt/SCRATCH/githubs/submodules/m/muse-cwl/tools/muse_sump.cwl'
usage: tools/muse_sump.cwl [-h] --call_output CALL_OUTPUT --dbsnp DBSNP
                           [--exp_strat EXP_STRAT] --output_base OUTPUT_BASE
                           [job_order]

positional arguments:
  job_order             Job input json file

optional arguments:
  -h, --help            show this help message and exit
  --call_output CALL_OUTPUT
  --dbsnp DBSNP
  --exp_strat EXP_STRAT
                        E or G. E should be used for WXS and G for WGS.
  --output_base OUTPUT_BASE
```

## For GDC users

See https://github.com/NCI-GDC/gdc-somatic-variant-calling-workflow.
