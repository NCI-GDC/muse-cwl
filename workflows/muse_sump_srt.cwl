#!/usr/bin/env cwl-runner

cwlVersion: v1.0

class: Workflow

requirements:
  - class: InlineJavascriptRequirement
  - class: StepInputExpressionRequirement

inputs:
  - id: call_output
    type: File
  - id: prefix
    type: string
  - id: dbsnp
    type: File
  - id: exp_strat
    type: string
  - id: java_opts
    type: string
  - id: nthreads
    type: string
  - id: reference_dict
    type: File

outputs:
  - id: sorted_vcf
    type: File
    outputSource: picard_sortvcf/sorted_output_vcf

steps:
  - id: muse_sump
    run: ../tools/muse_sump.cwl
    in:
      - id: dbsnp
        source: dbsnp
      - id: call_output
        source: call_output
      - id: exp_strat
        source: exp_strat
      - id: output_base
        source: prefix
        valueFrom: $(self + '.MuSE.unsorted.vcf')
    out:
      - id: output_file

  - id: picard_sortvcf
    run: ../tools/picard-sortvcf.cwl
    in:
      - id: java_opts
        source: java_opts
      - id: nthreads
        source: nthreads
      - id: reference_dict
        source: reference_dict
      - id: output_vcf
        source: prefix
        valueFrom: $(self + '.MuSE.vcf.gz')
      - id: input_vcf
        source: muse_sump/output_file
    out:
      - id: sorted_output_vcf
